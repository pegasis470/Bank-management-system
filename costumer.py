#!/user/bin/python3
import os
import pandas as pd
from error import CostumerErrors
from datetime import datetime as dt

def write_costumer_logs(action,user):
    path="Logs/costumer_logs.log"
    with open(path,'a') as file:
        time=dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
        file.write(f"{time}: {user}  {action} \n")

def signup(name,username,password):
    data=pd.read_csv("Costumer/account_req.csv").drop("Unnamed: 0",axis=1)
    data.loc[len(data.index)]=[name,username,password]
    write_costumer_logs("Appealed to open an account",username)
    data.to_csv("Costumer/account_req.csv")
    print("Your request has been accepted we will contact you soon! ;)")


class Costumer:
    def __init__(self):
        self.Auth=False
        print("*** logging in as costumer ***")
        self.user=input("Enter your username: ")
        user=self.user
        password=input("Enter Your Password: ")
        self.data=pd.read_csv('Costumer/data.csv')
        if "Unnamed: 0" in self.data.columns:
            self.data=self.data.drop("Unnamed: 0",axis=1)
        data=self.data
        if user in data['username'].values:
            user_name=data['username'][data['username']==user].values[-1]
            user_pass=str(data['password'][data['username']==user].values[-1])
            if user == user_name and password==user_pass:
                self.Auth=True
                write_costumer_logs("Succesfully logged in ",user)
            else:
                CostumerErrors.Incorrectcredentials(user)
        else:
            CostumerErrors.NotEligibleError(user)
        if self.Auth:
            self.balance=data.loc[data['username']==self.user,'balance'].values[0]
            self.CIFID=data.loc[data['username']==self.user,'CIFID'].values[0]
            self.name=data.loc[data['username']==self.user,'name'].values[0]
        else:
            pass
    def Withdraw(self,amt):
        if self.Auth:
            if amt+500 < self.balance:
                write_costumer_logs(f'Withdrew {amt} form balance of {self.balance}',self.user)
                print(f'You withdrew {amt} your current balance is {self.balance-amt}')
                self.data.loc[self.data['username']==self.user,'balance']= self.balance-amt
                self.data.to_csv('Costumer/data.csv')
            else:
                print("Inssufficient funds")
                CostumerErrors.InvalidValues(self.user)
    def Deposit(self,amt):
        if self.Auth:
            write_costumer_logs(f'deposited {amt} form balance of {self.balance}',self.user)
            print(f'You deposited {amt} your current balance is {self.balance+amt}')
            self.data.loc[self.data['username']==self.user,'balance']= self.balance+amt
            self.data.to_csv('Costumer/data.csv')
    def Loan_appeal(self,amount,time):
        if self.Auth:
            loan_data=pd.read_csv('Costumer/loan_appeal.csv').drop('Unnamed: 0',axis=1)
            if self.user not in loan_data['user'].values:     
                if self.balance > 5000:
                    write_costumer_logs(f"Applied for a loan of {amount} for {time} year/s",self.user)
                    loan_data.loc[len(loan_data.index)]=[self.name,self.user,amount,time]
                    loan_data.to_csv("Costumer/loan_appeal.csv")
                    print("Loan application sucessful")
                else:
                    CostumerErrors.NotEligibleError(self.user)
                    print("Inssufficient funds")
            else:
                CostumerErrors.NotEligibleError(self.user)
                print("Please wait for your last loan request to be processed")

                



