# Main file for blog


# Import statements
from flask import (
    Flask,
    render_template,
    redirect,
    Markup,
    request,
    flash,
    url_for,
    session,
    jsonify
)
from db_functions import (
    get_posts,
    get_post,
    add_post,
    update_post,
    delete_post,
    get_projects,
    get_project,
    add_project as add_project_to_db,
    update_project as update_project_to_db,
    delete_project as delete_project_to_db
)
import markdown
import sendgrid

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"
app.config["USERNAME"] = "charliethomas"
app.config["PASSWORD"] = "my_password"


# Routes


@app.route("/")
@app.route("/show")
def show():
    """Main Page for blog. It shows all the posts from the db.

    Parameters:
    None

    Template: show.html
    Redirect: None
    """
    context = {
        "posts": get_posts()[::-1]
    }
    return render_template("show.html", **context)


@app.route("/post/<id>")
def post(id):
    """Page for each post. It shows the title and body of a given post.

    Parameters:
    id - init - id for post to view

    Template: post.html
    Redirect: None
    """
    post = get_post(id)
    title = post["title"]
    body = post["body"]
    unicode_body = body.decode("utf-8")
    html_body = markdown.markdown(unicode_body)
    safe_html_body = Markup(html_body)
    context = {
        "title": title,
        "body": safe_html_body
    }
    return render_template("post.html", **context)


@app.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    """Route to update post the function has two operations based on the
    request method.

    Parameters:
    id - init - id for post to update

    GET method:
    If the request method is GET it loads the form to update the post.

    Template: edit.html
    Redirect: None

    POST method:
    If the request method is POST then it updates the post based on the id
    with the title and body.

    Template: None
    Redirect: show
    """
    if request.method == "POST":
        result = update_post(
            id,
            request.form["title"],
            request.form["body"]
        )
        flash(result)
        return redirect(url_for("show"))
    else:
        post = get_post(id)
        return render_template("edit.html", **post)


@app.route("/delete/<id>")
def delete(id):
    """Route to delete post from id.

    Parameters:
    id - int - id for post to delete

    Template: None
    Redirect: show
    """
    result = delete_post(id)
    flash(result)
    return redirect(url_for("show"))


@app.route("/add", methods=["POST", "GET"])
def add():
    """Route to add post. The function has two operations based on the request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a post.

    Template: add.html
    Redirect: None

    POST method:
    If the request method is POST then it adds the post with the title and
    body.

    Template: None
    Redirect: show
    """
    if request.method == "POST":
        result = add_post(
            request.form["title"],
            request.form["body"]
        )
        flash(result)
        return redirect(url_for("show"))
    else:
        return render_template("add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Route to login. The function has two operations based on the request
    method

    GET method:
    If the request method is GET it loads the form to login.

    Template: login.html
    Redirect: None

    POST method:
    If the request method is POST then it trys tp log the user in. If login
    errors it returns an errors back to login.html. If login is successful
    it redirects to show.

    Template: None
    Redirect: show
    """
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in sucessfully")
            return redirect(url_for("show"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """Route to logout.

    Parameters:
    None

    Template: None
    Redirect: show
    """
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("show"))


@app.route("/about")
def about():
    """Route for about page"""
    return render_template("about.html")


@app.route("/portfolio")
def portfolio():
    """Route for portfolio page"""
    projects = get_projects()
    for project in projects:
        unicode_body = project["description"].decode("utf-8")
        html_body = markdown.markdown(unicode_body)
        safe_html_body = Markup(html_body)
        project["description"] = safe_html_body
    context = {
        "projects": projects
    }
    return render_template("portfolio.html", **context)


@app.route("/update_project/<id>", methods=["POST", "GET"])
def update_project(id):
    """Route to update project the function has two operations based on the
    request method.

    Parameters:
    id - init - id for project to update

    GET method:
    If the request method is GET it loads the form to update the project.

    Template: edit.html
    Redirect: None

    project method:
    If the request method is project then it updates the project based on the
    id with the title and body.

    Template: None
    Redirect: portfolio
    """
    if request.method == "POST":
        result = update_project_to_db(
            id,
            request.form["title"],
            request.form["link"],
            request.form["description"]
        )
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        project = get_project(id)
        return render_template("edit_project.html", **project)


@app.route("/delete_project/<id>")
def delete_project(id):
    """Route to delete project from id.

    Parameters:
    id - int - id for project to delete

    Template: None
    Redirect: portfolio
    """
    result = delete_project_to_db(id)
    flash(result)
    return redirect(url_for("portfolio"))


@app.route("/add_project", methods=["POST", "GET"])
def add_project():
    """Route to add project. The function has two operations based on the
    request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a project.

    Template: add.html
    Redirect: None

    POST method:
    If the request method is project then it adds the project with the title
    and body.

    Template: None
    Redirect: portfolio
    """
    if request.method == "POST":
        result = add_project_to_db(
            request.form["title"],
            request.form["link"],
            request.form["description"]
        )
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        return render_template("add_project.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        sendgrid_object = sendgrid.SendGridClient(
            "Ottermad", "OttersR0ck")
        message = sendgrid.Mail()
        sender = request.form["email"]
        subject = request.form["name"]
        body = request.form["body"]
        message.add_to("charlie.thomas@attwoodthomas.net")
        message.set_from(sender)
        message.set_subject(subject)
        message.set_html(body)
        sendgrid_object.send(message)
        flash("Email sent.")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html")

@app.route("/post_json", methods=["POST","GET"])
def post_json():
    posts = get_posts()[::-1]
    return jsonify(results=posts)

if __name__ == "__main__":
    app.run(debug=True)
