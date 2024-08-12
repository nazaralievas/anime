from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    articles = Article.query.all()
    return render_template('homepage.html', articles=articles)

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        image = request.form['image']
        new = Article(title=title, text=text, image=image)
        db.session.add(new)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get(id)
    return render_template('article.html', article=article)


@app.route('/delete/<int:id>')
def delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.text = request.form['text']
        db.session.commit()
        return redirect('/')

    return render_template('update.html', article=article)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
