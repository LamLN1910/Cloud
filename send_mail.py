import smtplib
from email.mime.text import MIMEText


def send_mail(mssv, student, teacher, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'd9a177f2f63aef'
    password = '292aef88691d64'
    message = f"<h3>New Feedback Submission</h3><ul><li>Mssv: {mssv}</li><li>Student: {student}</li><li>Teacher: {teacher}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = mssv + '@student.hcmute.edu.vn'
    receiver_email = 'phongdaotao@hcmute.edu.vn'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
