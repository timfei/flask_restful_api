from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(20))
    # token = db.Column(db.String(20))
    password_hash = db.Column(db.String(100))

    def __repr__(self):
        return 'Id: {}, name: {}'.format(self.id, self.username)

# # init user schema
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = {'id', 'username', 'phone', 'password', 'token'}


# user_schema = UserSchema()
# users_schema = UserSchema(many= True)
