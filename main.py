from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime

app = Flask(__name__)


codes = []
user_data = []

@app.route("/createclass")
def main(): 
    return render_template("index.html")


def addUserData(code, ip):
    for dat in user_data:
        if dat["ip"] == ip:
            found = False
            for cod in dat["code"]:
                if cod == code:
                    found = True
            if found == False: 
                dat["code"].append(code)
    user_data.append({"ip":ip, "code": [code]})


@app.route("/ajax/attendance-data", methods=["POST"])
def attendance_data(): 
    form = request.form
    uniquecode = form["code"]
    password = form["pass"]
    valid = False
    for code in codes:
        if code["code"] == uniquecode:
            if code["pass"] == password:
                addUserData(code["code"], request.remote_addr)
                return "True"
            else: 
                return "False"

    addUserData(uniquecode, request.remote_addr)
    codes.append({"code": uniquecode, "pass": password, "people":[], "latest_iteration": 0})
    return "True"

@app.route("/ajax/get-attendance", methods=["POST"])
def get_attendance():
    form = request.form
    code = form["code"]
    for cod in codes:
        if cod["code"] == code:
            return jsonify(cod["people"])
        
    return jsonify([])

@app.route("/ajax/send-attendance", methods=["POST"])
def send_attendance():
    form = request.form
    code = form["code"]
    name = form["name"]
    for cod in codes:
        if cod["code"] == code:
            found = False
            for person in cod["people"]:
                if person["name"] == name:
                    found = True
                    person["amount"] += 1
                    person["last_joined"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            if found == False:
                cod["people"].append({"name": name, "amount": 1, "last_joined": datetime.today().strftime('%Y-%m-%d %H:%M:%S')})

    return "True"

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/")
def attend():
    return render_template("giveattendance.html")

@app.route("/attendance/<code>")
def attendance(code):
    allowed = False
    if code == "test":
        allowed = True
    for user in user_data:
        if user["ip"] == request.remote_addr:
            if code in user["code"]:
                allowed = True
    if allowed:    
        return render_template("track_attendance.html")
    else: 
        return redirect("/")

if __name__ == "__main__":
    app.run(port=8000, debug=True)