from app import app
from database import db
from models import User, Video
from datetime import datetime

# This is the code that will be used to create the tables in the database
def create_tables():
    with app.app_context():
        db.create_all()

# This is the code that will be used to drop the tables in the database
def drop_tables():
    with app.app_context():
        db.drop_all()

# Insert New Record to Video
def new_video(user_id,title,url,views,likes,dislikes,score,word):
    new_video = Video()
    new_video.title = title
    new_video.url = url
    new_video.views = views
    new_video.likes = likes
    new_video.dislikes = dislikes
    new_video.score = score
    new_video.word = word
    new_video.date = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = User.query.get(user_id)
    user.videos.append(new_video)
    db.session.commit()
    
if __name__ == '__main__':
    drop_tables()
    create_tables()