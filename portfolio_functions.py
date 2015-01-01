def add_project(title, description):
    """Function to create a new project

    Parameters:
    title - string -title for the project
    description - string - description of the project

    Returns Success if project creation is successful or Error if not.
    """
    try:
        new_project = project(title=title, body=body)
        new_project.save()
        return "Success"
    except:
        return "Error"


def get_projects():
    """Function to get all projects from db

    Parameters
    None

    Returns a list of dictionaries. The dictionaries will be in the following
    have an id, title and body
    """
    projects = []
    for project in project.select():
        project_dict = {
            "id": project.id,
            "title": project.title,
            "body": project.body
        }
        projects.append(project_dict)
    return projects


def get_project(id):
    """Function to get an indiviual project from an id.

    Parameters
    id - int - id for a project

    It searches for the project with corrosponding id and returns a dictionary
    with the id, title and body of the project.
    """
    project_dict = {}
    project = project.get(project.id == id)
    project_dict = {
        "id": project.id,
        "title": project.title,
        "body": project.body
    }
    return project_dict


def update_project(id, title, body):
    """Function to update a project

    Parameters
    id - int - id for project to update
    title - string - new title for project
    body - string - new body for project

    It searches for the project with the matching id. Then updates the title and
    body.
    """
    try:
        project = project.get(project.id == id)
        project.title = title
        project.body = body
        project.save()
        return "Success"
    except:
        return "Error"


def delete_project(id):
    """Function to delete a project

    Parameters
    id - int - id for project to delete

    It searches for the project with the matching id then deletes it.
    """
    try:
        project = project.get(project.id == id)
        project.delete_instance()
        return "Success"
    except:
        return "Error"
