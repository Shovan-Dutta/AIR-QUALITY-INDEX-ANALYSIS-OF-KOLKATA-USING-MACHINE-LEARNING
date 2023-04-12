import pandas as pd
import time
import numpy as np
import math
import argparse

##1. PM2.5 Sub-Index calculation
def PM25(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 30:
        return x * 50 / 30
    elif x <= 60:
        return 50 + (x - 30) * 50 / 30
    elif x <= 90:
        return 100 + (x - 60) * 100 / 30
    elif x <= 120:
        return 200 + (x - 90) * 100 / 30
    elif x <= 250:
        return 300 + (x - 120) * 100 / 130
    elif x > 250:
        return 400 + (x - 250) * 100 / 130
    else:
        return 0

##2. PM10 Sub-Index calculation
def PM10(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 50:
        return x
    elif x <= 100:
        return x
    elif x <= 250:
        return 100 + (x - 100) * 100 / 150
    elif x <= 350:
        return 200 + (x - 250)
    elif x <= 430:
        return 300 + (x - 350) * 100 / 80
    elif x > 430:
        return 400 + (x - 430) * 100 / 80
    else:
        return 0

##3. NO2 Sub-Index calculation
def NO2(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 180:
        return 100 + (x - 80) * 100 / 100
    elif x <= 280:
        return 200 + (x - 180) * 100 / 100
    elif x <= 400:
        return 300 + (x - 280) * 100 / 120
    elif x > 400:
        return 400 + (x - 400) * 100 / 120
    else:
        return 0


##4. NH3 Sub-Index calculation
def NH3(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 200:
        return x * 50 / 200
    elif x <= 400:
        return 50 + (x - 200) * 50 / 200
    elif x <= 800:
        return 100 + (x - 400) * 100 / 400
    elif x <= 1200:
        return 200 + (x - 800) * 100 / 400
    elif x <= 1800:
        return 300 + (x - 1200) * 100 / 600
    elif x > 1800:
        return 400 + (x - 1800) * 100 / 600
    else:
        return 0

##5. SO2 Sub-Index calculation
def SO2(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 380:
        return 100 + (x - 80) * 100 / 300
    elif x <= 800:
        return 200 + (x - 380) * 100 / 420
    elif x <= 1600:
        return 300 + (x - 800) * 100 / 800
    elif x > 1600:
        return 400 + (x - 1600) * 100 / 800
    else:
        return 0

##6. CO Sub-Index calculation
def CO(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 1:
        return x * 50 / 1
    elif x <= 2:
        return 50 + (x - 1) * 50 / 1
    elif x <= 10:
        return 100 + (x - 2) * 100 / 8
    elif x <= 17:
        return 200 + (x - 10) * 100 / 7
    elif x <= 34:
        return 300 + (x - 17) * 100 / 17
    elif x > 34:
        return 400 + (x - 34) * 100 / 17
    else:
        return 0

##7. O3 Sub-Index calculation
def O3(x):
    if x == "" or x == "NA" or x == "None":
        return 0
    x = float(x)
    
    if x <= 50:
        return x * 50 / 50
    elif x <= 100:
        return 50 + (x - 50) * 50 / 50
    elif x <= 168:
        return 100 + (x - 100) * 100 / 68
    elif x <= 208:
        return 200 + (x - 168) * 100 / 40
    elif x <= 748:
        return 300 + (x - 208) * 100 / 539
    elif x > 748:
        return 400 + (x - 400) * 100 / 539
    else:
        return 0
    
def aqi(l):
    final = max(PM25(l[0]),PM10(l[1]),NO2(l[2]),NH3(l[3]),SO2(l[4]),CO(l[5]),O3(l[6]))
    if final >=0 and final<=50:
        return([round(final,2),"Good"])
    elif final>50 and final<=100:
        return([round(final,2),"Satisfactory"])
    elif final>100 and final<= 200:
        return([round(final,2),"Moderately Polluted"])
    elif final>200 and final<=300:
        return([round(final,2),"Poor"])
    elif final>300 and final<=400:
        return([round(final,2),"Very poor"])
    elif final>400:
        return([round(final,2),"Severe"])

#this function extracts data from the downloaded excel data_set to proper csv format for further procssing
def csv_creator(file_name):
    newData = pd.read_excel(file_name) # read the excel file

    parameters = newData.loc[newData["CENTRAL POLLUTION CONTROL BOARD"] =="From Date"]   # Here we find the attrubutes
    unique_parameters =["Date"]
    for i in parameters.drop('CENTRAL POLLUTION CONTROL BOARD', axis=1).drop('Unnamed: 1', axis=1).columns:
        unique_parameters.append(parameters[i].unique()[0])
    for i in parameters.drop('CENTRAL POLLUTION CONTROL BOARD', axis=1).drop('Unnamed: 1', axis=1).columns:
        unique_parameters.append(parameters[i].unique()[1])
    unique_parameters = [item for item in unique_parameters if not(pd.isnull(item)) == True]

    data = {}
    for i in unique_parameters:
        data[i]=[]

    for i in newData["CENTRAL POLLUTION CONTROL BOARD"][16:].unique():          #here we properly extract and format our data
        try:
            time.strptime(str(i[:10]), '%d-%m-%Y')
        except :
            pass
        else:
            data["Date"].append(i[:10])
            temp = newData.loc[newData["CENTRAL POLLUTION CONTROL BOARD"] ==i]
            data["PM2.5"].append(list(temp["Unnamed: 2"])[0])
            data["PM10"].append(list(temp["Unnamed: 3"])[0])
            data["NO2"].append(list(temp["Unnamed: 4"])[0])
            data["NH3"].append(list(temp["Unnamed: 5"])[0])
            data["SO2"].append(list(temp["Unnamed: 6"])[0])
            data["CO"].append(list(temp["Unnamed: 2"])[1])
            data["Ozone"].append(list(temp["Unnamed: 3"])[1])
            data["AT"].append(list(temp["Unnamed: 4"])[1])

    data = pd.DataFrame.from_dict(data)
    return(data)

# this function fills the missing values with average of the nearest two records.
def missing_controller(list1):
    a=0
    b=0
    for i in range(len(list1)):
        y=i
        if math.isnan(list1[y]):
            if (y-1) != -1:
                a=list1[y-1]
            else:
                while True:
                    y=y+1
                    a=list1[y]
                    if math.isnan(a) == False:
                        break
            if y == i:
                if y<(len(list1)-1):
                    while True:
                        y=y+1
                        b = list1[y]
                        if math.isnan(b) == False:
                            break
                else:
                    b = list1[y-2]
            else:
                if y<(len(list1)-1):
                    while True:
                        y=y+1
                        b = list1[y]
                        if math.isnan(b) == False:
                            if b!=a:
                                break
                else:
                    b = list1[y-2]
            #print(a,b)
            list1[i] = round((a+b)/2,2)
    return(list1)

def process(name,in_path,out_path):
    stand = [] # to store the AQI standard
    aqi_val = [] # to store the exact AQI value
    print("######################## Processing for ",name," ########################")
    rpath = in_path+name+'.xlsx'
    data = csv_creator(rpath)    # reads the csv file
    data = data.replace('None',np.nan) # replaces the 'None' string to null
    data_temp = data.drop('Date', axis=1).astype(float) # converts all the values to float except date
    data['Date'] = pd.to_datetime(data['Date'], format="%d-%m-%Y") # converts the date vales to proper date format from string
    
    for col in data.drop('Date', axis=1).columns:
        data[col]=data_temp[col]
    print("**Before handeling missing data:-\n",data.head())

    for x in list(data.drop('Date', axis=1).columns.values) : # replaces all the null values by the column's average
        data[x] = missing_controller(list(data[x]))
    data_temp = data.drop('Date', axis=1).drop('AT', axis=1)

    for i in range(data_temp.shape[0]): # now calculating the aqi value & aqi class for each day and adding the data as separate column
        report = aqi(list(data_temp.loc[i,:]))
        aqi_val.append(report[0])
        stand.append(report[1])
    data['AQI'] = aqi_val
    data['AQI_Standard'] = stand
    wpath = out_path+name[:-8]+'.csv'
    data.to_csv(wpath,index=False) # Now properly writing the fairly preprocessed data
    print("\n**After handeling missing data:-\n",data.head())


# settingup the parser
parser = argparse.ArgumentParser(description="Toolkit for preprocessing the dataset")
parser.add_argument("--in_path", type=str,default = "C:/Users/shova/iCloudDrive/Kolkata_data/Work/Sitewise_original/",help="Get input path of .xlsx files")
parser.add_argument("--out_path", type=str,default = "C:/Users/shova/iCloudDrive/Kolkata_data/Work/Semi_processed/",help="Get output path of .csv files")
args = parser.parse_args()
files = ['Ballygunge_Kolkata','Bidhannagar_Kolkata','Fort_william_Kolkata','Jadavpur_Kolkata','Rabindra_Bharati_University_Kolkata','Rabindra_Sarobar_Kolkata','Victoria_Kolkata']
for name in files:
    process(name,args.in_path,args.out_path)