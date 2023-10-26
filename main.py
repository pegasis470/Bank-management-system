from costumer import Costumer,signup
from admin import AdminActions,Admin

if __name__=='__main__':
    print("### Welcome to farziwada bank ### ")
    print("Press 1 open an account ")
    print("Press 2 to login as existing costumer")
    print("Press 3 to login as Administrator")
    choice=int(input())
    if choice ==1:
        name=input("Please Enter your name: ")
        username=input("Please choose a username: ")
        password=input("Please choose a password: ")
        signup(name,username,password)
    elif choice == 2:
        costumer=Costumer()
        if costumer.Auth:
            while True:
                print("Press 1 to withdraw")
                print("Press 2 to deposite")
                print("press 3 to apply for a loan")
                print("press 9 to logout")
                c=int(input())
                if c == 1:
                    amt=int(input("Enter amount to withdraw: "))
                    costumer.Withdraw(amt)
                elif c == 2 :
                    amt=int(input("Enter amount to deposit: "))
                    costumer.Deposit(amt)
                elif c == 3:
                    amt=int(input("Enter the required amount: "))
                    time=int(input("Enter the number for years: "))
                    costumer.Loan_appeal(amt,time)
                elif c == 9:
                    del costumer
                    break
    elif choice == 3 :
        while True:
            print("press 1 to preform sudo oprations:")
            print("press 2 for other oprations:")
            print("Press 3 to exit")
            ad=int(input())
            if ad==1:
                admin=Admin()
                print("press 1 to add an admin")
                print('press 2 to remove admin')
                print("press 3 to change access")
                print("Press 4 to logout")
                a=int(input())
                if a == 1:
                    name=input("Enter the name of the admin to add: ")
                    user=input("Enter the username of the admin to add: ")
                    password=input("Enter the password of the new admin: ")
                    access=input("Enter the access level of new admin: ")
                    admin.AddAdmin(name,user,password,access)
                elif a == 2:
                    user=print('Enter the username of the admin to delete: ')
                    admin.RemoveAdmin(user)
                elif a == 3:
                    user=input("Enter the username of admin to change: ")
                    access=input("Enter the new access level: ")
                    admin.ChangeAccess(user,access)
                elif a==4:
                    print(f"bye! see you agian {admin.user}")
                    del admin
            elif ad==2:
                admin=AdminActions()
                print("press 1 to add a costumer")
                print("press 2 to remove a costumer")
                print("press 3 to approve a loan request")
                print("press 4 to logout")
                x=int(input())
                if x == 1:
                    name=input("Enter the name of the costumer: ")
                    admin.add_costumer(name)
                elif x == 2:
                    user=input("Enter the username of the costumner to remove: ")
                    admin.remove_costumer(user)
                elif x == 3:
                    user=input("Enter username of the costumer to approve loan")
                    admin.approve_loan(user)
                elif x == 4:
                    print("bye! see you agian {admin.admin.user}")
                    del admin
            elif ad == 3:
                break
