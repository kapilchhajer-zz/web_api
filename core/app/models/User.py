from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=True)
    email = db.Column('email', db.String(100), unique=True, nullable=True)
    password = db.Column('password', db.String(100), unique=True, nullable=True)
    profile_url = db.Column('profile_url', db.String(100), nullable=True)
    created_on = db.Column(
        'created_on', db.TIMESTAMP, default=db.text('now()'))

    def as_dict(self):
        return model_helpers.as_dict(self)
