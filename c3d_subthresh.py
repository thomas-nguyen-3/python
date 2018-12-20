
##
##Goal: run command :  c3d linuxAUCFile -thresh .15 inf 1 0 -o linuxlabelFile
##Process note:
## - query to get linuxAUCFile path and linuxlabelFile destination path
##   select linuxAUCFile, linuxlabelFile from DFdcelitt.manualdceuid;
## - run command through paramiko.SSHClient()
## if there is error (ex: files not exit) during executtion loop, it will bring out and continue next iteration.
import os,cgi,json,time,datetime,base64,MySQLdb,MySQLdb.cursors,paramiko
from pprint import pprint
import sys
import paramiko
import getpass
import random

##Database connection
db = MySQLdb.connect(host='scrdep2.mdanderson.org',    # your host, usually localhost
                     user="xxxx",         # your username
                     passwd="xxxx",  # your password
                     db="DFdcelitt")        # name of the data base


##NORMAL CURSOR: DATA SAVE IN ARRAY -
cur = db.cursor()
##DICTIONARY CURSOR: DATA SAVE AS DICTIONARY (SAVE TIME) - USE THIS WHEN NEED DICTIONARY OUTPUT
d_cur = db.cursor(MySQLdb.cursors.DictCursor)
######

user_name="xxx"
password = "xxxx"
ip = "10.1xxx182"

print
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=user_name, password=password)

##CALL TO RUN THE MAIN CODE
action=form_dict.get('action','c3d_subthresh')

## c3d linuxAUCFile -thresh .15 inf 1 0 -o linuxlabelFile 
elif action=="c3d_subthresh":
  ##GET file location and file destination path 
  q = """select linuxAUCFile, linuxlabelFile from DFdcelitt.manualdceuid;"""
  d_cur.execute(q)
  rdata = d_cur.fetchall();
  ##cd to dcelitt
  cmd_cd = "cd /rsrch1/ip/ip-comp_rsch_lab/github/dcelitt;"
  
  for row in rdata:
    linuxAUCFile = row['linuxAUCFile']
    linuxlabelFile = row['linuxlabelFile']
    ##linuxlabelFile = '/home/tbnguyen3/dcelitt/'
    ##print(linuxlabelFile)
    try:
      ##copy to local for testing or real
      ##cmd_c3d = 'c3d '+linuxAUCFile+ ' -thresh .15 inf 1 0 -o /home/tbnguyen3/dcelitt/subthresh'+str(random.randint(1,101))+'.nii.gz'
      cmd_c3d = 'c3d '+linuxAUCFile+ ' -thresh .15 inf 1 0 -o '+linuxlabelFile

      ##RUN COMMAND AND PARSE OUTPUT
      ##combine and run both command: cd /rsrch1/ip/ip-comp_rsch_lab/github/dcelitt; c3d linuxAUCFile -thresh .15 inf 1 0 -o linuxlabelFile
      stdin, stdout, stderr = ssh_client.exec_command(cmd_cd+cmd_c3d)
    except Exception as e:    
      cmd_c3d=""
      print("error: "+linuxAUCFile)
      print(e)
  print("done")
