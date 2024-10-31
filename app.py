from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message


app = Flask(__name__)
app.config["SECRET_KEY"] = "myapplication123"  # For flash messages and other secure uses
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Corrected mail server key
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "gauravpande568@gmail.com"  # Update with environment variable in production
app.config["MAIL_PASSWORD"] = ""  # Update with environment variable in production
db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(80), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            date = request.form["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            occupation = request.form["occupation"]

            new_form = Form(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date=date_obj,
                occupation=occupation,
            )
            db.session.add(new_form)
            db.session.commit()

            # Prepare and send the email
            message_body = f"Hello {first_name},\nYour application has been successfully submitted."
            message = Message(
                "New Form Submission",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email],
                body=message_body,
            )
            mail.send(message)
            flash("Your form was submitted successfully", "success")

        except Exception as e:
            db.session.rollback()
            flash("There was an error submitting the form.", "error")
            print("Error:", e)

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
