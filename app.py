from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from collections.abc import Mapping

app = Flask(__name__)

ENV = ''

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01274757673@localhost/danhgia'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gqnkyebedxqckf:9a065e2029f094d49c977230adc70dc006549744ea48c8259e08617964820a7a@ec2-54-160-109-68.compute-1.amazonaws.com:5432/d7e1bfc1d7ko9r'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'danhgiasv'
    id = db.Column(db.Integer, primary_key=True)
    mssv = db.Column(db.String(200), unique=True)
    student = db.Column(db.String(200))
    teacher = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, mssv, student, teacher, rating, comments):
        self.mssv = mssv
        self.student = student
        self.teacher = teacher
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        mssv = request.form['mssv']
        student = request.form['student']
        teacher = request.form['teacher']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if student == '' or teacher == '' or mssv == '':
            return render_template('index.html', message='Bạn chưa điền những thông tin cần thiết')
        if db.session.query(Feedback).filter(Feedback.mssv == mssv).count() == 0:
            data = Feedback(mssv, student, teacher, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(mssv, student, teacher, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='Bạn đã đánh giá rồi')


if __name__ == '__main__':
    app.run()
