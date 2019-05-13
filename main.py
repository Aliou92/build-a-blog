from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:alioudiallo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120)) # Change made

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/", methods=['GET'])
def main():
    return render_template("newpost.html")

@app.route('/newpost', methods=['POST', 'GET'])
def index():
    return render_template("newpost.html")

@app.route('/blog?id=<id>', methods=['GET'])
def blog(id):
    post = Blog.query.filter_by(id=int(id))
   
    return render_template('/blog.html', tasks=post)

@app.route('/all_blogs', methods=['POST', 'GET'])
def all_blogs():
    if request.method == 'POST':
        blog_head = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_blog = Blog(blog_head, blog_body)
        db.session.add(new_blog)
        db.session.commit()

    tasks = Blog.query.all()

    return render_template("all_blogs.html", tasks = tasks)

if __name__ == "__main__":
    app.run()