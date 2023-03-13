from flask import Flask ,request,render_template,redirect,jsonify
import pyrebase
import stripe
from chat import get_response

stripe.api_key = "sk_test_51Mf5iMSHP7cyCBSwbnncFvTrRnH4J0rwq5WJQklUaTtMnPK3KOA2v08cRX457eu1GY4nY67Yst9SXegWba4wc11L00b5LLpjmB"
YOUR_DOMAIN = "http://localhost:5000"

app = Flask(__name__)

#---------------------------------------- Database ---------------------------------------------

config = {
    'apiKey': "AIzaSyBvDcyseD-KvyScH2dMmc_8hViaYN24Tc8",
    'authDomain' : "authenticate-900e0.firebaseapp.com",
    'projectId' : "authenticate-900e0",
    'storageBucket' : "authenticate-900e0.appspot.com",
    'messagingSenderId' : "633937864486",
    'appId' : "1:633937864486:web:7735ae1604e3c37fa543e7",
    'measurementId'  : "G-LCRBSBPLDF",
    'databaseURL' : 'https://authenticate-900e0-default-rtdb.firebaseio.com/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

database = firebase.database()

#-----------------------------------------------------------------------------------------------

#----------------------------------------- Home Page -------------------------------------------

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('home.html')

#-----------------------------------------------------------------------------------------------

#-------------------------------------- ChatBot ------------------------------------------------

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: CHECK IF TEXT IS VALID
    response = get_response(text)
    message = {"answer": response} 
    return jsonify(message)

#-----------------------------------------------------------------------------------------------

#-------------------------------------- Appointment --------------------------------------------

@app.route('/Appoint',methods=['GET','POST'])
def Appointment():
    return render_template()

#-----------------------------------------------------------------------------------------------

# ----------------------------------------- Payment --------------------------------------------

@app.route('/cancel',methods=['GET','POST'])
def cancel():
    return render_template('cancel.html')


@app.route('/success',methods=['GET','POST'])
def success():
    return render_template('success.html')


@app.route('/Donate',methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price":"price_1Mf5mHSHP7cyCBSwt9FT4k6p",
                    "quantity":1
                }
            ],
            mode="subscription",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url = YOUR_DOMAIN + "/cancel"
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url,code=303)

# -----------------------------------------------------------------------------------------------

#-------------------------------------- Model ---------------------------------------------------

@app.route('/Test',methods=['GET','POST'])
def test():
    return render_template('home.html')
 
#------------------------------------------------------------------------------------------------

# ----- Doctor -------

@app.route('/DLogin',methods=['GET','POST'])
def Dlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        try:
            user = auth.sign_in_with_email_and_password(username,password)
            print('success')
            message = 'success'
        except:
            message = 'unsuccessful'
            print('unsuccessful')

        return render_template('Dlogin.html',message=message)

    return render_template('Dlogin.html')
        

@app.route('/DRegister',methods=['GET','POST'])
def DRegister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        docid = request.form['docid']
        password = request.form['pass']

        data = {'name':name,'email':email,'Phone':number,'docid':docid,'password':password}

        try:
            database.push(data)

            user = auth.create_user_with_email_and_password(email,password)

            print('account created success')
            message = 'success'
        except:
            message = 'unsuccessful'
            print('account creation unsuccessfull')

        return render_template('DRegister.html',message=message)

    return render_template('DRegister.html') 

# ------- Paitent -------

@app.route('/PLogin',methods=['GET','POST'])
def Plogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(username,password)
            print('success')
            message = 'success'

        except Exception as e:
            message = 'unsuccessful'
            #print('unsuccessful '+e)

        return render_template("Plogin.html",message=message)    

    return render_template("Plogin.html")     


@app.route('/PRegister',methods=['GET','POST'])
def PRegister():
    if request.method == 'POST':
        name = request.form['Rname']
        email = request.form['REmail']
        phone = request.form['Rphone']
        password = request.form['Pass']

        data = {'name':name,'email':email,'Phone':phone,'password':password}
        
        try:
            database.push(data)

            user = auth.create_user_with_email_and_password(email,password)

            print('account created success')
            message = 'success'

        except Exception as e:
        # message = 'unsuccess'
            print('account creation unsuccessfull '+e)

        return render_template("Pregister.html",message=message)

    return render_template("Pregister.html")



if __name__ == "__main__":
    app.run(debug=True)