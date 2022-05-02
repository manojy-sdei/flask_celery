from flask import Flask, render_template ,request,redirect,url_for,flash,session
from tasks import make_celery
import time
from flask_mail import Mail ,Message 
import os
from dotenv import load_dotenv
from flask_session import Session
from random import choice , random
from werkzeug.utils import secure_filename
from docx2pdf import convert


load_dotenv()


app = Flask(__name__)
mail = Mail()
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/celerydata'  #or we can use hear the localhost and uri 




####### mail configurations #########

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')


celery = make_celery(app)
sess = Session()


######## INSERT DATA IN DATABASE #####


# @celery.task(name='flaskapp.insert')
# def insert(): 
#     # for i in range(100):
#     data = ''.join(choice("ABCDEFGE"))
#     result = Results(data=data)
#     db.session.add(result)
#     db.session.commit()
#     return 'done'

############### SIMPLE TASK ######

@app.route('/user/<name>')
async def user(name):
    reverce.delay(name)
    return "request sent"


@celery.task(name='flaskapp.reverse')
def reverce(string):
    return "Done!!!!!"

############### CREATE A TASK FOR MAIL DEMO NEED TO CONFIG MAIL SERVER #######


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


# route that will execute a long-running task

@celery.task(name='flaskapp.long_running_task')
def long_task():
    # long_running_task.delay()
    return "Done!!!"


@app.route("/long_running_task")
def long_running_task():
    time_to_wait = 5
    print(f"This task will take {time_to_wait} seconds to complete...")
    time.sleep(time_to_wait)
    return f"<h1>The task completed in {time_to_wait} seconds!</h1>"


@celery.task
def sending_email_with_celery(name='flaskapp.long_running_task_celery'):
    print("Executing Long running task : Sending email with celery...")
    time.sleep(15)
    print("Task complete!")


# route to trigger celery task
@app.route("/long_running_task_celery")
def long_running_task_celery():
    sending_email_with_celery.delay()
    return f"Long running task triggered with Celery! Check terminal to see the logs..."


##########  sending email ###########


# @celery.task(name='flaskapp.sending_mail')
# def mail_send():
#     return sending_mail()

# @app.route('/', methods=['GET', 'POST'])
# def sending_mail():
#     if request.method == 'GET':
#         return render_template('mail.html', email=session.get('email', ''))
#     email = request.form['email']
#     session['email'] = email
#     # sends this content
#     email_msg = {
#         'subject': 'Testing Celery with Flask',
#         'to': email,
#         'body': 'Testing background task with Celery'
#         }
    
#     if request.form['submit'] == 'Send':
#         # sends the email content to the backgraound function
#         send_email.delay(email_msg)
#         flash('Sending email to {0}'.format(email))
#     else:
#         flash('No Email sent')

#     return redirect(url_for('sending_mail'))


# @celery.task
# def send_email(email_msg):
# #Async function to send an email with Flask-Mail    
#     msg_sub = Message(email_msg['subject'],
#     email_sender = app.config['MAIL_DEFAULT_SENDER'],
#     recipient = [email_msg['to']])
#     msg_sub.body = email_msg['body']
#     with app.app_context():
#         mail.send(msg_sub)





############################################################################

if __name__ == '__main__':
    app.secret_key='super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=True)
