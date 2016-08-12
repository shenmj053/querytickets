# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import requests
from stations import stations
app = Flask(__name__)


name = [
    'station_train_code',
    'from_station_name',
    'to_station_name',
    'lishi',
    'start_time',
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


@app.route('/zd')
def zd_tickets():
    tickets = []
    date = request.args.get('Date')
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.\
        format(date, from_station, to_station)

    r = requests.get(url, verify=False)
    contents = r.json()['data']['datas']

    for content in contents:
        ticket = {key: content[key] for key in name}
        tickets.append(ticket)

    return jsonify(tickets)


@app.route('/hc')
def hc_tickets():
    tickets_1 = []
    tickets_2 = []
    date = request.args.get('Date')
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    changed_station = request.args.get('change')
    url1 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'. \
        format(date, from_station, changed_station)

    r1 = requests.get(url1, verify=False)
    contents_1 = r1.json()['data']['datas']
    for content in contents_1:
        ticket = {key: content[key] for key in name}
        tickets_1.append(ticket)

    for ticket in tickets_1:
        # TODO
        if int(ticket['lishi'][:2]) + int(ticket['start_time'][:2]) < 24:
            url2 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT' \
                   '&queryDate={}&from_station={}&to_station={}'. \
                format(date, changed_station, to_station)
            r2 = requests.get(url2, verify=False)
            contents_2 = r2.json()['data']['datas']

            for content in contents_2:
                ticket = {key: content[key] for key in name}
                tickets_2.append(ticket)

            for x in tickets_1:
                x['changed_ticket'] = [y for y in tickets_2 if
                                       1 < int(y['start_time'][:2]) - int(x['arrive_time'][:2]) < 3]

        else:
            date2 = str(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1))[:10]
            url2 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT' \
                   '&queryDate={}&from_station={}&to_station={}'. \
                format(date2, changed_station, to_station)

            r2 = requests.get(url2, verify=False)
            contents_2 = r2.json()['data']['datas']

            for content in contents_2:
                ticket = {key: content[key] for key in name}
                tickets_2.append(ticket)

            for x in tickets_1:
                x['changed_ticket'] = [y for y in tickets_2 if
                                       1 < int(y['start_time'][:2]) - int(x['arrive_time'][:2]) < 3]

    return jsonify(tickets_1)



if __name__ == '__main__':
    app.run(debug=True)


    



















