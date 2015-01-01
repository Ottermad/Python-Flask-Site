from flask import *
from db_functions import *
import markdown

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"
app.config["USERNAME"] = "charliethomas"
app.config["PASSWORD"] = "my_password"

@app.route("/")
@app.route("/show")
def show():
	context = {
		"posts": get_posts()[::-1]
	}
	return render_template("show.html", **context)

@app.route("/post/<id>")
def post(id):
	post = get_post(id) 
	title =  post["title"]
	body = post["body"]
	unicode_body = body.decode("utf-8")
	html_body = markdown.markdown(unicode_body)
	safe_html_body = Markup(html_body)
	context = {
		"title": post["title"],
		"body": safe_html_body
	}
	return render_template("post.html", **context)


@app.route("/update/<id>", methods=["POST", "GET"])
def update(id):
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
		return render_template("update.html", **post)


@app.route("/delete/<id>")
def delete(id):
	result = delete_post(id)
	flash(result)
	return redirect(url_for("show"))

@app.route("/add", methods=["POST", "GET"])
def add():
	if request.method == "POST":
		result = add_post(
			request.form["title"],
			request.form["body"]
		)
		flash(result)
		return redirect(url_for("show"))
	else:
		return render_template("add.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in sucessfully')
			return redirect(url_for('show'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show'))


if __name__ == "__main__":
	app.run(debug=True)
