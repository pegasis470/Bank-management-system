#!/user/bin/python3
import os
import pandas as pd
from error import AdminError
from datetime import datetime as dt
def write_admin_logs(action,user):
    path="Logs/admin_logs.log"
    with open(path,'a') as file:
        time=dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
        file.write(f"{time}: {user}  {action} \n")
active_admins=[]
#Sudo
class Admin:
    def __init__(self):
        self.Auth=False
        self.Access=0
        print("*** Logging in in as ADMINISTRATOR ***")
        self.user=input("Enter Your Username: ")
        user=self.user
        password=input("Enter Your Password: ")
        self.data=pd.read_csv('Admin/data.csv')
        if "Unnamed: 0" in self.data.columns:
            self.data=self.data.drop("Unnamed: 0",axis=1)
        data=self.data
        if user in data['username'].values:
            user_name=data['username'][data['username']==user].values[-1]
            user_pass=str(data['password'][data['username']==user].values[-1])
            if user == user_name and password==user_pass:
                if user not in active_admins:
                    self.Auth=True
                    self.Access=data['access'][data['username']==user].values[-1]
                    active_admins.append(user)
                    write_admin_logs("Succesfully logged in ",user)
                else:
                    raise AdminError.AlreadyActive(user)
            else:
                raise AdminError.AuthFailure(user)
        else:
            raise AdminError.PermissionFailure(user)
    def AddAdmin(self,new_name,new_user,new_pass,new_access):
        if self.Auth:
            if self.Access != 3:
                if new_access > 3 or new_access < 1:
                    print("Invalid Access Specifier")
                    write_admin_logs(f"faild to Added {new_user} as Admin",self.user)
                    return 0
                data=pd.read_csv('Admin/data.csv').drop('Unnamed: 0',axis=1)
                data.loc[len(data.index)]=[new_name,new_user,new_pass,new_access]
                data.to_csv('Admin/data.csv')
                write_admin_logs(f"Added {new_user} as Admin",self.user)
                print("New admin added.")
                print(f"*** Welcome {new_name} ***")
            else:
                raise AdminError.PermissionFailure(self.user)
    def RemoveAdmin(self,user):
        if self.Auth:
            data=pd.read_csv('Admin/data.csv').drop('Unnamed: 0',axis=1)
            if user in data['username'].values:
                access=data['access'][data['username']==user].values[-1]
                if self.Access >= access: 
                    ind=data['username'][data['username']==user].index[0]
                    data=data.drop(ind)
                    data.to_csv("Admin/data.csv")
                    write_admin_logs(f"Deleted {user}",self.user)
                else:
                    raise AdminError.PermissionFailure(self.user)          
            else:
                print(f"Sorry {user} is not an admin")
    def ChangeAccess(self,user,new_access):
        if self.Auth:
            if self.Access >= 2:
                data=pd.read_csv('Admin/data.csv').drop('Unnamed: 0',axis=1)
                if user in data['username'].values:
                    if new_access > 3 or new_access < 1:
                        print("Invalid Access Specifier")
                        write_admin_logs(f"faild to Added {new_user} as Admin",self.user)
                        return 0
                    data.loc[data['username']==user,'access'] = new_access
                    write_admin_logs(f"changed {user} access",self.user)
                    print("*** {user} access changed ***")
                else:
                    write_admin_logs("Attempt to change {user} access failed",self.user)
                    print("{user} is not an admin")
            else:
                raise AdminError.PermissionFailure(self.user)
    def __del__(self):
        active_admins.remove(self.user)

#Admin
class AdminActions:
    def __init__(self):
        self.admin=Admin() #Sudo()
        #self.user_data=pd.read_csv('Costumer/data.csv').drop('Unnamed: 0',axis=1)  
    def add_costumer(self,name,balance=500):
        if self.admin.Auth:
            user_data=pd.read_csv('Costumer/data.csv').drop('Unnamed: 0',axis=1)
            data=pd.read_csv("Costumer/account_req.csv").drop('Unnamed: 0',axis=1)
            name=data.loc[data['name']==name,'name'].values[-1]
            username=data.loc[data['name']==name,'username'].values[-1]
            password=data.loc[data['name']==name,'password'].values[-1]  
            CFID=user_data.iloc[-1].values[-1]+1
            user_data.loc[len(user_data.index)]=[name,username,password,balance,CFID]
            data=data.drop(data.loc[data['username']==username,'username'].index)
            write_admin_logs(f"Added {name} as a costumer",self.admin.user)
            user_data.to_csv('Costumer/data.csv')
            data.to_csv("Costumer/account_req.csv")
            print(f"{name} added as a costumer to our bank")
    def remove_costumer(self,user):
        if self.admin.Auth:
            user_data=pd.read_csv('Costumer/data.csv').drop('Unnamed: 0',axis=1)
            user_data=user_data.drop(user_data.loc[user_data['username']==user,'username'].index)
            write_admin_logs(f'Removed {user} from costumers',self.admin.user)
            print("Costumer removed")

    def approve_loan(self,costumer):
        if self.admin.Auth:
            loan_data=pd.read_csv('Costumer/loan_appeal.csv').drop('Unnamed: 0',axis=1)
            loan_approved=pd.read_csv('Admin/loan.csv').drop('Unnamed: 0',axis=1)
            amt=loan_data.loc[loan_data['user']==costumer,'amount'].values[-1]
            time=loan_data.loc[loan_data['user']==costumer,'time'].values[-1]
            ld=loan_data.drop(loan_data.loc[loan_data['user']==costumer,'user'].index)
            loan_approved.loc[len(loan_approved.index)]=[costumer,amt,time]
            write_admin_logs(f"approved {costumer} loan request",self.admin.user)
            print("*** LOAN APPROVED ***")
            loan_approved.to_csv("Admin/loan.csv")
            ld.to_csv('Costumer/loan_appeal.csv')
        else:
            raise AdminError.PermissionFailure(self.user)
    def __del__(self):
        del self.admin
