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


def no_entry(text):

    if text:
        return False
    else:
        return True

@app.route('/')
def redirect_main():
    return redirect('/all_blogs')

@app.route('/all_blogs')
def blog():

    blog_id = request.args.get('id')

    if blog_id:
        view_blog=Blog.query.get(blog_id)
        return render_template('blog.html', blog=view_blog)
    else:
        show_all = Blog.query.all()
        return render_template('all_blogs.html', blogs=show_all)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    title_error = ""
    blog_error = ""

    if request.method == 'POST':
        add_title = request.form['blog_title']
        add_blog = request.form['blog_body']
        add_all = Blog(add_title, add_blog)

        if no_entry(add_title):
            title_error = "A title is required."
            if no_entry(add_blog):
                blog_error = "A text is required for the blog."
            return render_template('newpost.html', title_error=title_error, blog_error=blog_error)
        elif no_entry(add_blog):
            blog_error = "A text is required for the blog."
            return render_template('newpost.html', title_error=title_error, blog_error=blog_error)
        else:
            db.session.add(add_all)
            db.session.commit()
            show_blog = "/all_blogs?id=" + str(add_all.id)
            return redirect(show_blog)
    else:
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
