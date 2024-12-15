from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, StringField, PasswordField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_name = EmailField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    user_name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    contact_num = StringField('Contact Number', validators=[DataRequired()])
    conf_password = PasswordField('Confrim Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    role = RadioField("Role", choices=[(1, "Admin"), (2,  "Service_Pro"), (3, "Customer")], validators=[DataRequired()])

class CreateServiceProForm(FlaskForm):
    desc = StringField('Description', validators=[DataRequired()])
    serv_id = IntegerField('Service Offered', validators=[DataRequired()])
    experience = IntegerField('Experience(in years)',  validators=[DataRequired()])
    service_area_pin_code = IntegerField('Pin code for services',  validators=[DataRequired()]) #add a custom validator for correct pincodes 

class CustomerRegisterationForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    pin_code = IntegerField('Pin code for services',  validators=[DataRequired()])

class CreateServiceForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    desc = StringField('desc', validators=[DataRequired()])
    base_price = StringField('base_price', validators=[DataRequired()])
    min_time = StringField('min_time', validators=[DataRequired()])

class UpdateService(FlaskForm):
    name = StringField('name')
    desc = StringField('desc')
    base_price = StringField('base_price')
    min_time = StringField('min_time')
    
class CloseServiceForm(FlaskForm):
    ext_cost = StringField('Extra Cost')

class FeedbackForm(FlaskForm):
    feedbackRating = StringField('FeedbackRating', validators=[DataRequired()])
    feedback = StringField('Feedback')

class ServiceRqstForm(FlaskForm):
    service_msg = StringField('service_msg')