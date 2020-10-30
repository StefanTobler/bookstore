from django.core.mail import EmailMessage

def send_mail():
    mail_subject = 'Bookstore4050 - Test Email'
    message = 'This is a test.'
    email = EmailMessage(
            mail_subject, message, to=['toblerlstefan@gmail.com']
    )
    email.send()

def main():
    send_mail()

if __name__ == '__main__':
    main()
