from flask_mail import Message
from .. import mail
from flask import render_template, current_app, url_for


def send_email(to, subject, url, **kwargs):
    msg = Message(subject=subject, recipients=[to], sender=('li', current_app.config['MAIL_USERNAME']))
    # msg = Message(subject="liyong email", recipients=['516051225@qq.com'], body='text body haha',
    #               html='<b>HTML</b> body', sender=('li', '54004267@qq.com'))
    msg.body = render_template(url + '.txt', **kwargs)
    msg.html = render_template(url + '.html', **kwargs)
    mail.send(msg)
