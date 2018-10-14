from flask import Flask, request, render_template
from slaves import Mongo

app = Flask("__name__")
mongo = Mongo(app)


@app.route('/screens', methods=['POST', 'GET'])
def screen():
    if request.method == 'POST':
        return mongo.new_sc(request.json)
    else:
        return render_template('')


@app.route('/screens/<string:screen_name>/reserve', methods=['POST'])
def reserve(screen_name):
    return mongo.res(screen_name, request.json['seats'])


@app.route('/screens/<string:screen_name>/unreserved', methods=['GET'])
def unreserved(screen_name):
    return mongo(screen_name)


@app.route('/screens/<string:screen_name>/numSeats=<int:x>&choice=<seat_row_number>', methods=['GET'])
def seat_stat(screen_name, x, seat_row_number):
    return mongo.suggest_seats(screen_name, x, seat_row_number)


if __name__ == '__main__':
    app.run(port=9090, debug=True)
