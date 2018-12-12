import os,cgi,json,time,datetime,base64,MySQLdb,MySQLdb.cursors,paramiko
from pprint import pprint

"""
12/12/2018
goal: check path in FUSQA table and insert 1 or 0 if files exist
workflow note:
- query connect to FUSQA table  (DFRandomForestHCCResponse.FUSQA to be exact)
- loop through the path and check if the path contain any files
      key script: len(os.listdir(path))
- insert 1,0 accordingly into FUSDIRBool column
Note: the keyscript can actually show the number of files exists and compare with PACs to see if we get everything
"""

db = MySQLdb.connect(xxxx)

##NORMAL CURSOR: DATA SAVE IN ARRAY - WE DONT USE THIS
cur = db.cursor()
##DICTIONARY CURSOR: DATA SAVE AS DICTIONARY (SAVE TIME) - USE THIS
d_cur = db.cursor(MySQLdb.cursors.DictCursor)
######

## this is for 
def checkFUS4():
  d_cur.execute ('SELECT id, FUSDIRPath, FUSDIRBool FROM DFRandomForestHCCResponse.FUSQA')
  rdata = d_cur.fetchall();  
  print
  print("start checking")
  for row in rdata:
    path = row['FUSDIRPath']
    id = row['id']
    try:
      emptycheck = len(os.listdir(path))
    except:
      emptycheck = 0
    ##update 1,0 to Bool accordingly 
    d_cur.execute('SET SQL_SAFE_UPDATES = 0;')
    q = """UPDATE DFRandomForestHCCResponse.FUSQA 
           SET FUSDIRBool = %s WHERE id =%s
        """    
    if emptycheck == 0:
      v = ('0',id)
      print(q % v)
      cur.execute(q,v)
    else:
      v = ('1',id)
      ##print(q % v)
      cur.execute(q,v)
  db.commit()
  print('done')
  db.close()          
  
  
if action =='blank':
  print
  print"doing nothing to prevent the code run by accident"

elif action =='run_me':
  checkFUS4()
