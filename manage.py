from app import app
from database import db

# This is the file that will be used to create the tables in the database
def create_tables():
    with app.app_context():
        db.create_all()

# This is the file that will be used to drop the tables in the database
def drop_tables():
    with app.app_context():
        db.drop_all()

if __name__ == '__main__':
    drop_tables()
    create_tables()