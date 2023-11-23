from flask import render_template
from flask import redirect
from flask import flash
from flask import session
from flask import request
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, SearchForm, NewNoteButton, EditNoteButton, Editbox
from app.models import User, Note, Table
from app import myapp_obj
from app import db

@myapp_obj.route("/")
def index():
		return render_template('index.html')

@myapp_obj.route("/home")
def home():
		return render_template('home.html')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		found_user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
		if found_user:
			session['user'] = form.username.data
			print('you logged in! it worked!')
			return redirect('/home')
		else:
			return redirect('/createaccount')
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

@myapp_obj.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'user' in session:
		user = session['user']
		newnote = NewNoteButton() 
		editbutton = EditNoteButton()
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id

		note_list = {}
		found_id = Note.query.filter_by(user_id = session['id']).all()
		if found_id:
			for note in found_id:
				note_list[f'{note.note_name}'] = (note.note_body, editbutton)

		found_user = User.query.filter_by(id = session['id']).first()
		changeName = updateName()
		changeName.username = found_user.username
		if changeName.validate_on_submit():
			found_user.username = changeName.newname.data
			session['user'] = found_user.username
			db.session.commit()
			return redirect('/profile')

		changePassword = updatePassword()
		changePassword.password = found_user.password
		if changePassword.validate_on_submit():
			found_user.password = changeName.newpassword.data
			db.session.commit()
			return redirect('/profile')
	else:
		return redirect('/login')
	return render_template('profile.html', user=user, note_list=note_list, changeName = changeName, changePassword= changePassword, newnote=newnote)

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
	return render_template('newnote.html', note= note)

@myapp_obj.route('/newtable', methods=['GET', 'POST'])
def newtable():
	if 'user' in session:

		user = session['user']
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id
			
		table = TableParams()
		table_list = {}
		found_id = Table.query.filter_by(user_id = session['id']).all()
		if found_id:
			for dbtable in found_id:
				table_list[f'{dbtable.table_name}'] = (dbtable.numRows, dbtable.numColumns)
		
		if table.validate_on_submit():
			print('table creation')
			u = Table(table_name= table.name.data,  numRows = table.rows.data, numColumns = table.columns.data, user_id = session['id'])
			db.session.add(u)
			db.session.commit()
		
	else:
		return redirect('/login')
	return render_template('newtable.html', table = table, table_list = table_list)

@myapp_obj.route('/editnote/<notename>', methods=['GET', 'POST'])
def editnote(notename):
	if 'user' in session:
		found_user = Note.query.filter_by(note_name=notename).first()
		if found_user:
			editnote = Editbox(note_body=found_user.note_body)

		if editnote.validate_on_submit():
			found_user.note_body = editnote.note_body.data
			print()
			db.session.commit()
			return redirect('/profile')
	return render_template('editnote.html', editnote=editnote)
#function of flask that return dictionary
@myapp_obj.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


  #get data from submitted form 
   #Query the database
    #notes=notes.order_by(Note.note_name).all()
@myapp_obj.route('/search',methods=['GET', 'POST'])
def search():
    form=SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        searched=form.searched.data
        #notes=Note.filter(Note.note_name.like('%'+notes.searched+'%')).all()
        result = Note.query.filter(Note.note_name.like(searched)).all()
        return render_template("search.html",form =form, searched=searched,result=result)
    else:
        return render_template("search.html")
        
    
         