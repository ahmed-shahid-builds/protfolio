from flask import Flask, render_template, request, redirect, flash, session, url_for
from datetime import datetime
from functools import wraps
import os

import database as db
from notifications import send_booking_notification


app = Flask(__name__)

app.secret_key = "jakes123412344321"

# Set this via environment variable in production:
#   export ADMIN_PASSWORD=yourpassword
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme123")

ALL_TIME_SLOTS = [
    "8:00 AM - 11:00 AM",
    "11:00 AM - 2:00 PM",
    "2:00 PM - 5:00 PM",
]

# Create the database/table on startup if it doesn't exist yet
db.init_db()


# ===========================
# HOME
# ===========================

@app.route("/")
@app.route("/home.html")
@app.route("/index.html")
def home():
    booked_times = db.get_booked_times_for_today()
    return render_template(
        "index.html",
        booked_times=booked_times
    )


# ===========================
# STATIC PAGES
# ===========================


@app.route("/about.html")
@app.route("/about")
def about():

    return render_template(
        "about.html"
    )




@app.route("/services")
@app.route("/services.html")
def services():

    return render_template(
        "services.html"
    )





@app.route("/emergency-plumbing")
@app.route("/emergency plumbing")
def emergency():

    return render_template(
        "emergency-plumbing.html"
    )





@app.route("/drain-cleaning")
def drain():

    return render_template( "drain-cleaning.html" )





@app.route("/water-heater")
def water_heater():
    return render_template("water-heater.html")


@app.route("/leak-detection")
def leak_detection():

    return render_template("leak-detection.html")


@app.route("/service-areas")
def service_area():

    return render_template("service-areas.html")

@app.route("/reviews.html")
@app.route("/reviews")
@app.route("/Reviews")
def reviews():

    return render_template("reviews.html")


@app.route("/contact")
@app.route("/contact.html")
def contact():

    return render_template("contact.html")


# ===========================
# BOOKING SYSTEM
# ===========================

@app.route("/book", methods=["POST"])
def book():

    name = request.form["name"]
    phone = request.form["phone"]
    time = request.form["time"]
    service = request.form["service"]
    message = request.form["message"]

    today = datetime.now().strftime("%Y-%m-%d")

    # First-come-first-served: if this slot is already taken today, reject it.
    if db.is_slot_taken(today, time):
        flash("Sorry, that time slot just got booked. Please pick another one.")
        return redirect("/")

    db.create_reservation(name, phone, today, time, service, message)

    # Notify the business owner by email (won't crash booking if email fails)
    send_booking_notification(name, phone, today, time, service, message)

    flash("Reservation submitted successfully! We'll confirm by phone shortly.")
    return redirect("/")


# ===========================
# ADMIN AREA
# ===========================

def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)
    return wrapped


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect password.")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    reservations = db.get_all_reservations()
    return render_template("admin.html", reservations=reservations)


@app.route("/admin/cancel/<int:reservation_id>", methods=["POST"])
@login_required
def admin_cancel(reservation_id):
    db.cancel_reservation(reservation_id)
    flash("Appointment cancelled. That time slot is now available again.")
    return redirect(url_for("admin_dashboard"))


# RUN SERVER

if __name__ == "__main__":

    app.run(debug=True, port=5001)
