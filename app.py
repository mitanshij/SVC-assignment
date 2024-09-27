from flask import Flask, request, redirect, url_for, render_template, session
import pymongo 
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = ("testing")

uri = pymongo.MongoClient("mongodb+srv://mitanshijain22:Minor2sem6@flasktest.2x2lgzj.mongodb.net/")

try:
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client.Test  # Select your database
    collection = db.FlaskTest  # Select your collection
    
    # Test query
    result = collection.find_one({})
    print(result)
    
    # Disconnect from MongoDB
    client.close()
    
except Exception as e:
    print("Error:", e)

client = uri 

db = client.get_database('total_records')

records = db.register

@app.route('/', methods=['GET','POST'])

# MongoDB connection URI

    
def index():
    message = ''
    if "email" in session: 
        return redirect(url_for("logged_in"))
    if request.method == 'POST':   # the user submitted a form via POST method
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)

            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)