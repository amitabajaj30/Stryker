from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np
from tqdm import tqdm
import plotly.express as px
#import datetime

app = Flask(__name__)

#model = pickle.load(open("t_models/", "rb"))



@app.route("/")

def home():

    return render_template("home1.html")

@app.route("/predict", methods = ["GET", "POST"])

def predict():
   
    if request.method == "POST":
     
       Shift = request.form["Shift"]
       
       DowntimeDesctiption=request.form["DowntimeDesctiption"]
       
       if(DowntimeDesctiption=="ALARM"):
            DD = 1
            
       elif(DowntimeDesctiption=="IDLE"):
            DD = 2
            
       else:
            DD = 3    
            
            
          
       date = request.form["date"]
       date = pd.to_datetime(date,format ="%Y-%m-%d").date()
            
       machine = request.form["machine"]
       
       if(machine=="903030"):
            Mcode = 1
            

       elif (machine=="901850"):
            Mcode = 2

       elif (machine=="148-NTX"):
            Mcode = 3
            
       elif (machine=="152-NTX"):
             Mcode = 4
            
       elif (machine=="161-NTX"):
             Mcode = 5
            
       elif (machine=="162-NTX"):
             Mcode = 6

       elif (machine=="169-NZX"):
             Mcode = 7

       elif (machine=="170-NZX"):
             Mcode = 8

       elif (machine=="174-NZX"):
             Mcode = 9

       elif (machine=="186-NTX"):
             Mcode = 10
            
       elif (machine=="187-NTX"):
             Mcode = 11

       elif (machine=="197-NTX"):
             Mcode = 12
             
       elif (machine=="201-NZX"):
            Mcode = 13

       elif (machine=="FF1"):
            Mcode = 14
            
       elif (machine=="IBL-ER004"):
             Mcode = 15

       elif (machine=="IBL-TG008"):
             Mcode = 16
            
       elif (machine=="IBL-TG024"):
             Mcode = 17

       elif (machine=="IBU-ST002"):
             Mcode == 18
             
       elif (machine=="IBU-ST003"):
             Mcode = 19

       elif (machine=="IBU-ST004"):
             Mcode = 20

       elif (machine=="IBU-ST006"):
             Mcode = 21
             
       elif (machine=="IBU-ST007"):
             Mcode = 22  
             
       else:
             Mcode = 23         
       title = 'Machine '+machine+'-'+'Shift '+Shift+'-'+'Downtime Description '+DowntimeDesctiption
       cols_1 = ['date','time_series']
       data = pd.read_excel("C://Users//Naisha Bajaj//Desktop//Deployment//Stryker//converted.xlsx")
       print(data)
       data['Mcode'] = ['Mcode_' + str(i) for i in data['Mcode']]
       data['Shift'] = ['Shift_' + str(i) for i in data['Shift']]
       data['DD'] = ['DD_' + str(i) for i in data['DD']]
       data['time_series'] = data[['Mcode', 'Shift','DD']].apply(lambda x: '_'.join(x), axis=1)
       print(data)
       
       
       Mcode=str(Mcode)
       DD = str(DD)
       time_series = 'Mcode'+'_'+Mcode+'_'+'Shift'+'_'+Shift+'_'+'DD'+'_'+DD
       
       olddata = data[data['time_series'] == time_series] 
       
       print(olddata)
       
       all_dates = pd.date_range(start='2021-06-01', end = '2021-07-31', freq = 'D') 
       score_df = pd.DataFrame() 
       score_df['date'] = all_dates
       score_df['time_series'] = time_series
       print(score_df)
       

       
      
      
       l = load_model('trained_models/' + str(time_series), verbose=False)
       p = predict_model(l, data=score_df)
       final_df = pd.merge(p, data, how = 'left', left_on=['date', 'time_series'], right_on = ['date', 'time_series'])
       print(final_df)
       
      
       output = "{:.2f}".format(p.Label[0])
       
       fig = px.line(final_df,x="date", y=['Label','DowntimeInHours'], title=title , template = 'plotly_dark')
       fig.show() 
       return render_template('home1.html',pred= 'Machine {} on {} in shift {} due to {} state will be down for {} Hrs '.format(machine,date,Shift,DowntimeDesctiption,output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
     if request.method == "POST":
     
       Shift = request.form["Shift"]
       
       DowntimeDesctiption=request.form["DowntimeDesctiption"]
       
       if(DowntimeDesctiption=="ALARM"):
            DD = 1
            
       elif(DowntimeDesctiption=="IDLE"):
            DD = 2
            
       else:
            DD = 3    
            
            
          
       date = request.form["date"]
       date = pd.to_datetime(date,format ="%Y-%m-%d").date()
            
       machine = request.form["machine"]
       
       if(machine=="903030"):
            Mcode = 1
            

       elif (machine=="901850"):
            Mcode = 2

       elif (machine=="148-NTX"):
            Mcode = 3
            
       elif (machine=="152-NTX"):
             Mcode = 4
            
       elif (machine=="161-NTX"):
             Mcode = 5
            
       elif (machine=="162-NTX"):
             Mcode = 6

       elif (machine=="169-NZX"):
             Mcode = 7

       elif (machine=="170-NZX"):
             Mcode = 8

       elif (machine=="174-NZX"):
             Mcode = 9

       elif (machine=="186-NTX"):
             Mcode = 10
            
       elif (machine=="187-NTX"):
             Mcode = 11

       elif (machine=="197-NTX"):
             Mcode = 12
             
       elif (machine=="201-NZX"):
            Mcode = 13

       elif (machine=="FF1"):
            Mcode = 14
            
       elif (machine=="IBL-ER004"):
             Mcode = 15

       elif (machine=="IBL-TG008"):
             Mcode = 16
            
       elif (machine=="IBL-TG024"):
             Mcode = 17

       elif (machine=="IBU-ST002"):
             Mcode == 18
             
       elif (machine=="IBU-ST003"):
             Mcode = 19

       elif (machine=="IBU-ST004"):
             Mcode = 20

       elif (machine=="IBU-ST006"):
             Mcode = 21
             
       elif (machine=="IBU-ST007"):
             Mcode = 22  
             
       else:
             Mcode = 23         
       title = 'Machine '+machine+'-'+'Shift '+Shift+'-'+'Downtime Description '+DowntimeDesctiption
       cols_1 = ['date','time_series']
       data = pd.read_excel("C://Users//Naisha Bajaj//Desktop//Deployment//Stryker//converted.xlsx")
       print(data)
       data['Mcode'] = ['Mcode_' + str(i) for i in data['Mcode']]
       data['Shift'] = ['Shift_' + str(i) for i in data['Shift']]
       data['DD'] = ['DD_' + str(i) for i in data['DD']]
       data['time_series'] = data[['Mcode', 'Shift','DD']].apply(lambda x: '_'.join(x), axis=1)
       print(data)
       
       
       Mcode=str(Mcode)
       DD = str(DD)
       time_series = 'Mcode'+'_'+Mcode+'_'+'Shift'+'_'+Shift+'_'+'DD'+'_'+DD
       
       olddata = data[data['time_series'] == time_series] 
       
       print(olddata)
       
       all_dates = pd.date_range(start='2021-06-01', end = '2021-07-31', freq = 'D') 
       score_df = pd.DataFrame() 
       score_df['date'] = all_dates
       score_df['time_series'] = time_series
       print(score_df)
       

       
      
      
       l = load_model('trained_models/' + str(time_series), verbose=False)
       p = predict_model(l, data=score_df)
       final_df = pd.merge(p, data, how = 'left', left_on=['date', 'time_series'], right_on = ['date', 'time_series'])
       print(final_df)
       
      
       output = "{:.2f}".format(p.Label[0])
       
       fig = px.line(final_df,x="date", y=['Label','DowntimeInHours'], title=title , template = 'plotly_dark')
       fig.show() 
       return render_template('home1.html',pred= 'Machine {} on {} in shift {} due to {} state will be down for {} Hrs '.format(machine,date,Shift,DowntimeDesctiption,output))

if __name__ == "__main__":
 app.run(debug=True)

