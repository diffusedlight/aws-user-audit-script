# Imports 
import boto3
import csv
import os
from datetime import datetime

iam = boto3.client("iam")

userList = []
userAccountInfo = [['User', 'Date Created', 'Password Last Used']] 
accessKeyInfo = [['User', 'Access Key ID', 'Status', 'Date Created', 'Last Used']]


# Get list of users
paginator = iam.get_paginator('list_users')
for response in paginator.paginate():
    for user in response['Users']:
        userList.append(user['UserName'])
        newRow = []
        newRow.append(user['UserName'])
        newRow.append(user['CreateDate'].strftime("%d/%m/%Y"))
        if 'PasswordLastUsed' in user:
            newRow.append(user['PasswordLastUsed'].strftime("%d/%m/%Y"))
        else:
            newRow.append("Password Never Used")
        userAccountInfo.append(newRow)



# Get Access Keys from list of users
for item in userList:
    paginator = iam.get_paginator('list_access_keys')
    for response in paginator.paginate(UserName=item):
        for elem in response['AccessKeyMetadata']:
            lastUsedInfo = iam.get_access_key_last_used(AccessKeyId=elem['AccessKeyId'])
            newEntry = []
            newEntry.append(elem['UserName'])
            newEntry.append(elem['AccessKeyId'])
            newEntry.append(elem['Status'])
            newEntry.append(elem['CreateDate'].strftime("%d/%m/%Y"))
            if 'LastUsedDate' in lastUsedInfo['AccessKeyLastUsed']:
                newEntry.append(lastUsedInfo['AccessKeyLastUsed']['LastUsedDate'].strftime("%d/%m/%Y"))
            else:
                newEntry.append("Key Never Used")
            accessKeyInfo.append(newEntry)




# Create CSV's
# Console Access CSV
if os.path.exists("console-access-audit.csv"):
    os.remove("console-access-audit.csv")

if os.path.exists("programmatic-access-audit.csv"):
    os.remove("programmatic-access-audit.csv")

with open("console-access-audit.csv", 'w', newline='') as consoleFile:
    writer = csv.writer(consoleFile)
    writer.writerows(userAccountInfo)

# CLI / Programmatic Access CSV
with open("programmatic-access-audit.csv", 'w', newline='') as accessKeyFile:
    writer = csv.writer(accessKeyFile)
    writer.writerows(accessKeyInfo)