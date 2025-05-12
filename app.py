from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db.payment import Payment
from datetime import timedelta, datetime
from payment.pix import Pix
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'
db.init_app(app)
sockeio = SocketIO(app)

@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    data = request.get_json()

    if 'Value' not in data:
        return jsonify({"message": "Invalid Value"})
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['Value'], expiration_date=expiration_date)

    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix["bank_payment_id"]
    new_payment.qr_code = data_payment_pix["qr_code_path"]
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has been created",
                    "payment": new_payment.to_dict()})

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def create_qrcode(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype="image/png")

@app.route('/payments/confirmation/pix', methods=['POST'])
def confirmation_pix():
    data = request.get_json()

    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"message": "Invalid payment data"}), 400

    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment or payment.paid:
        return jsonify({"message": "Payment not found"}), 404
    
    if data.get("value") != payment.value:
        return jsonify({"message": "Invalid payment data"}), 400
    
    payment.paid = True
    db.session.commit()
    sockeio.emit(f"payment-confirmation-{payment.id}")
    return jsonify({"message": "The payment has been confirmed"})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    searchPayment = Payment.query.get(payment_id)

    if not searchPayment:
        return render_template("404.html")

    if searchPayment.paid:
        return render_template("confirmed_payment.html", payment_id=searchPayment.id, value=searchPayment.value)
    return render_template("payment.html", payment_id=searchPayment.id, value=searchPayment.value, host="http://127.0.0.1:5000/", qr_code=searchPayment.qr_code)

# Websocket

@sockeio.on('connect')
def handle_connect():
    return print("Client connected to the server")

@sockeio.on('disconnect')
def handle_disconnect():
    return print("The client has been disconnected from the server")

if __name__ == "__main__":
    sockeio.run(app, debug=True)