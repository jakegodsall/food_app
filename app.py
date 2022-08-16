from flask import Flask, render_template, g, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

app.config["DEBUG"] = True

def connect_db():
    sql = sqlite3.connect('food_log.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlit3_db.close()


@app.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date'] # assuming the date is in YYYY-MM-DD format
        dt = datetime.fromisoformat(date)
        database_date = datetime.strftime(dt, '%Y%m%d')

        db.execute('INSERT INTO log_date (entry_date) VALUES (?)', [database_date])
        db.commit()

    cur = db.execute('SELECT entry_date FROM log_date ORDER BY entry_date DESC')
    results = cur.fetchall()

    pretty_results = []
    for result in results:
        single_date = {}
        r = str(result['entry_date'])
        d = datetime.strptime(r, '%Y%m%d')
        single_date['entry_date'] = datetime.strftime(d, '%d %B, %Y')
        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)

@app.route('/view/<date>', methods=['GET', 'POST']) # 2022-08-16
def view(date):

    db = get_db()

    cur = db.execute('SELECT id, entry_date FROM log_date WHERE entry_date = ?', [date])
    date_result = cur.fetchone()

    if request.method == 'POST':
        db.execute('INSERT INTO food_date (food_id, log_date_id) VALUES (?, ?)',
                    [request.form['food-select'], date_result['id']])
        db.commit()
 
    r = str(date_result['entry_date'])
    d = datetime.strptime(r, '%Y%m%d')
    pretty_date = datetime.strftime(d, '%d %B %Y')

    food_cur = db.execute('SELECT id, name FROM food');
    food_results = food_cur.fetchall()

    log_cur = db.execute("""SELECT 
                                food.name,
                                food.protein,
                                food.carbohydrates,
                                food.fat, 
                                food.calories
                            FROM log_date
                            JOIN food_date
                                ON food_date.log_date_id = log_date.id
                            JOIN food 
                                ON food.id = food_date.food_id
                            WHERE log_date.entry_date = ?""",
                            [date])
    log_results = log_cur.fetchall()

    return render_template('day.html', date=pretty_date, food_results=food_results, log_results=log_results)

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        protein = int(request.form['protein']) 
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = 4 * (protein + carbohydrates) + 9 * fat

        db.execute('INSERT INTO food (name, protein, carbohydrates, fat, calories) VALUES (?, ?, ?, ?, ?)',
                   [name, protein, carbohydrates, fat, calories])
        db.commit()

    cur = db.execute('SELECT name, protein, carbohydrates, fat, calories FROM food')
    results = cur.fetchall()

    return render_template('add_food.html', results=results)


if __name__ == '__main__':
    app.run()