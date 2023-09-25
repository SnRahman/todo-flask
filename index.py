from flask import Flask ,render_template , request , redirect, url_for , flash
from mysql import connector


app = Flask(__name__)
app.secret_key = 'todo'

connection = connector.connect(host="localhost",user="root",password='',database='todo') 

@app.route('/')
def index():
    return "Server is running."


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        if not fname:
            flash('Name is required', 'error')
            return redirect(url_for('signup'))

        if not email or  "@" not in email:
            flash('Valid email is required', 'error')
            return redirect(url_for('signup'))
        
        if not password:
            flash('Password is required', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords should match', 'error')
            return redirect(url_for('signup'))

        db = connection.cursor()
        db.execute('INSERT INTO users (fname,lname,email,password) VALUES(%s,%s,%s,%s)',(fname,lname,email,password))
        
        connection.commit()
        db.close()
        flash('Signup Successfully!', 'success')
        return redirect(url_for('signup'))
    else:
        flash('Only Post type is allowed for signup', 'error')
        return redirect(url_for('signup'))


@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        
        if not email or  "@" not in email:
            flash('Valid email is required', 'error')
            return redirect(url_for('login'))

        if not password:
            flash('Password is required', 'error')
            return redirect(url_for('login'))
        
        db = connection.cursor()
        # db.execute(f'SELECT * FROM users WHERE email = {email} and password = {password}')
        db.execute('SELECT * FROM users WHERE email = %s and password = %s',(email, password))
        result = db.fetchone()
        db.close()

        if result:
            flash('Login Successfully!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Credentials does\'t matched!', 'error')
            return redirect(url_for('login'))


@app.route('/todo')
def todo():
    db = connection.cursor()
    db.execute('SELECT * FROM todos')
    todos = db.fetchall()
    db.close()

    return render_template('todo.html', current_todos = todos)


@app.route('/create-todo', methods =['POST'])
def create_todo():
    if request.method == 'POST':
        description = request.form['description']

        if description:
            db = connection.cursor()
            db.execute('INSERT INTO todos (description) VALUES (%s) ',(description,))
            connection.commit()
            db.close()
            flash('Todo is added', 'success')
            return redirect(url_for('todo'))
        else:
            flash('Kindly enter Something', 'error')
            return redirect(url_for('todo'))


@app.route('/delete-todo/<id>')
def delete_todo(id):
    db = connection.cursor()
    # db.execute('DELETE FROM users WHERE id = %s',(id))
    db.execute(f'DELETE FROM todos WHERE id = {id}')
    connection.commit()
    db.close()
    flash('Todo is deleted', 'success')
    return redirect(url_for('todo'))

if __name__ == '__main__':
    app.debug = True
    app.run()