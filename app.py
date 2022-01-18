from datetime import datetime
import re
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)
#for making a database 
class todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc= request.form['desc']
        todoo=todo(title=title,desc=desc)
        db.session.add(todoo)
        db.session.commit()
        
    # todo1=todo(title="First Todo",desc="Flask sikhega mai")
    # db.session.add(todo1)
    # db.session.commit()
    allTodo=todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)
    
@app.route('/show')
def products():
    allTodo=todo.query.all()
    print(allTodo)
    return 'products page it is'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc= request.form['desc']
        allTodo=todo.query.filter_by(sno=sno).first()
        allTodo.title=title
        allTodo.desc=desc
        db.session.add(allTodo)
        db.session.commit()
        return redirect('/')

    allTodo=todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    Todo=todo.query.filter_by(sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True,port=8000)    