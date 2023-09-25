from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from flask import abort

class User( db.Model ):
    __tablename__ = 'users'

    id = db.Column( db.Integer, primary_key=True )
    first_name = db.Column( db.String )
    last_name = db.Column( db.String )
    email = db.Column( db.String, unique = True )
    password = db.Column( db.Text )

    def authenticate( self, password ):
        return bcrypt.check_password_hash(
            self.password, password.encode( 'utf-8' )
        )