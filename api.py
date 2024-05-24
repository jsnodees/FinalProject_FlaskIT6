from flask import Flask, make_response, jsonify, request
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

def data_fetch(query):
    curs = mysql.connection.cursor()
    curs.execute(query)
    data = curs.fetchall()
    curs.close()
    return data

@app.route("/employees", methods=["GET"])
def get_employees():
    curs = mysql.connection.cursor()
    query = """
    SELECT * FROM employee
    """
    curs.execute(query)
    data = curs.fetchall()
    curs.close()

    return make_response(jsonify(data), 200)
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee_by_id(id):
    curs = mysql.connection.cursor()
    query = """
    SELECT * FROM employee where ssn = {}
    """.format(id)
    curs.execute(query)
    data = curs.fetchall()
    curs.close()
    return make_response(jsonify(data), 200)

@app.route("/employees/<int:id>/dependent", methods=["GET"])
def get_dependent_by_employee(id):
    data = data_fetch("""
    SELECT * FROM employee WHERE id = %s
    """.format(id))
    return make_response(jsonify({"ssn": id,  "count": len(data), "dependent": data}), 200)

@app.route("/employees", methods=["POST"])
def add_employee():
    curs = mysql.connection.cursor()
    info = request.get_json()
    Fname = info["First_name:"]
    Lname = info["Last_name:"]
    curs.execute(
        """INSERT INTO EMPLOYEE (address, bdate, DL_id, first name, last name, Minit, 
        Salary, Super_ssn, ssn) VALUE (%s, %s)""", (Fname, Lname),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(curs.rowcount))
    rows_affected = curs.rowcount
    curs.close()
    return make_response(jsonify({"message": "Employee added succesfully!", "rows_affected": rows_affected}), 201 )


if __name__ == "__main__":
    app.run(debug=True)
