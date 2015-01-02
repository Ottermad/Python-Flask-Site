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
    If the request method is project then it updates the project based on the id
    with the title and body.

    Template: None
    Redirect: portfolio
    """
    if request.method == "project":
        result = update_project(
            id,
            request.form["title"],
            request.form["body"]
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
    result = delete_project(id)
    flash(result)
    return redirect(url_for("portfolio"))


@app.route("/add_project", methods=["POST", "GET"])
def add_project():
    """Route to add project. The function has two operations based on the request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a project.

    Template: add.html
    Redirect: None

    project method:
    If the request method is project then it adds the project with the title and
    body.

    Template: None
    Redirect: portfolio
    """
    if request.method == "project":
        result = add_project(
            request.form["title"],
            request.form["body"]
        )
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        return render_template("add_project.html")