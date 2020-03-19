from app import db

class Todo(db.Model):
    __tablename__ = 'todo'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


    def __init__(self, name ,description):
        self.name = name
        self.description = description

class TodoSchema(ma.Schema):
    class Meta:
        fields = {'name', 'description'}


todo_schema = TodoSchema()
todos_schmea = TodoSchema(many = True)

