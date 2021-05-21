import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache


account_sid = 'ACb895ab7ee06ffe89e57ba5bfdce2d62f'
auth_token = '2d73194bf0a26811d65f76e7e4aff8a6'

client = Client(account_sid, auth_token)

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('index.html')


@app.route('/test_page', methods=['POST', 'GET'])
def login_registration_dtls():
    first_name = request.form['fname']
    print(first_name)
    last_name = request.form['lname']
    print(last_name)
    email_id = request.form['email']
    print(email_id)
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['aadhaarnumber']
    date = request.form['date']
    full_name = first_name+"."+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        msg = "Hello "+" "+full_name+" "+"Your Travel From " +\
            " "+source_dt+" "+"To"+" "+destination_dt+" "\
            + "Has" + " "+status + " On"+" "+date+" "+", Confirmed"
        client.messages.create(to="whatsapp:+91" + phoneNumber,
                               from_="whatsapp:+14155238886",
                               body=msg)
        print(phoneNumber)
        return render_template('status.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)

    else:
        status = 'Not confirmed'
        client.messages.create(to="whatsapp:+91"+phoneNumber,
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + " " + "Your Travel From " +
                               " " + source_dt + " " + "To" + " " + destination_dt + " "
                               + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")
        return render_template('status.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)


if __name__ == "main_":
    app.run(port=9001, debug=True)
