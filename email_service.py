import smtplib
from email.message import EmailMessage


def send_verification(user):
    link = 'http://localhost:4200/verify/' + str(user['id'])

    msg = EmailMessage()
    msg['Subject'] = 'Verification'
    msg['From'] = 'flx.grimm@gmail.com'
    msg['To'] = user['email']
    msg.set_content(
        'Thank you for signing up to our chat!\n'
        'To Proceed you need to verify your E-Mail by clicking on the following link:\n'
        '' + link)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('flx.grimm@gmail.com', 'KoMpLeX_1')
    smtp.send_message(msg)
    smtp.quit()