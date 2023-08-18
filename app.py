from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="school"
)
cursor = db.cursor()

# Email configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_username'
SMTP_PASSWORD = 'your_password'
SENDER_EMAIL = 'your_email@example.com'


def send_confirmation_email(email):
    msg = MIMEText('Your account has been created successfully.')
    msg['Subject'] = 'Account Created'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [email], msg.as_string())
    except Exception as e:
        print("Error sending email:", str(e))

# Routes


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute('INSERT INTO teachers (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        db.commit()

        send_confirmation_email(email)

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM teachers WHERE email = %s AND password = %s', (email, password))
        teacher = cursor.fetchone()

        if teacher:
            return redirect(url_for('dashboard', teacher_id=teacher[0]))

    return render_template('login.html')


@app.route('/dashboard/<int:teacher_id>')
def dashboard(teacher_id):
    cursor.execute('SELECT name FROM teachers WHERE id = %s', (teacher_id,))
    teacher_name = cursor.fetchone()[0]

    return render_template('dashboard.html', teacher_id=teacher_id, teacher_name=teacher_name)


@app.route('/add_student/<int:teacher_id>', methods=['GET', 'POST'])
def add_student(teacher_id):
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        age = request.form['age']

        cursor.execute('INSERT INTO students (teacher_id, name, roll_number, age) VALUES (%s, %s, %s, %s)',
                       (teacher_id, name, roll_number, age))
        db.commit()

        return redirect(url_for('dashboard', teacher_id=teacher_id))

    return render_template('add_student.html', teacher_id=teacher_id)


@app.route('/update_student/<int:teacher_id>', methods=['GET', 'POST'])
def update_student(teacher_id):
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        age = int(request.form['age'])

        cursor.execute('UPDATE students SET name = %s, roll_number = %s, age = %s WHERE teacher_id = %s AND roll_number = %s',
                       (name, roll_number, age, teacher_id, roll_number))
        db.commit()

        return redirect(url_for('dashboard', teacher_id=teacher_id))

    return render_template('update_student.html', teacher_id=teacher_id)


@app.route('/delete_student/<int:teacher_id>', methods=['GET', 'POST'])
def delete_student(teacher_id):
    if request.method == 'POST':
        roll_number = request.form['roll_number']

        cursor.execute('DELETE FROM students WHERE teacher_id = %s AND roll_number = %s', (teacher_id, roll_number))
        db.commit()

        return redirect(url_for('dashboard', teacher_id=teacher_id))

    return render_template('delete_student.html', teacher_id=teacher_id)


@app.route('/show_students/<int:teacher_id>')
def show_students(teacher_id):
    cursor.execute('SELECT name, roll_number, age FROM students WHERE teacher_id = %s', (teacher_id,))
    students = cursor.fetchall()

    return render_template('show_students.html', teacher_id=teacher_id, students=students)


if __name__ == '__main__':
    app.run(debug=True)
