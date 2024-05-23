from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/employees", methods=["GET"])
def get_employees():
    curs = mysql.connection.cursor()
    query = """
    select * from employee
    """
    curs.execute(query)
    data = curs.fetchall()
    curs.close()

    return make_response(jsonify(data), 200)



if __name__ == "__main__":
    app.run(debug=True)
