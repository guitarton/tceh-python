from blog_db import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False, unique=True)
    content = db.Column(db.String(3000), nullable=False)
    is_visible = db.Column(db.Boolean)

    def __init__(self, title, content, is_visible):
        self.title = title
        self.content = content
        self.is_visible = True
