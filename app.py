import time
import os 

from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Message, Mail

mail = Mail()

app = Flask(__name__)
app.secret_key = ''

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ''
app.config["MAIL_PASSWORD"] = ''

mail.init_app(app)


bootstrap = Bootstrap(app)

def get_images():
    images = []

    for i in os.listdir(os.path.split(os.path.realpath(__file__))[0]+'/static/gallery'):
        if i != '.DS_Store':
            images.append("gallery/" + i)
    return images


@app.context_processor
def inject_user():
  return dict(year=time.strftime("%Y"))

@app.route('/')
@app.route("/index")  
def index():
    return render_template('index.html')


@app.route("/gallery")  
def gallery():
    return render_template('gallery.html', date=time.strftime("%m/%d/%Y"), images=get_images())

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact_us.html', form=form)
        else:
          msg = Message(form.subject.data + " (ESTIMATE EMAIL)", sender='contact@example.com', recipients=[''])
          msg.body = "Client Name: {0}\nClient Email: {1}\nMessage:\n\n{2}".format(form.name.data, form.email.data, form.message.data)
          mail.send(msg)

          return render_template('contact_us.html', success=True)

    elif request.method == 'GET':
        return render_template('contact_us.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
    
