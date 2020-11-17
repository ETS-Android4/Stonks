from flask import Flask
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'db name'

mysql = MySQL(app)


@app.route('/')
def hell():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM tata ''')
    result = cur.fetchall()
    print(result)
    return 'done'





if __name__ == "__main__":
    app.run(debug = True)