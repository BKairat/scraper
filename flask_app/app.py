from flask import Flask, render_template, request
from config import db_name, db_user, db_password, db_host, db_port
import psycopg2


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = psycopg2.connect(
        host='postgres',
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()

    cursor.execute("SELECT title, image FROM parsed_flats LIMIT 500")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('index.html', rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)