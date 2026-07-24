from flask_wtf import FlaskForm
from wtforms.widgets import ListWidget, CheckboxInput, DateInput


from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    DateField,
    BooleanField,
    SelectMultipleField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional, Email
from flask_wtf import RecaptchaField


class EventQuoteForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired()
        ], 
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
            "autocomplete" : "name"
        }
    )
    # --- Contact Info ---
    number = StringField("Telephone", validators=[DataRequired()],
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
            "autocomplete" : "tel"
        }
    )
    email = StringField(
        "Email",
        validators=[Email(),DataRequired()],
         render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
            "autocomplete" : "email"
        }
    )

    # --- Event Timing ---
    start_datetime = DateField(
        "Event Start Date",
        format="%Y-%m-%d",
        validators=[Optional()],
        widget=DateInput(),
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
        }
    )

    end_datetime = DateField(
        "Event End Date",
        format="%Y-%m-%d",
        validators=[Optional()],
        widget=DateInput(),
        render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
        }
        
    )

    is_multi_day = BooleanField("This is a multi‑day event")
    no_timing_info = BooleanField("I do not have this information yet")

    # --- Services Required (custom multi-select) ---
    services_required = SelectMultipleField(
        "Services Required",
        choices=[],  # filled dynamically
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False),
        validators=[Optional()]
    )

    # --- Message ---
    message = TextAreaField("Message", validators=[Optional()],  render_kw= {
            "placeholder" : "",
            "class" : " floating-label",
        })
    recaptcha = RecaptchaField()

    submit = SubmitField("Request Quote")


    def __init__(self, *args, **kwargs):
        from core.models.service import Service

        super().__init__(*args, **kwargs)

        # Load services dynamically
        self.services_required.choices = [
            (str(service.id), service.title)
            for service in Service.query.order_by(Service.title.asc()).all()
        ]
    def validate(self):
        rv = super().validate()
        if not rv:
            return False

        # If user says they don't have timing info, skip datetime checks
        if self.no_timing_info.data:
            return True

        # Otherwise enforce that start/end must be provided
        if not self.start_datetime.data:
            self.start_datetime.errors.append("Please provide a start date/time.")
            return False

        if self.is_multi_day.data and not self.end_datetime.data:
            self.end_datetime.errors.append("Please provide an end date/time for multi-day events.")
            return False

        return True
