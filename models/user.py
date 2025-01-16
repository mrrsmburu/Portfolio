from extensions import db

class User(db.Model):
    __bind_key__ = None
    __table_args__ = {'extend_existing': True}  # Add this line to handle duplicate table definition
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message
        }