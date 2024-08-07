from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]



blog_url = "https://api.npoint.io/5910111f7431b1d7e52d"
all_posts = requests.get(blog_url).json()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/<int:num>")
def get_post(num):
    target_post = None
    for blog_post in all_posts:
        if blog_post["id"] == num:
            target_post = blog_post
    return render_template("post.html", post=target_post, image="static/assets/img/" + str(num) + ".jpg")


def receive_data(heading_text, sub_text):
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    content = f"{name}\n{email}\n{phone}\n{message}"
    send_email(content)
    return render_template("contact.html", heading_text=heading_text, sub_text=sub_text)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        return receive_data("Successfully sent message.", "Thanks!")
    else:
        return render_template("contact.html")


def send_email(content):
    global MY_EMAIL
    global PASSWORD
    subject = "New Contact Form Submitted"
    body = content

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: {subject} \n\n{body}"
        )



if __name__ == "__main__":
    app.run(debug=True)