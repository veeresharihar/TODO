from turtle import title
from flask import Flask,render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    slno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.slno}-{self.title}"

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('home.html',alltodo=alltodo)


@app.route('/delete/<int:slno>',methods=['GET','POST'])
def delete(slno):
    todo=Todo.query.filter_by(slno=slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ =="__main__":
    app.run(debug=True)