from wtforms import Form, validators
from wtforms.fields import StringField, TextAreaField, TelField, EmailField
from wtforms.csrf.session import SessionCSRF
from flask_wtf import RecaptchaField
class ContactForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF  
        csrf_secret = b'yD5g@4]!wer45g8fda5thk^wtyokVe468f3v{/}' 
    name = StringField(
        "Name",
        validators=[
            validators.input_required()
        ], 
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
            "autocomplete" : "name"
        }
    )
    email = EmailField(
        "Email",
        validators=[
            validators.input_required()
        ], 
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
            "autocomplete" : "email"
        }
    )
    number = TelField(
        "Telephone",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "",
            "class" : " mb-3 floating-label",
            "autocomplete" : "tel"

        }
    )
    message = TextAreaField(
        "Message",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label"
        })
    recaptcha = RecaptchaField()