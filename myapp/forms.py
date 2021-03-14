from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed
from myapp.database import User


class MainForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])],
                        render_kw = {"onchange": "imageView()"} )
    usepicture = BooleanField("Use Picture?", default= True)
    name = StringField("Name ", validators=[validators.DataRequired(), validators.Length(max = 100)],
                       render_kw={"placeholder": "Artist Name"})
    email = EmailField('Email address',validators=[validators.DataRequired(), validators.Length(max = 100)],
                       render_kw={"placeholder": "Artist Email"})
    phone = StringField('Phone', validators=[validators.DataRequired(), validators.Length(max = 100)],
                        render_kw={"placeholder": "Artist Phone Number"})
    aname = StringField("Agent Name: ", validators=[validators.Length(max = 100)],
                        render_kw={"placeholder": "Agent Name"})
    aemail = EmailField('Agent Email', validators=[validators.Length(max = 100)],
                        render_kw={"placeholder": "Agent Email"})
    aphone = StringField('Agent Phone',validators=[validators.Length(max = 100)],
                         render_kw={"placeholder": "Agent Phone"})
    device = StringField("devices",validators=[validators.DataRequired(),validators.Length(max = 100)],
                         render_kw={"onmouseup": "addDevice(this.id)", "placeholder": "Device Name"})
    device_description = StringField("dDescriptions", validators=[validators.Length(max = 500)], render_kw={"placeholder": "Device Notes"})
    t = TextAreaField("dComments",validators=[validators.Length(max = 1000)], render_kw={"placeholder": "Tech Notes", 'rows': 3})
    h = TextAreaField("hospitality",validators=[validators.Length(max = 1000)], render_kw={"placeholder": "Hospitality and Accommodation Requirements",
                                                    'rows': 5})
    p = TextAreaField("pay",validators=[validators.Length(max = 1000)], render_kw={"placeholder": "Force majeure and Pay",
                                                    'rows': 5})
    submit = SubmitField("Build")


class LoginForm(FlaskForm):
    email = EmailField('Email address', validators = [validators.Length(max = 200),validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators = [validators.Length(max = 200),validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Name: ", validators=[validators.Length(max = 200), validators.DataRequired()])
    email = EmailField('Email address', validators = [validators.Length(max = 200), validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators = [validators.Length(max = 200),validators.DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[validators.Length(max = 200),validators.DataRequired(), validators.EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self,email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise validators.ValidationError(f'User with email {email.data} already exists')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise validators.ValidationError(f'User with username {username.data} already exists')


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Old Password", validators=[validators.Length(max = 200),validators.DataRequired()])
    new_password = PasswordField("New Password", validators=[validators.Length(max = 200),validators.DataRequired()])
    submit = SubmitField("Change Password")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[validators.Length(max = 200), validators.DataRequired(), validators.Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise validators.ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[validators.Length(max = 200),validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.Length(max = 200),validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Reset Password')