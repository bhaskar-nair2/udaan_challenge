from flask import Flask, request, render_template, redirect
from slaves import Mongo

app = Flask("__name__")
mongo = Mongo(app)


# This is the page for all the routing

@app.route('/', methods=['GET'])
def home():
    return render_template('res.html')


# TODO: Q1- API to accept details of a movie screen.
@app.route('/screens', methods=['POST'])
def screen():
    return mongo.new_sc(request.json)


# TODO: Q2. API to reserve tickets for given seats in a given screen
@app.route('/screens/<string:screen_name>/reserve', methods=['POST'])
def reserve(screen_name):
    return mongo.res(screen_name, request.json['seats'])


# TODO: Q3. API to get the available seats for a given screen
@app.route('/screens/<string:screen_name>/unreserved', methods=['GET'])
def unreserved(screen_name):
    return mongo(screen_name)


# TODO: Q4. API to get information of available tickets at a given position
@app.route('/screens/<string:screen_name>/numSeats=<int:x>&choice=<seat_row_number>', methods=['GET'])
def seat_stat(screen_name, x, seat_row_number):
    return mongo.suggest_seats(screen_name, x, seat_row_number)


if __name__ == '__main__':
    app.run(port=9090)
