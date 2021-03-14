from flask import render_template, request, redirect, url_for, flash, make_response
from myapp.database import User
from myapp.forms import LoginForm, MainForm, RegistrationForm,ChangePasswordForm,RequestResetForm, ResetPasswordForm
from myapp import app, bcrypt, db, mail
from flask_login import login_user, current_user, logout_user, login_required
from myapp.dataprep import split, parse
import json
from myapp.generator import generate
from myapp.picworks import save_pic, delete_pic, get_pic_string, check_pic
from flask_mail import Message

help_data = [
    {
        'title': 'Structure',
'date': '11.03.2021',
        'contents': 'You can see that document is laid out to include many different details (like Agent data, or hospitality, etc).'
                    ' You obviously may not have an Agent, or you perform in your own town, so leave unnecessary fields empty.'
                    ' If you encounter errors when generating pdf - please send me an email so that I could correct them!'

    },
    {
        'title': 'Colors',
        'contents': 'A funny feature that I had some time to implement was to generate colors from your picture. IMO, this is the best way to get your pdf to look fine,'
                    ' because colors are directly linked to your picture, '
                    'thus reflecting your taste. Plus, they are partially randomised, so you may try multiple times'
                    ' to get what you want. You can also build Riders without picture, which is fine, but the colors are then going to default'
                    ' to few of the basic color schemes, which I was not particularly good at.'
    },
    {
        'title': 'Generation',
        'contents': 'Using templates like this sure has few drawbacks (it saves hours, if not days, though). For instance, I dont know how good pdf is going to look when you use'
                    ' extremely long names, or fill each and every piece with huge texts. You should understand that the data you fill in there is not really checked or filtered. So, few basic tips are:\n'
                    '1) do not try to list each and every detail, you may always come back and edit the document, but for now, stick to something relevant;\n'
                    '2) Long Names may not display well. You can easily write "Xone92" instead of "AlennHeath blablabla mk2 rev2018";\n'
                    '3) Check your spelling! I must have broken this rule in here multiple times;\n'
                    '4) I suggest that you try to fit everything in one page;\n'
                    '5) Although I have no commercial interest, and do not plan on building this exact tool'
                    ' into something BIG, feel free to send me an email if interested in cooperation, or have errors for me to fix!\n'
                    'If you want to improve your own skills by building interesting designs, or maybe improving the service - you are very welcome to do so, but atm I can not offer you any money.\n '
                    'vania.stankov@gmail.com'
    }

]

about_data = [
    {
        'title': 'What?',
        'date': '11.03.2021',
        'contents': 'This resource is designed to help aspiring DJs, live artists, or even bands to get proper riders for their performances.\n'
                    'Although I have some experience myself, it had always been unclear, how to write technical and/or hospitality rider properly.\n'
                    'After spending some time reading professional riders I came up with an idea to have a template based rider generator,'
                    ' that would help all artists build a unified document, that would contain all necessary details and also act as a guide.'
                    ' Promoters, on the other hand, will have an opportunity to work with readable, structurized documents, therefore not wasting time scrolling through messages or whatever.'
    },
    {
        'title': 'Why?',
        'contents': 'I found out that there are not many resources like that online, plus I really wanted to understand main principles behind web development.\n '
                    'The App itself is based upon Flask Framework for Python, which is then supplemented with PDFKit for PDF generation, JSON parser and Image handlers.\n'
                    'The target audience here is definitely shifted towards young artists.\n'
                    'Feel free to get in touch via email: vania.stankov@gmail.com'
    }
]


@app.route("/", methods=['GET'])
def slip():
    return redirect(url_for('main'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('main'))
    title = "Login"
    meta_description = "Please Login to build your own Technical/Hospitality Rider." \
                       " You may try multiple times to achieve best results, so login system is necessary"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('main'))
        else:
            flash('Login Error', 'danger')
    return render_template('login.html', title=title, form=form, meta_description = meta_description)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('main'))
    title = "Register"
    meta_description = "DJs, Live Musicians and Booking Agents are welcome to use this tool." \
                       " You can build nice PDF Riders for free, but you have to Register."
    form = RegistrationForm()
    if request.method == "GET":
        flash('You are probably going to rebuild the document multiple times,'
              ' so I have to store your data somehow. It is not used anywhere and you will have an opportunity'
              ' to completely delete yourself after you are done.', 'info')
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f'User {user} created', 'success')
        return redirect(url_for('main'))
    return render_template('register.html', title=title, form=form, meta_description = meta_description)


@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    title = "Main Rider Creation Page"
    meta_description = "Using simple form you can create well-arranged PDF Technical/Hospitality Rider." \
                       " Even on the go!"
    form = MainForm()
    devices = {}
    descriptions = {}
    if request.method == 'GET':
        parse(form, current_user)
        if current_user.tech:
            json_dict = json.loads(current_user.tech)
            devices = list(json_dict.keys())
            descriptions = list(json_dict.values())
        if check_pic(current_user.pic):
            return render_template('main.html', pic=get_pic_string(current_user.pic), title=title,
                                   meta_description= meta_description,
                                   form=form, dev=devices, des=descriptions)
        else:
            return render_template('main.html', title=title, meta_description= meta_description, form=form, dev=devices, des=descriptions)
    if request.method == 'POST':
        if form.validate():
            if form.picture.data:
                delete_pic(current_user.pic)
                new_pic = save_pic(form.picture.data)
                User.query.filter_by(id=current_user.id).update({User.pic: new_pic})
                db.session.commit()
            gen, dev, texts = split(request.form.to_dict())
            if current_user.pic and form.usepicture.data:
                pdf = generate(gen, dev, texts, pic=current_user.pic)
            else:
                pdf = generate(gen, dev, texts)
            gen = json.dumps(gen)
            dev = json.dumps(dev)
            texts = json.dumps(texts)
            User.query.filter_by(id=current_user.id).update({User.gen: gen, User.tech: dev, User.texts: texts})
            db.session.commit()
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline/filename= {}.pdf'.format(current_user.id)
            return response
        else:
            if check_pic(current_user.pic):
                return render_template('main.html', pic=get_pic_string(current_user.pic), title=title, meta_description= meta_description, form=form,
                                       dev=[], des=[])
            else:
                return render_template('main.html', title=title,meta_description= meta_description, form=form, dev=[], des=[])


@app.route("/about")
def about():
    title = "How To Create Rider"
    meta_description = "THRider allows you to create your own Technical and/or Hospitality Riders." \
                       " You can additionally learn the structure of the document here."
    return render_template('static.html', title=title, meta_description=meta_description, data=about_data)


@app.route("/help")
def help():
    title = "Tips/Hints and Feedback"
    meta_description = "To generate PDF you simply have to fill the form." \
                       " However, not all fields have to be filled, here you can find an advice."
    return render_template('static.html', title=title, meta_description=meta_description, data=help_data)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(f'LOGED OUT', 'success')
    return redirect(url_for('login'))


@app.route("/delete", methods=['GET', 'POST'])
@login_required
def delete():
    delete_pic(current_user.pic)
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash(f'User deleted', 'success')
    return redirect(url_for('login'))


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    title = "Change Password"
    meta_description = "Change Password Here."
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User.query.get(current_user.id)
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                User.query.filter_by(id=current_user.id).update({User.password: new_hashed_password})
                db.session.commit()
                logout_user()
                flash(f'Password Changed Successfully', 'success')
                return redirect(url_for('login'))
            else:
                flash(f'An Error Occurred. You Might Have Typed a Wrong Password', 'warning')
    return render_template('change_password.html', title=title, meta_description=meta_description, form=form)





@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    title = "Reset Password"
    meta_description = "Ask for Password reset email if you forgot original."
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title= title, meta_decsription=meta_description, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.

Best,
THRider
'''
    mail.send(msg)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    title = "Password Reset"
    meta_description = "Reset Password Here."
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title=title, meta_description=meta_description, form=form)

