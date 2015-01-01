from peewee import (
    MySQLDatabase,
    CharField,
    TextField,
    Model,
)

db = MySQLDatabase("BLOG_DB", user="root", passwd="OttersR0ck")

# Models


class BaseModel(Model):
    """A model/class to act as a base for other models.

    This is to keep my code DRY by setting common elements in one place
    e.g. the db
    """
    class Meta:
        database = db


class Post(BaseModel):
    """A model for Posts which have a title and a body"""
    title = CharField()
    body = TextField()


# Functions


def setup_db():
    db.connect()
    db.create_tables([Post])


def add_post(title, body):
    try:
        new_post = Post(title=title, body=body)
        new_post.save()
        return "Success"
    except:
       return "Error"


def get_posts():
    posts = []
    for post in Post.select():
        print post, post.id, post.title, post.body
        post_dict = {
            "id": post.id,
            "title": post.title,
            "body": post.body
        }
        posts.append(post_dict)
    return posts


def get_post(id):
    post_dict = {}
    post = Post.get(Post.id == id)
    post_dict = {
        "id": post.id,
        "title": post.title,
        "body": post.body
    }
    return post_dict


def update_post(id, title, body):
    try:
        post = Post.get(Post.id == id)
        post.title = title
        post.body = body
        post.save()
        return "Success"
    except:
        return "Error"


def delete_post(id):
    try:
        post = Post.get(Post.id == id)
        post.delete_instance()
        return "Success"
    except:
        return "Error"

