from flask import Flask, render_template, request, render_template_string, send_file
import pickle
import pandas as pd
import numpy as np




app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/chart")
def chart():
    date = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    load = [0, 10, 5, 2, 20, 30, 45]

    prediction = pd.DataFrame(date, columns=['ds'])
    prediction['yhat'] = load

    label = prediction['ds'].values
    data = prediction['yhat'].values

    tup = [
            (prediction['ds'].iloc[0], prediction['yhat'].iloc[0]),
            (prediction['ds'].iloc[1], prediction['yhat'].iloc[1])
          ]       
    labels = [row[0] for row in tup]
    values = [row[1] for row in tup]

    return render_template('chart.html',  label=labels, data=values)

@app.route("/contact")
def contact():
    
    return render_template('contact.html')  

 


@app.route('/predict',methods=['POST'])
def predict():
    #date = request.form.values()
    #date = request.args.get('date')
    
    date = request.form["Date"]
    temperature = request.form["Temperature"]
    humidity = request.form["Humidity"]
    weather = request.form["Weather"]

    summer = {
    "clouds" : 200,
    "clear" : 300,
    "rain" : 150
    }

    winter = {
    "clouds" : 200,
    "clear" : 300,
    "rain" : 150
    }

    rainy = {
    "clouds" : 200,
    "clear" : 300,
    "rain" : 150
    }

    #Processing the month and temperature sensitivity
    new = ""
    for n in np.arange(5,7):  #used to find the month
        new = new + str(date[n])

    new1 = ""   #used to find date
    for n in np.arange(8,10):
        new1 = new1 + str(date[n])

    temp = {
    '01' : 2.13,
    '02' : 4.96,
    '03' : 17.03,
    '05' : 36.6,
    '06' : 53.14,
    '07' : 39.76,
    '08' : 37.22,
    '09' : 22.37,
    '10' : 16.00,
    '11' : 5.65,
    '12' : 4.94
    }   


    rh = {
    '01' : 0.205,
    '02' : 0.180,
    '03' : -0.274,
    '04' : -0.249,
    '05' : -0.353,
    '06' : 0.089,
    '07' : 0.363,
    '08' : 0.454,
    '09' : 0.461,
    '10' : -0.055,
    '11' : 0.118,
    '12' : 0.098
    }   



    offset=["01:00:00","02:00:00","03:00:00","04:00:00","05:00:00","06:00:00","07:00:00","08:00:00","09:00:00"
       ,"10:00:00","11:00:00","12:00:00","13:00:00","14:00:00","15:00:00","16:00:00","17:00:00","18:00:00", "19:00:00"
       ,"20:00:00","21:00:00","22:00:00","23:00:00"]

    str_array = []

    for item in offset:
        new_str = date + " " + item
        str_array.append(new_str)

    custom_df = pd.DataFrame(str_array, columns=['ds'])

    #custom = {
        #'ds' : date     
    #}
    #custom_df = pd.DataFrame(custom)


    #custom_df = pd.DataFrame({'ds' : [date] })

    custom_df['ds'] = pd.to_datetime(custom_df['ds'], format='%Y-%m-%d', utc=True)
    custom_df['ds'] = custom_df['ds'].dt.strftime('%Y-%m-%d %H:%M:%S')

    prediction = model.predict(custom_df)
    #prediction = model.predict(date)

    new_pred = pd.DataFrame()
    new_pred['Date'] = prediction['ds']
    new_pred['Pred Load'] = prediction['yhat']

    
    
    prediction.to_csv('table.csv')
    new_pred.to_html("templates/output_table.html")

    output = prediction['yhat'].values
    #output = round(prediction[0], 2)

    for n in temp:
        if(n==new):
            addon = temp[n] * abs(int(temperature) - 20)
            prediction['yhat'] += addon

    for n in rh:
        if(n==new):
            addon1 = rh[n] * abs(int(humidity))
            prediction['yhat'] += addon1        

    new = int(new)   #convert month into int dtype
    new1 = int(new1) #convert day into int dtype

    if(new>=3 & new<=6):
        for n in summer:
            if(n==weather):
                prediction['yhat'] += summer[n]

    if(new==11 or new==12 or new==1):
        for n in winter:
            if(n==weather):
                prediction['yhat'] += winter[n]

    if(new>=7 & new<=9):
        for n in rainy:
             if(n==weather):
                prediction['yhat'] += rainy[n]

    if(new==3):    #las fellas
        if(new1>=15 and new1<=19):
            prediction['yhat'] += 200
                
    if(new==7):    #july fair
        prediction['yhat']+=200

    if(new==10):    #national day
        if(new1==9):
            prediction['yhat'] += 150

    if(new==5):     #lady of foresaken
        if(new1>=11 and new1<=12):
            prediction['yhat']+=50

    if(new==4):     #easter holy festival
        if(new1>=5 and new1<=11):
            prediction['yhat'] += 70

    dic = {
    "date" : prediction['ds'] , 
    "load" : prediction['yhat']
    }   

    prediction['yhat'] = round(prediction['yhat'], 2)

    tup = (
    (prediction['ds'].iloc[0] , prediction['yhat'].iloc[0]),
    (prediction['ds'].iloc[1] , prediction['yhat'].iloc[1]),
    (prediction['ds'].iloc[2] , prediction['yhat'].iloc[2]),
    (prediction['ds'].iloc[3] , prediction['yhat'].iloc[3]),
    (prediction['ds'].iloc[4] , prediction['yhat'].iloc[4]),
    (prediction['ds'].iloc[5] , prediction['yhat'].iloc[5]),
    (prediction['ds'].iloc[6] , prediction['yhat'].iloc[6]),
    (prediction['ds'].iloc[7] , prediction['yhat'].iloc[7]),
    (prediction['ds'].iloc[8] , prediction['yhat'].iloc[8]),
    (prediction['ds'].iloc[9] , prediction['yhat'].iloc[9]),
    (prediction['ds'].iloc[10] , prediction['yhat'].iloc[10]),
    (prediction['ds'].iloc[11] , prediction['yhat'].iloc[11]),
    (prediction['ds'].iloc[12] , prediction['yhat'].iloc[12]),
    (prediction['ds'].iloc[13] , prediction['yhat'].iloc[13]),
    (prediction['ds'].iloc[14] , prediction['yhat'].iloc[14]),
    (prediction['ds'].iloc[15] , prediction['yhat'].iloc[15]),
    (prediction['ds'].iloc[16] , prediction['yhat'].iloc[16]),
    (prediction['ds'].iloc[17] , prediction['yhat'].iloc[17]),
    (prediction['ds'].iloc[18] , prediction['yhat'].iloc[18]),
    (prediction['ds'].iloc[19] , prediction['yhat'].iloc[19]),
    (prediction['ds'].iloc[20] , prediction['yhat'].iloc[20]),
    (prediction['ds'].iloc[21] , prediction['yhat'].iloc[21]),
    (prediction['ds'].iloc[22] , prediction['yhat'].iloc[22])
    
    )

    
    

    labels = [row[0] for row in tup]
    values = [row[1] for row in tup]
           
    legend = 'Daily Load'
    labels = prediction['ds'].values
    values = prediction['yhat'].values
    return render_template('results.html', values=values, labels=str_array, legend=legend, tup=tup, date=date)
    
    
    #return render_template('index.html', prediction_text = 'Load Prediction for the date is {}'.format(output))

    #return render_template('chartist.html', tup=tup)


if __name__ == "__main__":
    app.run(debug=True)