from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
# import tensorflow as tf
# import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.graph_objs import *
import json
import plotly
import time 
import sqlite3
import csv
import datetime
from dateutil.parser import parse



app = Flask(__name__)
app.secret_key = 'kapil_shyam_zadpe_L038450'
medicine_type = 'Product1'
selected_medicines = ['RemediMax', 'VitaFlux', 'Vitalisol']
def check_userpass(username, password):
    # # Connect to the SQLite database
    # conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    
    # # Execute the query to check if the username and password are present in the 'userpass' table
    # c.execute("SELECT COUNT(*) FROM userpass WHERE username=? AND password=?", (username, password))
    
    # # Fetch the result of the query
    # result = c.fetchone()[0]
    # # Close the database connection
    # conn.close()
    
    # # Return True if the query result is greater than 0, else return False
    # return True if result > 0 else False
    if username=='kapilshyam.zadpe@lilly.com' and str(password)=='12345678':
        return True
    else:
        return False


# def process_file(file=None):

#     X, y, key_ids, costs = data_preprocess_criteo(file)
#     model_attn = tf.keras.models.load_model('Model/model_attn_weights_c.h5', custom_objects={'CustomAttention':CustomAttention,'XMI_lay':XMI_lay})
#     predictions = attribution_criteo(X, y, costs, model_attn)
#     predictions.to_csv('prediction.csv',index=False)
#     return True

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usercheck = check_userpass(username,password)
        if usercheck:
            session['username'] = username
            return redirect(url_for('pie_chart'))
        else:
            error = 'Please Check Your Credentials'
            return render_template('login.html', error=error)
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        error = 'Session expired, Please Login again!'
        return render_template('login.html', error=error)
        # return redirect(url_for('login'))

    elif request.method == 'POST':
        global medicine_type
        # selected_medicines = request.form['medicine_type']
        global selected_medicines
        selected_medicines = request.form.getlist('medicine_type')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        region = '(' + str(request.form.getlist('region'))[1:-1] + ')'
        user_type = '(' + str(request.form.getlist('user_type'))[1:-1] + ')'

        ##### write logic to get data from database or forecasting model
        tempppp = pd.read_csv('final_results.csv')
        
        # Convert 'Date' column to datetime format
        global filtered_data
        tempppp['date'] = pd.to_datetime(tempppp['date'], dayfirst=True)
        tempppp['date'] = tempppp['date'].dt.strftime('%Y-%m-%d')
        filtered_data = tempppp[(tempppp['date'] >= start_date) & (tempppp['date'] <= end_date)]
        filtered_data.to_csv('temp_data.csv', index=False)

        return render_template('forecast.html', selected_medicines=selected_medicines)

    elif request.method == 'GET':
        return render_template('home.html', error=None)
    return render_template('home.html', error=None)

@app.route('/requestt', methods=['GET', 'POST'])
def requestt():    
    return render_template('requestt.html')

@app.route('/pie_chart')
def pie_chart():
    if 'username' not in session:
        error = 'Session expired, Please Login again!'
        return render_template('login.html', error=error)
        # return redirect(url_for('login'))
    return render_template('pie_chart.html')

@app.route('/descp')
def descp():
    if 'username' not in session:
        error = 'Session expired, Please Login again!'
        return render_template('login.html', error=error)
        # return redirect(url_for('login'))
    return render_template('descp.html')

@app.route('/descp2')
def descp2():
    if 'username' not in session:
        error = 'Session expired, Please Login again!'
        return render_template('login.html', error=error)
        # return redirect(url_for('login'))
    return render_template('descp2.html')

@app.route('/download')
def download_file():
    # Get the path to the file you want to download
    file_path = 'temp_data.csv'
    # Return the file for download using the send_file() function
    return send_file(file_path, as_attachment=True)


#######################################################################################################################
@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    
    if 'username' not in session:
        error = 'Session expired, Please Login again!'
        return render_template('login.html', error=error)

    if request.method == 'POST':
        selected_variable = request.form.get('variable')
        selected_model = request.form.get('model')
        filtered_data_temp =  filtered_data[(filtered_data.variable == selected_variable) & ( filtered_data.model == selected_model)]

        dates           = filtered_data_temp.date
        actual_values   = filtered_data_temp.actual
        actual_values   = []
        forecast_values = filtered_data_temp.forecast

        actual_values = [float(i) for i in actual_values]
        forecast_values = [float(i) for i in forecast_values]
        # dates = [parse(date) for date in dates]

        # Create the plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=actual_values, mode='lines+markers', name='Actual'))
        fig.add_trace(go.Scatter(x=dates, y=forecast_values, mode='lines+markers', name='Forecast'))
        fig.update_layout(title=f'{selected_variable} Forecast Using- {selected_model} ',
                        xaxis_title='Date',
                        yaxis_title='Value')
                        # xaxis_tickangle=-45 ) # Adjust the angle here)
        graphJSON = fig.to_json()

        return render_template('forecast.html', graphJSON=graphJSON, data=filtered_data_temp.to_dict('records'), selected_medicines=selected_medicines)
    return render_template('forecast.html', selected_medicines=selected_medicines)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True ,port=5001)