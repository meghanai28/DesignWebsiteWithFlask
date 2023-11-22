from flask import render_template
from flask import redirect
from flask import flash
from flask import session
from flask import request
from .forms import CreateAccountForm, LoginForm, Notebox, NewNoteButton, EditNoteButton, Editbox
from app.models import User, Note
from app import myapp_obj
from app import db
from wtforms.widgets import TextArea

@myapp_obj.route("/")
def index():
		return render_template('index.html')

@myapp_obj.route("/home")
def home():
		return render_template('base.html')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		found_user = User.query.filter_by(username=form.username.data).first()
		if found_user:
			session['user'] = form.username.data
			print('you logged in! it worked!')
		else:
			redirect('/createaccount')
	return render_template('login.html', form=form)

@myapp_obj.route('/logout')
def logout():
	session.pop("user", None)
	return redirect('/login')

@myapp_obj.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    form = CreateAccountForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('do something')
        print(f'this is the username of the user {form.username.data}')
        print(f'this is the password of the user {form.password.data}')
        u = User(username=form.username.data, password=form.password.data,
                 email=form.email.data)
        db.session.add(u)
        db.session.commit()
        return redirect('/')

    return render_template('createaccount.html', form=form)

@myapp_obj.route("/profile", methods=['POST', 'GET'])
def profile():
	if 'user' in session:
		newnote = NewNoteButton()
		editnote = EditNoteButton()
		user = session['user']

		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id

		note_list = {}
		num = 0
		found_id = Note.query.filter_by(user_id = session['id']).all()
		if found_id:
			for note in found_id:
				note_list[note.note_name] = (note.note_body)
		
	else:
		return redirect('/login')
	return render_template('profile.html', user=user, note_list=note_list,newnote=newnote,editnote=editnote)

@myapp_obj.route('/newnote', methods=['GET', 'POST'])
def newnote():
	if 'user' in session:
		note = Notebox()
		if note.validate_on_submit():
			print('you submitted your note!')
			found_user = User.query.filter_by(username=session['user']).first()
			u = Note(note_body = note.note_body.data, note_name = note.note_name.data, owner=found_user)
			db.session.add(u)
			db.session.commit()
			return redirect('/profile')
	else:
		return redirect('/login')
	return render_template('newnote.html', note=note)

@myapp_obj.route('/editnote', methods=['GET', 'POST'])
def editnote():
	if 'user' in session:
		found_user = Note.query.filter_by(id = 1).first()
		if found_user:
			editnote = Editbox(note_body=found_user.note_body)

		if editnote.validate_on_submit():
			found_user.note_body = editnote.note_body.data
			print()
			db.session.commit()
			return redirect('/profile')
		
	return render_template('editnote.html', editnote=editnote)






