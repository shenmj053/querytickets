# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response, abort
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
    if from_station in stations.keys() and to_station in stations.keys():
        from_station = stations[from_station]
        to_station = stations[to_station]
    else:
        abort(400)

    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.\
        format(date, from_station, to_station)
    r = requests.get(url, verify=False)
    # if the url param 'date'was supplied incorrectly, 12306 would return -1 of int type.
    if r.json() == -1:
        abort(400)
    if 'datas' in r.json()['data']:
        contents = r.json()['data']['datas']

        # get out the information that we want in the contents dict.
        for content in contents:
            ticket = {key: content[key] for key in name}
            tickets.append(ticket)
    else:
        abort(404)

    return jsonify({'tickets': tickets})


@app.route('/hc')
def hc_tickets():
    tickets_1 = []
    tickets_2 = []
    date = request.args.get('Date')
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    changed_station = request.args.get('change')
    if from_station in stations.keys() and to_station in stations.keys() and changed_station in stations.keys():
        from_station = stations[from_station]
        to_station = stations[to_station]
        changed_station = stations[changed_station]
    else:
        abort(400)

    url1 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'. \
        format(date, from_station, changed_station)
    r1 = requests.get(url1, verify=False)

    if r1.json() == -1:
        abort(400)

    if 'datas' in r1.json()['data']:
        contents_1 = r1.json()['data']['datas']

        for content in contents_1:
            ticket = {key: content[key] for key in name}
            tickets_1.append(ticket)
    else:
        abort(404)

    for ticket in tickets_1:
        if int(ticket['lishi'][:2]) + int(ticket['start_time'][:2]) < 24:  # TODO
            url2 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT' \
                   '&queryDate={}&from_station={}&to_station={}'. \
                format(date, changed_station, to_station)
            r2 = requests.get(url2, verify=False)

            if r2.json() == -1:
                abort(400)

            if 'datas' in r2.json()['data']:
                contents_2 = r2.json()['data']['datas']

                for content in contents_2:
                    ticket = {key: content[key] for key in name}
                    tickets_2.append(ticket)

                if tickets_2:
                    for x in tickets_1:
                        x['changed_ticket'] = [y for y in tickets_2 if
                                               1 < int(y['start_time'][:2]) - int(x['arrive_time'][:2]) < 3]
            else:
                abort(404)

        else:
            # if the first train arrived at next day, we add one day to the queryDate param.
            date2 = str(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1))[:10]

            # TODO: the following repeatedly codes should be moved to a helper method.
            url2 = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT' \
                   '&queryDate={}&from_station={}&to_station={}'. \
                format(date2, changed_station, to_station)
            r2 = requests.get(url2, verify=False)

            if r2.json() == -1:
                abort(400)

            if 'datas' in r2.json()['data']:
                contents_2 = r2.json()['data']['datas']

                for content in contents_2:
                    ticket = {key: content[key] for key in name}
                    tickets_2.append(ticket)

                if tickets_2:
                    for x in tickets_1:
                        x['changed_ticket'] = [y for y in tickets_2 if
                                           1 < int(y['start_time'][:2]) - int(x['arrive_time'][:2]) < 3]

    return jsonify({'tickets': tickets_1})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Please check your query param format'}), 400)


if __name__ == '__main__':
    app.run(debug=True)


    




















