from flask import make_response, jsonify
from flask_pymongo import PyMongo
import json


class Mongo:
    def __init__(self, app):
        URI = 'mongodb://127.0.0.1:27017/udaan'
        self.mongo = PyMongo(app, URI)
        self.client = self.mongo.db['udaan.screens']

    # TODO: A1. New Screen
    def new_sc(self, data):
        if self.client.find_one({"name": data['name']}) is None:
            data['res_info'] = {}
            self.client.insert_one(data)
            res = make_response('New Screen Added')
            res.status_code = 201
            return res
        else:
            res = make_response('The screen name already exists')
            res.status_code = 409
            return res

    # TODO: A3. Available Seats
    def __call__(self, scr_name):
        try:
            data = self.client.find_one({"name": scr_name})
            avail = data['seatInfo']  # AVAIlAble Keys
            resed = data['res_info']  # reserveed keys
            rows = []
            for _ in avail:
                try:
                    rows.append({_: set([x for x in range(avail[_]['numberOfSeats'])]).difference(resed[_])})
                except KeyError:
                    rows.append({_: set([x for x in range(avail[_]['numberOfSeats'])])})
            resp = make_response(json.dumps({"seats": rows}, cls=SetEncoder))
            resp.status_code = 200
            return resp

        except KeyError:
            return self.client.find_one({'name': scr_name})
        except TypeError:
            return 'No Such Screen'

    # TODO: A2. Reserve tickets
    def res(self, scr_name, demand):
        try:
            avail = self.client.find_one({'name': scr_name})['seatInfo']  # AVAIlAble Keys
            resed = self.client.find_one({'name': scr_name})['res_info']  # reserveed keys
            if len(set(demand).intersection(avail)) != len(demand):
                res = make_response('The rows are not there in the screen')
                res.status_code = 403
                return res
            flag = ''
            keys = set([x for x in demand]).intersection([x for x in resed])
            for row in keys:
                if set(demand[row]).intersection(resed[row]) != set():
                    flag += "Requested Seats {} in row {} are taken\n".format(set(demand[row]).intersection(resed[row]),
                                                                              row)  # (demand[row])

            if flag is '':
                for _ in demand:
                    self.client.find_one_and_update({'name': scr_name},
                                                    {'$push': {'res_info.{}'.format(_): {"$each": demand[_]}}})
                res = make_response('Seats {} booked'.format(demand))
                res.status_code = 200
                return res
            else:
                return flag
        except KeyError:
            self.client.find_one_and_update({'name': scr_name}, {'$set': {'res_info': demand}})
            res = make_response('Seats {} booked'.format(demand))
            res.status_code = 200
            return res

        except TypeError:
            res = make_response('No Such Screen')
            res.status_code = 403
            return res

    # TODO: A4. That suggestion function
    # TODO: BAM BAM BAM!!!
    def suggest_seats(self, scr_name, seat_count, choice):
        data = self.client.find_one({"name": scr_name})
        key, val = choice[0], choice[1]
        row_seats = list(set([x for x in range(data['seatInfo'][key]['numberOfSeats'])]))
        try:
            avail_seats = list(set([x for x in range(data['seatInfo'][key]['numberOfSeats'])]).difference(
                data['res_info'][key]))
        except KeyError:
            avail_seats = list(set([x for x in range(data['seatInfo'][key]['numberOfSeats'])]))
        aisle = (data['seatInfo'][key]['aisleSeats'])
        aisle.sort()
        seats = []
        for _ in range(0, len(aisle), 2):
            if int(val) in row_seats[aisle[_]:aisle[_ + 1] + 1]:
                seats = row_seats[aisle[_]:aisle[_ + 1] + 1]
        seats = list(set(seats).intersection(avail_seats))
        # print("Seats count=", seats)
        if len(seats) < seat_count:
            resp = make_response('Not enough Seats Available')
            resp.status_code = 301  # This is a pun,
            return resp
        else:
            ind = seats.index(int(val))
            if (ind - seat_count + 1) > 0:
                min_in = ind - seat_count + 1
            else:
                min_in = 0

            if (ind + seat_count - 1) < len(seats):
                max_in = ind + seat_count
            else:
                max_in = len(seats)
            inc = min_in + seat_count - 1
            suggest = []
            for _ in range(0, seat_count):
                # suggest.append(seats[min_in: inc + 1])
                # print(ind, min_in, inc, max_in)
                suggest.append(seats[min_in: inc + 1])
                min_in += 1
                inc = min_in + seat_count - 1
                if min_in > ind or inc + 1 > max_in:
                    break

        # return ''
        return jsonify({"availableSeats": {key: suggest}})


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
