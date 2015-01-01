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

    This is to keep my code DRY by setting common elements in one place e.g.
    the db
    """
    class Meta:
        database = db


class Post(BaseModel):
    """A model for Posts which have a title and a body"""
    title = CharField()
    body = TextField()


# Functions


def setup_db():
    """Function to connect to db and create tables"""
    db.connect()
    db.create_tables([Post])


def add_post(title, body):
    """Function to create a new post

    Parameters:
    title - string -title for the posts
    body - string - main content of the post

    Returns Success if post creation is successful or Error if not.
    """
    try:
        new_post = Post(title=title, body=body)
        new_post.save()
        return "Success"
    except:
        return "Error"


def get_posts():
    """Function to get all posts from db

    Parameters
    None

    Returns a list of dictionaries. The dictionaries will be in the following
    have an id, title and body
    """
    posts = []
    for post in Post.select():
        post_dict = {
            "id": post.id,
            "title": post.title,
            "body": post.body
        }
        posts.append(post_dict)
    return posts


def get_post(id):
    """Function to get an indiviual post from an id.

    Parameters
    id - int - id for a post

    It searches for the post with corrosponding id and returns a dictionary
    with the id, title and body of the post.
    """
    post_dict = {}
    post = Post.get(Post.id == id)
    post_dict = {
        "id": post.id,
        "title": post.title,
        "body": post.body
    }
    return post_dict


def update_post(id, title, body):
    """Function to update a post

    Parameters
    id - int - id for post to update
    title - string - new title for post
    body - string - new body for post

    It searches for the post with the matching id. Then updates the title and
    body.
    """
    try:
        post = Post.get(Post.id == id)
        post.title = title
        post.body = body
        post.save()
        return "Success"
    except:
        return "Error"


def delete_post(id):
    """Function to delete a post

    Parameters
    id - int - id for post to delete

    It searches for the post with the matching id then deletes it.
    """
    try:
        post = Post.get(Post.id == id)
        post.delete_instance()
        return "Success"
    except:
        return "Error"
