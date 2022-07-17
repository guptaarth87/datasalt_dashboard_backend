from unittest import result
from flask import Flask,render_template
from app import app, mongo
from home import home_bp
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask import jsonify, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import *
import collections

global patients
global length
users=mongo.db.Patients.find()
patients =dumps(users)

patients=json.loads(patients)
length=len(patients)

def freq_res(month_list):
   res={'january':0,'febraury':0,'march':0,'april':0,'may':0,'june':0,'july':0,'august':0,'september':0,'october':0,'november':0,'december':0}
   for month in month_list:
        if month==1:
          res['january']+=1
        elif month==2:
          res['febraury']+=1
        elif month==3:
          res['march']+=1
        elif month==4:
          res['april']+=1
        elif month==5:
          res['may']+=1
        elif month==6:
          res['june']+=1
        elif month==7:
          res['july']+=1
        elif month==8:
          res['august']+=1
        elif month==9:
          res['september']+=1
        elif month==10:
          res['october']+=1
        elif month==11:
          res['november']+=1
        elif month==12:
          res['december']+=1
   return res

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello User!"

@app.route('/getdata', methods=['GET'])
def getdata():
    if patients!=[]:
       return {"response":patients , "status":200}
    else:
        return {"response":"server error", "status" : 404}

@app.route('/databydate/<string:start>/<string:end>',methods=['GET','POST'])
def get_databydate(start,end):
   req=[]
   if start!='null':
     d1, m1, y1 = [int(x) for x in start.split('-')]
     start = date(y1, m1, d1)

   if end!='null':
     d2, m2, y2= [int(x) for x in  end.split('-')]
     end = date(y2, m2, d2)
   for i in range (0,length):
     y3, m3, d3 = [int(x) for x in patients[i]['date'].split('-')]
     temp_date = date(y3, m3, d3)
   
     if start !='null' and end != 'null':
       if temp_date>=start and temp_date<=end:
         req.append(patients[i])
       else:
         continue
     elif start == 'null' and end !='null':
       if temp_date <= end:
         req.append(patients[i])
       else:
         continue
     elif end == 'null' and start !='null':
        if temp_date >=start:
          req.append(patients[i])
        else:
          continue
     else:
       continue
   
   if req==[]:
     return {"response":"inappropriate date given","status":404}
   else:
     return {"response":req, "status":200}


@app.route('/databytag/<string:tag>',methods=['GET','POST'])
def get_databytag(tag):
    tag_ = tag
    l1=[]
    for j in range(0,length):
      if tag_ in patients[j]['tags']:
        l1.append(patients[j])
      else:
        continue
    temp_l=[]
    for k in range (0,len(l1)):
       month=int(l1[k]['date'][5:7])
       temp_l.append(month)
    res=freq_res(temp_l)
    
    #second response
    l2=[]
    req=[]
    for d in range(0,length):
      if tag_ in patients[d]['tags']:
        l2.append(patients[d])
      else:
        continue
    for m in l1:
       for _ in m['medication']:
          req.append(_)
   
    req_frequency= collections.Counter(req)
    if res!=[]:
       return {"response":res,
               "status":200,
               "requres_data":req,
               "medication_used_for_tag_frequency":dict(req_frequency)
                }
    else:
        return {"response":"server error","status":404}

@app.route('/databyeffect/<string:effect>',methods=['GET','POST'])
def get_databyeffect(effect):
    list_of_=[]
    ln=len(patients)
    resx=effect
    for j in range(0,ln-1):
      if patients[j]['result']==resx:
        list_of_.append(patients[j])
        # print(patients[j])
      else:
        continue
    tags_=[]
    medication_=[]
    
    for tem in list_of_:
       for _ in tem['tags']:
         tags_.append(_)
         
    for tem in list_of_:
       for _ in tem['medication']:
         medication_.append(_)
    
    
    frequency_of_tags = collections.Counter(tags_)
    frequency_of_medication = collections.Counter(medication_)
    
    if list_of_!=[]:
      return {
          "data":list_of_,
          "tags_used":tags_,
          "tags_frequency":dict(frequency_of_tags),
          "medication_frequency":dict(frequency_of_medication),
          "status":200
      }
    else:
        return{
            {"response":"server error or may be no available data","status":404}
        }

@app.route('/databymedication/<string:tag>',methods=['GET','POST'])
def get_databymedication(tag):
    medication_ = tag
    filtered_list=[]
    for j in range(0,length):
      if medication_ in patients[j]['medication']:
        filtered_list.append(patients[j])
        print(patients[j])
      else:
        continue
    temp_l1=[]
    for k in range (0,len(filtered_list)):
       
       month=int(filtered_list[k]['date'][5:7])
       temp_l1.append(month)
    resn=freq_res(temp_l1)
    if resn!=[]:
       return {"response":resn,"status":200}
    else:
        return {"response":"server error","status":404}


   
def fetch():
    users=mongo.db.Patients.find()
    return dumps(users)

def appRun(): 
  if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=105)
    
    patients=fetch()
  else:
      app.logger.error('This is an ERROR message')

app.register_blueprint(home_bp, url_prefix='/home')

appRun()
