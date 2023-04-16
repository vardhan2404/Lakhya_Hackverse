from flask import Flask, render_template, request
import pymongo
import model

app = Flask(__name__)

out = model.getMLPrediction(
    model.model, model.severity, model.distance, model.reputation, model.numOptions)
out = out.sort()
hnames = model.hnames


@app.route("/", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        username = request.form['username']
        password = request.form['password']
        for x in mycol.find():
            if x["name"] == username and x["password"] == password:
                return render_template('home.html')
        return "Wrong Credentials"
    else:
        return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]
        username = request.form['username']
        password = request.form['password']
        mydict = {"name": username, "password": password}
        x = mycol.insert_one(mydict)
        return "Signup successful!"
    else:
        return render_template('signup.html')


@app.route("/hospital", methods=['GET', 'POST'])
def hosp_signin():
    if request.method == 'POST':
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["hospitals"]
        username = request.form['username']
        password = request.form['password']
        beds = request.form['bed']
        myquery = {"name": username, "password": password}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            if x["name"] == username and x["password"] == password:
                newvalues = {"$set": {"beds": beds}}
                mycol.update_one(myquery, newvalues)
                return render_template('hosp_home.html')
        return "Wrong Credentials"
    else:
        return render_template('hosp_signin.html')


@app.route("/suggestions", methods=['GET', 'POST'])
def hosp_recommendation():
    if request.method == "POST":
        Dis = request.form['disease']
        ret = ""
        b = model.rlk(0, 4)
        for i in range(b, 5):
            ret += "<h2>" + str(i) + "." + \
                hnames[i][0] + " Hospital" + "</h1>" + "<br>"
        return ret
    else:
        return render_template("presug.html")


if __name__ == "__main__":
    app.run(debug=True)
