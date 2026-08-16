import random

from flask import Blueprint, render_template, url_for, redirect, request, session, flash, current_app, send_from_directory, abort
from flask_login import current_user, login_user

from core.models import db
from core.forms.contact import ContactForm
from core.forms.quote import EventQuoteForm
from flask_mailman import EmailMessage
from core.extensions import login_manager
from core.admin.forms.login import LoginForm

from core.models.page import Page
from core.models.gallery import Gallery
from core.models.user import User
from core.models.service import  Service, Category
from core.models.event import Event
from core.models.policy import Policy

core = Blueprint('core', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

@core.before_request
def preview():
    if request.endpoint in ('core.coming_soon', 'static', 'media'):
        return
    if request.endpoint.startswith('admin'):
        return
    """ #TODO REmove THIS 
    if not current_user.is_authenticated:
        return redirect(url_for('core.coming_soon')) """


@core.route('/')
def welcome():
    page = Page.get_for_tag('home')
    gallery = Gallery()
    shows = Event.get_previous(limit=4)

    for show in shows:
        if not show.gallery: continue
        i = 0
        while i < len(show.gallery.slides) and i <= 5:
            gallery.slides.append(show.gallery.slides[i])
            i+= 1
    
    random.shuffle(gallery.slides)

    context = {
        'page' : page,
        'gallery' : gallery

    }
    return render_template('pages/index.html', **context)

@core.route('/about')
def about():
    page = Page.get_for_tag('about')
    context = {
        'page' : page,

    }
    return render_template('pages/about.html', **context)


@core.route('/shows')
def shows():
    page = Page.get_for_tag('events')
    
    prev_shows = Event.get_previous(8)
    future_shows = Event.get_upcoming()
    grouped_events = {}
    for event in future_shows:
        # Create a key for month-year grouping
        month_year = event.date.strftime('%B %Y')  # e.g., "July 2026"
        
        if month_year not in grouped_events:
            grouped_events[month_year] = []
        
        grouped_events[month_year].append(event)
    context = {
        'page' : page,
        'prev_shows' : prev_shows,
        'future_events' : grouped_events
    }
    return render_template('pages/shows.html', **context)


@core.route('/shows/<string:slug>')
def event_detail(slug):
    show = Event.get_by_slug(slug)
    page = Page.get_for_tag('events')
    context = {
        'show' : show,
        'page' : page
    }
    return render_template('pages/show-detail.html', **context)

@core.route('/services')
def services():
    primary_group = Category.get_group()
    primary = primary_group.services
    secondary_group = Category.get_group('secondary')

    secondary = secondary_group.services
    for service in secondary: 
        print(service.title)
    page = Page.get_for_tag('services')
    form = EventQuoteForm()
    context = {
        'primary' : primary,
        'secondary' : secondary,
        'page' : page,
        'form' : form    
    }
    return render_template('pages/services.html', **context)

@core.route('/services/<slug>')
def service_detail(slug):
    service = Service.get_by_slug(slug) 
    if not service:
        return abort(404)
    form = EventQuoteForm()
    context = {
        'service' : service,
        'form' : form,
    }
    return render_template('pages/service-detail.html', **context)
    
@core.route('/gallery')
def gallery():
    shows = Event.get_previous()
    page = Page.get_for_tag('gallery')
    
    context = {
        'shows' : shows,
        'page' : page
        
    }
    return render_template('pages/gallery.html', **context)

@core.route('/coming-soon', methods=['GET', 'POST'])
def coming_soon():
    form = ContactForm(request.form, meta={'csrf_context': session})
    page= {}
    context = {
        'form' : form,
        'page' : page
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


@core.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form, meta={'csrf_context': session})
    page= Page.get_for_tag('contact')
    context = {
        'form' : form,
        'page' : page
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
            except Exception as e:
                print(f"Email failed to send: {e}")
                flash(f"Email failed  to send.", "error")
            else: 
                flash("Message sent successfully, we will respond within 2 business days..", "success")

               
        else: 
            print("Error parsing form data!!!!")
            for error in form.errors.values():
                print(error)
            flash("There was an error parsing your message, please try again.", "error")

            return redirect(url_for('core.contact'))       
    return render_template('pages/contact.html', **context)


@core.route('/login', methods=['GET', 'POST'])
def login():
    # 1. If they are already logged in, send them straight to the admin panel
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))

    form = LoginForm(request.form, meta={'csrf_context': session})

    # 2. Handle form submission
    if form.validate():
        # Find user by username
        user : User = User.query.filter_by(username=form.username.data).first()
        
        # Verify user exists and the password hash matches
        if user and user.verify_password(form.password.data):
            # Log the user in with Flask-Login
            login_user(user)
            print(f"Login function executed. Is user authed? {current_user.is_authenticated}")
            # Handle the 'next' query parameter securely (from Flask-Admin/Flask-Login intercepts)
            next_page = request.args.get('next')
            
            # Simple security check to make sure the next page stays on your domain
            if not next_page:
                next_page = url_for('admin.index')
                
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        
        # Generic error message so malicious entities don't know if username or password was wrong
        flash('Invalid username or password.', 'danger')
        print(f"Login function not successful. Is user authed? {current_user.is_authenticated}")
        
    return render_template('admin/login.html', form=form)

@core.route('/media/<path:filename>')
def serve_media(filename):
    """Serves files seamlessly out of the media directory."""
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@core.route('/legal/')
def policy_list():
    page = Page.get_for_tag('policies')
    policies =Policy.get_all()
    context = {
        'page' : page,
        'policies' : policies
    }
    return render_template('pages/policty-list.html', **context)

@core.route("/legal/<slug>")
def policy_detail(slug):
    policy = Policy.get_by_slug(slug)
    if not policy: return abort(404)
    other_policies = Policy.query.filter(Policy.id != policy.id).all()

    context = {
        'policy' : policy,
        'other_policies' : other_policies
    }
    return render_template('pages/policy-detail.html', **context)


@core.errorhandler(404)
def error_not_found(e):
    return render_template('error/404.html')


@core.route('/quote', methods=['POST'])
def quote():
    form = EventQuoteForm(request.form, meta={'csrf_context': session})
    if not form.validate():
        print("Error parsing form data!!!!")
        for error in form.errors.values():
            print(error)
        flash("There was an error parsing your message, please try again.", "error")

        return redirect(url_for('core.services'))    
    print(form.data)
    client_email = form.email.data
    client_name = form.name.data
    client_tel = form.number.data
    start_date = form.start_datetime
    end_date = form.end_datetime
    message_body = form.message.data
    print(type(form.services_required.data)) 
    service_ids = list(form.services_required.data)
    selected_ids = [int(id) for id in service_ids]
    services = Service.query.filter(Service.id.in_(selected_ids)).all()
    service_titles = [service.title for service in services]
    email_body=f"New Quote request from:\n{client_name}\nTel:\n{client_tel}\nResponse Email:\n{client_email}\n\nMessage\n\n{message_body}\n\n"
    email_body += f"Requested Services\n\n "
    for title in service_titles: 
        email_body += f"{title}\n" 
    email_body += f"Requested Dates:\n {start_date} - {end_date}"
    
    msg = EmailMessage(
        subject="New Website Event Quote",
        body=email_body,
        to=[current_app.config['INBOUND_MAIL']]
        
    )
    try: 
        msg.send(fail_silently=False)
        flash("Message sent successfully, we will respond within 2 business days..", "success")
    except Exception as e:
        print(f"Email failed to send: {e}")
        flash(f"Email failed  to send.", "error")
    else:
        form =EventQuoteForm()    


    return redirect(url_for('core.services'))