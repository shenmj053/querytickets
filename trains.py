# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
import json
from stations import stations
app = Flask(__name__)


name = [
    'station_train_code',
    'from_station_name',
    'to_station_name',
    'lishi',
    'arrive_time',
    'swz_num',
    'tz_num',
    'zy_num',
    'ze_num',
    'gr_num',
    'rw_num',
    'yw_num',
    'rz_num',
    'yz_num',
    'wz_num',
    'qt_num']


@app.route('/')
def tickets():
    tickets = []
    date = request.args.get('queryDate')
    from_station = request.args.get('from_station')
    to_station = request.args.get('to_station')
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station)

    r = requests.get(url, verify=False)
    contents = r.json()['data']['datas']

    for content in contents:
        ticket = [(key, content[key]) for key in name]
        tickets.append(ticket)

    return jsonify(tickets)


if __name__ == '__main__':
    app.run(debug=True)


# curl http://localhost:5000?purpose_codes=ADULT&queryDate=2016-08-13&from_station=BJP&to_station=CQW

    




















