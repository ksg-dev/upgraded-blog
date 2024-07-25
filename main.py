from flask import Flask, render_template, request
import requests



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
    print(f"{name}\n{email}\n{phone}\n{message}")
    return render_template("contact.html", heading_text=heading_text, sub_text=sub_text)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        return receive_data("Successfully sent message.", "Thanks!")
    else:
        return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)