from myapp import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(20), default="")
    username = db.Column(db.String(120),nullable = False, unique=True)
    email = db.Column(db.String(120),nullable = False, unique=True)
    password = db.Column(db.String(80), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    texts = db.Column(db.Text, default="")
    tech = db.Column(db.Text, default="")
    gen = db.Column(db.Text, default="")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
