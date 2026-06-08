from flask import Blueprint, render_template, url_for, redirect, request, session, flash, current_app
from core.models import db
from core.forms.contact import ContactForm
from flask_mailman import EmailMessage

core = Blueprint('core', __name__)

@core.route('/', methods=['GET', 'POST'])
def coming_soon():
    form = ContactForm(request.form, meta={'csrf_context': session})
    context = {
        'form' : form

    }
    if request.method == "POST":
        print(form.data)
        if form.validate():
            client_email = form.email.data
            client_name = form.name.data
            client_tel = form.number.data
            message_body = form.message.data
            print(f"MAIL PORT:  {current_app.config['MAIL_PORT']}")
            print(f"MAIL USE SSL:  {current_app.config['MAIL_USE_SSL']}")
            print(f"MAIL USE TLS:   {current_app.config['MAIL_USE_TLS']}")
            #TEMP: Print the form data
            print(f"New contact query from:\n{client_name}\nTel:\n{client_tel}\nResponse Email:\n{client_email}\n\nMessage\n\n{message_body}")
            msg = EmailMessage(
                subject="New Website Contact Query",
                body=f"New contact query from:\n{client_name}\nTel:\n{client_tel}\nResponse Email:\n{client_email}\n\nMessage\n\n{message_body}",
                to=[current_app.config['INBOUND_MAIL']]
                
            )
            try:
                
                msg.send(fail_silently=False)
                flash("Message sent successfully, we will respond within 2 business days..", "success")
            except Exception as e:
                print(f"Email failed to send: {e}")
                flash(f"Email failed  to send. {e}", "error")
               
        else: 
            print("Error parsing form data!!!!")
            for error in form.errors.values():
                print(error)
            flash("There was an error parsing your message, please try again.", "error")

            return redirect(url_for('core.coming_soon'))       
    return render_template('pages/coming-soon.html', **context)


