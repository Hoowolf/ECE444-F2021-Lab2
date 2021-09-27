
from flask import Flask, render_template, session, redirect, url_for, flash, request

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField

from wtforms.validators import Required, Email, Regexp





app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):

	name = StringField('What is your name?', validators = [Required()])

	email = StringField('What is your UofT Email address?', validators = [Required(), Regexp('(.*?)@(.*?)', message = 'Please include an \'@\' in the eamil address. The input email is missing an \'@\'')])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	email = None
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		old_email = session.get('email')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name')
		if old_email is not None and old_email != form.email.data:
			flash('Looks like you have changed your email')
		session['name'] = form.name.data
		session['email'] = form.email.data
		return redirect(url_for('index'))
	return render_template('index.html', form = form, name = session.get('name'), email = session.get('email'))


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name = name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug = True)