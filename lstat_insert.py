import os,cgi,json,time,datetime,base64,MySQLdb,MySQLdb.cursors,paramiko
from pprint import pprint
import sys

"""
workflow note:
- Run command c3d ussing paramiko ssh connection to remove server
- use python to stdout the result 
- parse result and save into mysql database
"""

##NORMAL CURSOR: DATA SAVE IN ARRAY - WE DONT USE THIS
cur = db.cursor()
##DICTIONARY CURSOR: DATA SAVE AS DICTIONARY (SAVE TIME) - USE THIS
d_cur = db.cursor(MySQLdb.cursors.DictCursor)
######

user_name="xxx"
password = "xxx"
ip = "10.115.8.182"

print
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=user_name, password=password)

if action =='blank':
  print
  print"doing nothing to prevent the code run by accident"

  
elif action=="run_me":
  cmd_cd = "cd /rsrch1/ip/ip-comp_rsch_lab/github/dcelitt;"
  ##THIS SHOULD COME FORM DATABASE WHEN AVAILABLE
  cmd_main = []
  cmd_main.append("c3d datalocation/1087780/20160503/1.2.840.114350.2.412.2.798268.2.22265409.1/1.3.12.2.1107.5.2.31.30165.2016050315022229297233770.0.0.0/subvolume.nii.gz -dup -lstat")
  cmd_main.append("c3d datalocation/1087780/20160606/1.2.840.114350.2.412.2.798268.2.23883474.1/1.2.840.113619.2.374.4120.7587709.18907.1465214753.700/subvolume.nii.gz -dup -lstat")
  for line in cmd_main:

    ##split()[1] = datalocation/1087780/20160606/1.2.840.114350.2.412.2.798268.2.23883474.1/1.2.840.113619.2.374.4120.7587709.18907.1465214753.700/subvolume.nii.gz
    path = line.split()[1]
    InstanceUID = path.split("/")[4]
    SegmentationID = path.split("/")[-1]
    FeatureID='auc60.roirel'
 
    ##RUN COMMAND AND PARSE OUTPUT
    ##combine and run both command: cd /rsrch1/ip/ip-comp_rsch_lab/github/dcelitt; c3d datalocation/1087780/20160606/1.2.840.114350.2.4.....subvolume.nii.gz -dup -lstat
    stdin, stdout, stderr = ssh_client.exec_command(cmd_cd+line)
    res=stdout.read()
    ## InstanceUID, SegmentationID, FeatureID, LabelID, Mean, StdD, Max, Min, Count, Volume, ExtentX, ExtentY, ExtentZ
    for line in res.split("\n")[1:]:
      ##t_values = line.split("\t")
      t_values = line.split()
      if len(t_values) >1:
        [LabelID, Mean, StdD, Max, Min, Count, Volume, ExtentX, ExtentY, ExtentZ] = t_values
      else:
        continue
      
      ##Query replace into
      q = """REPLACE INTO student_intern.lstat(InstanceUID, SegmentationID, FeatureID, LabelID, Mean, StdD, Max, Min, Count, Volume, ExtentX, ExtentY, ExtentZ) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
      v=(InstanceUID, SegmentationID, FeatureID, LabelID, Mean, StdD, Max, Min, Count, Volume, ExtentX, ExtentY, ExtentZ)
      print (q % v)
      cur.execute(q,v)
  db.commit()
  print('done')
  db.close() 
