from flask import Flask,render_template,request,redirect
from pymongo import MongoClient
from flask import Mail,Message

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.@gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "21491A4207@qiscet.edu.in"
app.config["MAIL_PASSWORD"] = ""
mail = Mail(app)

my_client = MongoClient("localhost", 27017)
my_db = my_client["calci"] # database
results = my_db["results"] # collection
isLoggedIn = False

crendentials = {"steeve@gmail.com":"Steeve@123"}

@app.route("/",methods=["GET","POST"])
def home():
    global isLoggedIn
    if request.method == "POST":
        log_email = request.form["email"]
        log_password = request.form["password"]
        if(log_email in crendentials) and (crendentials[log_email] == log_password):
            isLoggedIn = True
            
            return redirect("/calci")
        else:
            return redirect("/")
    else:
        return render_template("login.html")
    

@app.route("/calci",methods=["GET","POST"])
def calculator():
    if isLoggedIn == True:
        if request.method == "POST":
            n1 = int(request.form["num1"])
            opr = request.form["opr"]
            n2 = int(request.form["num2"])
            msg = Message(subject="calculation", sender="",
                        recipients=[""])
            
            if opr == "add":
                res = f"{n1} + {n2} is {n1+n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body = res
                mail.send(msg)
                return render_template("index.html", output=res)
            elif opr == "sub":
                res = f"{n1} - {n2} is {n1-n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body = res
                mail.send(msg)
                return render_template("index.html", output=res)
            elif opr == "mul":
                res = f"{n1} x {n2} is {n1*n2}"
                results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                })
                msg.body = res
                mail.send(msg)
                return render_template("index.html", output=res)
            elif opr == "div":
                try:
                    res = f"{n1} / {n2} is {n1/n2}"
                    results.insert_one({
                    "number1":n1, "number2":n2, "operator":opr, "output":res
                    })
                    return render_template("index.html", output=res)
                except Exception as e:
                    error = "Please change num2 as non-zero"
                    return render_template("index.html", output=error)
            
        else:
            return render_template("index.html")
    else:
        return redirect("/")
app.run(debug=True)

