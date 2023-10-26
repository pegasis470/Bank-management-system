#!/user/bin/python3
import os
import pandas
from datetime import datetime as dt

class AdminError(Exception):
    def write_logs(error,user):
        path="Logs/error_logs.log" #os.path.join('Logs','error_logs.log')
        with open(path,'a') as file:
            time=dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
            file.write(f"{time}: {user} triggerd {error} \n")

    class AuthFailure(Exception):
        def __init__(self,user_name):
            AdminError.write_logs('Authorization faliure',user_name)
        def __str__(self):
            print("*** Initiating security lockout ***")
            return "Authorization faliure: Invalid credentials"
    class PermissionFailure(Exception):
        def __init__(self,user_name):
            AdminError.write_logs("Permission Error",user_name)
        def __str__(self):
            print("*** Initiating security lockout ***")
            return "Premission Error: You do not have premission to preform this action"
    class AlreadyActive(Exception):
        def __init__(self,user_name):
            AdminError.write_logs("Attemped double login",user_name)
        def __str__(self):
            print("*** Initiating security lockout ***")
            return "An Admin has already logged in using these credentials logout first or try agian after sometime"

class CostumerErrors:
    def write_logs(error,user):
        path="Logs/costumer_error.log"
        with open(path,'a') as file:
            time=dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
            file.write(f"{time}: {user} triggerd {error} \n")
    class Incorrectcredentials:
        def __init__(self,username):
            CostumerErrors.write_logs("IncorrectCredentialsError",username)
            print('ERROR: You have enterd Invalid credentials')
    class InvalidValues:
        def __init__(self,username,value):
            CostumerErrors.write_logs(f"entered {value} it was invalid",username)
            print(f" ERROR: {value} in invalid")
    class NotEligibleError:
        def __init__(self,username):
            CostumerErrors.write_logs(f"Applied {username} was not eligible ",username)
            print(f"ERROR:You are not eligible please contact your branch")
