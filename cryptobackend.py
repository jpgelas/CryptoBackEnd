#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A simple python backend providing json data to the frontend apps to build
    charts from a datalog file.

    datalog file format
    YYYY-MM-DD HH:MM:SS     BTC      USD 
    ---------- -------- ---------- -------
    2018-10-20 17:40:04 0.16232310 1066.61
    2018-10-20 17:50:04 0.16230383 1067.48
    2018-10-20 18:00:04 0.16224205 1066.69

"""

from flask import Flask, jsonify
import os
import utils

DATALOG_FILENAME = 'PATH_TO/LOG_FILE.LOG' 

app = Flask(__name__)
app.debug = False

USAGE_STRING = "Usage : /[24h|7d|1m|all|last|contact]"
EMAIL_CONTACT = "name@domain.tld"

@app.route("/cryptoback/")
def page_index():
    return USAGE_STRING

@app.route("/cryptoback/contact/", methods=['GET'])
def page_contact():
    data = {}
    data['email'] = EMAIL_CONTACT
    return jsonify(data)

@app.route("/cryptoback/last/", methods=['GET'])
def last_value(): 
    raw_data = utils.readLastLine(DATALOG_FILENAME)
    data = {}
    e = raw_data.replace("\n","").split(' ')
    data['timestamp'] = e[0] + " " + e[1]
    data['btc'] = e[2]
    data['usd'] = e[3]
    return jsonify(data)

@app.route("/cryptoback/24/")
@app.route("/cryptoback/24h/")
def send_24h_data():
    raw_data = utils.tail(DATALOG_FILENAME, 144)
    data = {}
    dataBTC, dataUSD, data['labels'] = [],[],[]
    for line in raw_data:
        e = line.split(' ')
        data['labels'].append(e[1]) # HH:MM:SS field
        dataBTC.append(float(e[2])) # BTC field  
        dataUSD.append(float(e[3])) # USD field  

    dicBTC = {
        'label': 'BTC',
        'yAxisID': 'BTC',
        'data': dataBTC,
        }
    dicUSD = {
        'label': 'USD',
        'yAxisID': 'USD',
        'data': dataUSD,
        }
    data['datasets'] = [ dicBTC, dicUSD ] 
    #return jsonify(utils.data_test)
    return jsonify(data)

@app.route("/cryptoback/7/")
@app.route("/cryptoback/7d/")
def send_7d_data():
    raw_data = utils.tail(DATALOG_FILENAME, 7 * 144)
    data = {}
    counter = 0
    dataBTC, dataUSD, data['labels'] = [],[],[]
    for line in raw_data:
        counter += 1
        if (counter % 7 == 0):
            e = line.split(' ')
            data['labels'].append(e[0] + " "+ e[1]) # YYYY-MM-DD field
            dataBTC.append(float(e[2])) # BTC field  
            dataUSD.append(float(e[3])) # USD field  

    dicBTC = {
        'label': 'BTC',
        'yAxisID': 'BTC',
        'data': dataBTC
        }
    dicUSD = {
        'label': 'USD',
        'yAxisID': 'USD',
        'data': dataUSD
        }
    data['datasets'] = [ dicBTC, dicUSD ] 
    return jsonify(data)

@app.route("/cryptoback/1/")
@app.route("/cryptoback/1m/")
def send_1m_data():
    raw_data = utils.tail(DATALOG_FILENAME, 4 * 7 * 144)
    data = {}
    counter = 0
    dataBTC, dataUSD, data['labels'] = [],[],[]
    for line in raw_data:
        counter += 1
        if (counter % 28 == 0):
            e = line.split(' ')
            data['labels'].append(e[0]) # YYYY-MM-DD field
            dataBTC.append(float(e[2])) # BTC field  
            dataUSD.append(float(e[3])) # USD field  

    dicBTC = {
        'label': 'BTC',
        'yAxisID': 'BTC',
        'data': dataBTC
        }
    dicUSD = {
        'label': 'USD',
        'yAxisID': 'USD',
        'data': dataUSD
        }
    data['datasets'] = [ dicBTC, dicUSD ] 
    return jsonify(data)

@app.route("/cryptoback/all/")
def send_all_data():
    raw_data = utils.readOneLineOverN(DATALOG_FILENAME, 200)
    data = {}
    counter = 0
    dataBTC, dataUSD, data['labels'] = [],[],[]
    for line in raw_data:
            e = line.split(' ')
            data['labels'].append(e[0]) # YYYY-MM-DD field
            dataBTC.append(float(e[2])) # BTC field  
            dataUSD.append(float(e[3])) # USD field  

    dicBTC = {
        'label': 'BTC',
        'yAxisID': 'BTC',
        'data': dataBTC
        }
    dicUSD = {
        'label': 'USD',
        'yAxisID': 'USD',
        'data': dataUSD
        }
    data['datasets'] = [ dicBTC, dicUSD ] 
    return jsonify(data)


@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def page_error(error):
    return "Error {}".format(error.code), error.code



if __name__ == "__main__":
    app.run(host='127.0.0.1')

