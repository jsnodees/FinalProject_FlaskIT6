from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Example: tokens expire after 1 hour

jwt = JWTManager(app)
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

@app.route("/employees/search", methods=["GET"])
def search_employee():
    search_query = request.args.get("query")

    if not search_query:
        return make_response(jsonify({"error": "Query parameter 'query' is required."}), 400)

    curs = mysql.connection.cursor()
    try:
        query = """
        SELECT * FROM employee 
        WHERE Fname LIKE %s OR Lname LIKE %s
        """
        curs.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
        data = curs.fetchall()
        curs.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)



@app.route("/employees", methods=["POST"])
def add_employee():
    curs = mysql.connection.cursor()
    info = request.get_json()
    Address = info["Address"]
    Bdate = info["Bdate"]
    DL_id = info["DL_id"]
    Fname = info["Fname"]
    Lname = info["Lname"]
    Minit = info["Minit"]
    Salary = info["Salary"]
    Sex = info["Sex"]
    Super_ssn = info["Super_ssn"]
    ssn = info["ssn"]
    curs.execute(
        """INSERT INTO EMPLOYEE (Address, Bdate, DL_id, Fname, Lname, Minit, 
        Salary, Sex, Super_ssn, ssn) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (Address, Bdate, DL_id, Fname, Lname, Minit, 
        Salary, Sex, Super_ssn, ssn),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(curs.rowcount))
    rows_affected = curs.rowcount
    curs.close()
    return make_response(jsonify({"message": "Employee added succesfully!", "rows_affected": rows_affected}), 201 )

@app.route("/employees/<int:ssn>", methods=["PUT"])
def update_emplotee(ssn):
    curs = mysql.connection.cursor()
    info = request.get_json()
    Fname = info["Fname"]
    Lname = info["Lname"]
    Minit = info["Minit"]
    curs.execute(
        """ UPDATE employee SET Fname = %s, Lname = %s, Minit = %s WHERE ssn = %s""", 
        (Fname, Lname, Minit, ssn)
    )
    mysql.connection.commit()
    rows_affected = curs.rowcount
    curs.close()
    return make_response(jsonify({"message": "Employee updated succesfully!", "rows_affected": rows_affected}), 200 )

@app.route("/employees/<int:ssn>", methods=["DELETE"])
def delete_employee(ssn):
    curs = mysql.connection.cursor()
    curs.execute("""DELETE FROM employee WHERE ssn = %s """,(ssn,))
    mysql.connection.commit()
    rows_affected = curs.rowcount
    curs.close()
    return make_response(jsonify(
        {"message": "Employee deleted succesfully!", "rows_affected": rows_affected}
        ), 
        200 )

if __name__ == "__main__":
    app.run(debug=True)
