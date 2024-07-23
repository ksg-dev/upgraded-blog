from flask import Flask, render_template
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


@app.route("/blog/<int:num>")
def get_post(num):
    target_post = None
    for blog_post in all_posts:
        if blog_post["id"] == num:
            target_post = blog_post
    return render_template("post.html", post=target_post)

if __name__ == "__main__":
    app.run(debug=True)