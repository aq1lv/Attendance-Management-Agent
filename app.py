from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["attendance_db"]
employees = db["employees"]


@app.route("/")
def home():
    employee_list = list(employees.find())
    return render_template("index.html", employees=employee_list)


@app.route("/add", methods=["POST"])
def add_employee():
    name = request.form["name"]
    total = int(request.form["total_classes"])
    attended = int(request.form["attended_classes"])

    percentage = (attended / total) * 100

    if percentage >= 95:
        status = "Premium Employee"
    elif percentage >= 85:
        status = "Green Employee"
    elif percentage >= 75:
        status = "Star Employee"
    else:
        status = "Regular Employee"

    employees.insert_one({
        "name": name,
        "total_classes": total,
        "attended_classes": attended,
        "percentage": round(percentage, 2),
        "status": status
    })

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)