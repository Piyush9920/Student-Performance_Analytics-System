from flask import Flask, render_template, request, redirect, Response, session, send_file
import sqlite3
import os
import qrcode
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from io import BytesIO, StringIO
import csv
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "studentanalytics"

# =========================
# CREATE DATABASE
# =========================

conn = sqlite3.connect('students.db')

cursor = conn.cursor()

# CREATE TABLE

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        course TEXT,
        marks INTEGER,

        ai INTEGER DEFAULT 0,
        ml INTEGER DEFAULT 0,
        dsa INTEGER DEFAULT 0,
        python INTEGER DEFAULT 0,
        algorithm INTEGER DEFAULT 0,

        photo TEXT
    )
    '''
)

# ADD COLUMNS IF DATABASE IS OLD

try:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN ai INTEGER DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN ml INTEGER DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN dsa INTEGER DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN python INTEGER DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN algorithm INTEGER DEFAULT 0"
    )
except:
    pass

conn.commit()

conn.close()
# =========================
# HOME PAGE
# =========================

@app.route('/')

@app.route('/home')
def home():

    if 'user' not in session:

        return redirect('/login')

    return render_template('index.html')
# =========================
# LOGIN PAGE
# =========================

@app.route('/login')
def login():

    return render_template(
        'login.html'
    )

# =========================
# LOGIN CHECK
# =========================

@app.route('/login_check', methods=['POST'])
def login_check():

    username = request.form['username']

    password = request.form['password']

    if username == "admin" and password == "admin123":

        session['user'] = username

        return redirect('/home')

    else:

        return """

        <h1>

            Invalid Username or Password

        </h1>

        <a href='/login'>

            Back

        </a>

        """

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')

# =========================
# ATTENDANCE SYSTEM
# =========================

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():

    if request.method == 'POST':

        name = request.form['name']

        status = request.form['status']

        return f"""

        <!DOCTYPE html>

        <html>

        <head>

            <title>Attendance Success</title>

            <style>

                body{{
                    font-family:Arial;
                    background:#0f172a;
                    color:white;
                    text-align:center;
                    padding-top:100px;
                }}

                .box{{
                    width:500px;
                    margin:auto;
                    background:white;
                    color:black;
                    padding:40px;
                    border-radius:15px;
                }}

                h1{{
                    color:green;
                }}

                a{{
                    display:inline-block;
                    margin-top:20px;
                    background:#2563eb;
                    color:white;
                    padding:12px 25px;
                    text-decoration:none;
                    border-radius:10px;
                }}

            </style>

        </head>

        <body>

            <div class='box'>

                <h1>

                    Attendance Submitted Successfully

                </h1>

                <h2>

                    Student Name : {name}

                </h2>

                <h2>

                    Status : {status}

                </h2>

                <a href='/attendance'>

                    Back To Attendance

                </a>

            </div>

        </body>

        </html>

        """

    return render_template(
        'attendance.html'
    )

# =========================
# RESULT PREDICTION
# =========================

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():

    if request.method == 'POST':

        name = request.form['name']

        marks = int(request.form['marks'])

        if marks >= 40:

            result = "PASS"

        else:

            result = "FAIL"

        return f"""

        <!DOCTYPE html>

        <html>

        <head>

            <title>Prediction Result</title>

            <style>

                body{{
                    font-family:Arial;
                    background:#0f172a;
                    color:white;
                    text-align:center;
                    padding-top:100px;
                }}

                .box{{
                    width:500px;
                    margin:auto;
                    background:white;
                    color:black;
                    padding:40px;
                    border-radius:15px;
                }}

                h1{{
                    color:#2563eb;
                }}

                h2{{
                    margin-top:20px;
                }}

                a{{
                    display:inline-block;
                    margin-top:25px;
                    background:#2563eb;
                    color:white;
                    padding:12px 25px;
                    text-decoration:none;
                    border-radius:10px;
                }}

            </style>

        </head>

        <body>

            <div class="box">

                <h1>

                    AI Result Prediction

                </h1>

                <h2>

                    Student Name : {name}

                </h2>

                <h2>

                    Marks : {marks}

                </h2>

                <h2>

                    Predicted Result : {result}

                </h2>

                <a href="/prediction">

                    Back

                </a>

            </div>

        </body>

        </html>

        """

    return render_template(
        'result.html'
    )

# =========================
# EMAIL NOTIFICATION
# =========================

@app.route('/email')
def email():

    return render_template(
        'email.html'
    )
# =========================
# SEND EMAIL
# =========================

@app.route('/send_email', methods=['POST'])
def send_email():

    student_name = request.form['name']

    student_email = request.form['email']

    message = request.form['message']

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

        <title>Email Sent</title>

        <style>

            body{{
                font-family:Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding-top:100px;
            }}

            .box{{
                width:550px;
                margin:auto;
                background:white;
                color:black;
                padding:40px;
                border-radius:15px;
            }}

            h1{{
                color:green;
            }}

            a{{
                display:inline-block;
                margin-top:25px;
                background:#2563eb;
                color:white;
                padding:12px 25px;
                text-decoration:none;
                border-radius:10px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h1>

                Email Sent Successfully

            </h1>

            <h2>

                Student : {student_name}

            </h2>

            <h2>

                Email : {student_email}

            </h2>

            <p>

                {message}

            </p>

            <a href="/email">

                Back

            </a>

        </div>

    </body>

    </html>

    """

# =========================
# ADD STUDENT
# =========================

@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']

    roll = request.form['roll']

    course = request.form['course']

    marks = request.form['marks']

    photo = request.files['photo']

    filename = photo.filename

    upload_folder = os.path.join(
        app.root_path,
        'static',
        'uploads'
    )

    if not os.path.exists(upload_folder):

        os.makedirs(upload_folder)

    photo.save(
        os.path.join(upload_folder, filename)
    )

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO students(
            name,
            roll,
            course,
            marks,
            photo
        )
        VALUES(?,?,?,?,?)
        ''',
        (
            name,
            roll,
            course,
            marks,
            filename
        )
    )

    conn.commit()

    conn.close()

    return redirect('/students')

# =========================
# VIEW STUDENTS
# =========================

@app.route('/students')
def students():

    search = request.args.get('search')

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    if search:

        cursor.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
            OR roll LIKE ?
            """,
            (
                '%' + search + '%',
                '%' + search + '%'
            )
        )

    else:

        cursor.execute(
            "SELECT * FROM students"
        )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )

# =========================
# PROFILE PAGE
# =========================

@app.route('/profile/<int:id>')
def profile(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'profile.html',
        student=student
    )

# =========================
# ID CARD
# =========================

@app.route('/idcard/<int:id>')
def idcard(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'idcard.html',
        student=student
    )

# =========================
# QR CODE
# =========================

@app.route('/qrcode/<int:id>')
def qrcode_generate(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    data = f"""
    Student ID : {student[0]}
    Name : {student[1]}
    Roll : {student[2]}
    Course : {student[3]}
    Marks : {student[4]}
    """

    qr = qrcode.make(data)

    qr_folder = os.path.join(
        app.root_path,
        'static',
        'qrcodes'
    )

    if not os.path.exists(qr_folder):

        os.makedirs(qr_folder)

    filename = f"{student[0]}.png"

    qr.save(
        os.path.join(qr_folder, filename)
    )

    return render_template(
        'qrcode.html',
        filename=filename
    )

# =========================
# EDIT STUDENT
# =========================

@app.route('/edit/<int:id>')
def edit(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit.html',
        student=student
    )

# =========================
# UPDATE STUDENT
# =========================

@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    name = request.form['name']

    roll = request.form['roll']

    course = request.form['course']

    marks = request.form['marks']

    ai = request.form['ai']

    ml = request.form['ml']

    dsa = request.form['dsa']

    python_marks = request.form['python']

    algorithm = request.form['algorithm']

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE students
        SET
            name=?,
            roll=?,
            course=?,
            marks=?,
            ai=?,
            ml=?,
            dsa=?,
            python=?,
            algorithm=?
        WHERE id=?
        ''',
        (
            name,
            roll,
            course,
            marks,
            ai,
            ml,
            dsa,
            python_marks,
            algorithm,
            id
        )
    )

    conn.commit()

    conn.close()

    return redirect('/students')

# =========================
# DELETE STUDENT
# =========================

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect('/students')

# =========================
# EXPORT CSV
# =========================

@app.route('/export')
def export():

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students"
    )

    students = cursor.fetchall()

    conn.close()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            'ID',
            'Name',
            'Roll',
            'Course',
            'Marks',
            'Photo'
        ]
    )

    for student in students:

        writer.writerow(student)

    response = Response(
        output.getvalue(),
        mimetype='text/csv'
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=students.csv"

    return response

# =========================
# ANALYTICS DASHBOARD
# =========================

@app.route('/analytics')
def analytics():

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM students"
    )

    total_students = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(marks) FROM students"
    )

    average_marks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT MAX(marks) FROM students"
    )

    highest_marks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT MIN(marks) FROM students"
    )

    lowest_marks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT name, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 1
        """
    )

    topper = cursor.fetchone()

    topper_name = topper[0]

    topper_marks = topper[1]

    conn.close()

    return render_template(
        'analytics.html',
        total_students=total_students,
        average_marks=round(average_marks,2),
        highest_marks=highest_marks,
        lowest_marks=lowest_marks,
        topper_name=topper_name,
        topper_marks=topper_marks
    )

# =========================
# STUDENT RANKING
# =========================

@app.route('/ranking')
def ranking():

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        ORDER BY marks DESC
        """
    )

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'ranking.html',
        students=students
    )


# =========================
# PDF REPORT CARD
# =========================

@app.route('/report/<int:id>')
def report(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    filename = f"report_{id}.pdf"

    c = canvas.Canvas(filename)

    c.setFont(
        "Helvetica-Bold",
        22
    )

    c.drawString(
        170,
        800,
        "Student Report Card"
    )

    c.setFont(
        "Helvetica",
        16
    )

    c.drawString(
        100,
        720,
        f"Student ID : {student[0]}"
    )

    c.drawString(
        100,
        680,
        f"Name : {student[1]}"
    )

    c.drawString(
        100,
        640,
        f"Roll Number : {student[2]}"
    )

    c.drawString(
        100,
        600,
        f"Course : {student[3]}"
    )

    c.drawString(
        100,
        560,
        f"Marks : {student[4]}"
    )

    if student[4] >= 40:

        result = "PASS"

    else:

        result = "FAIL"

    c.drawString(
        100,
        520,
        f"Result : {result}"
    )

    c.save()

    return send_file(
        filename,
        as_attachment=True
    )
# =========================
# AI CHATBOT
# =========================

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    answer = ""

    if request.method == 'POST':

        question = request.form['question'].lower()

        # TOPPER

        if "topper" in question:

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name, marks
                FROM students
                ORDER BY marks DESC
                LIMIT 1
                """
            )

            topper = cursor.fetchone()

            conn.close()

            if topper:

                answer = f"Topper is {topper[0]} with {topper[1]} marks."

            else:

                answer = "No student data found."

        # TOTAL STUDENTS

        elif "total students" in question:

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM students"
            )

            total = cursor.fetchone()[0]

            conn.close()

            answer = f"Total students are {total}."

        # AVERAGE MARKS

        elif "average marks" in question:

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT AVG(marks) FROM students"
            )

            avg = cursor.fetchone()[0]

            conn.close()

            if avg:

                answer = f"Average marks are {round(avg,2)}."

            else:

                answer = "No marks data found."

        # HIGHEST MARKS

        elif "highest marks" in question:

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT MAX(marks) FROM students"
            )

            highest = cursor.fetchone()[0]

            conn.close()

            answer = f"Highest marks are {highest}."

        # LOWEST MARKS

        elif "lowest marks" in question:

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT MIN(marks) FROM students"
            )

            lowest = cursor.fetchone()[0]

            conn.close()

            answer = f"Lowest marks are {lowest}."

        # SUBJECTS

        elif "ai" in question:

            answer = "Artificial Intelligence is the simulation of human intelligence in machines."

        elif "machine learning" in question or "ml" in question:

            answer = "Machine Learning is a branch of AI that learns from data."

        elif "python" in question:

            answer = "Python is widely used in AI, ML, Data Science and Web Development."

        elif "dsa" in question:

            answer = "DSA means Data Structures and Algorithms."

        elif "java" in question:

            answer = "Java is an Object Oriented Programming language."

        elif "algorithm" in question:

            answer = "An algorithm is a step-by-step procedure used to solve a problem."

        elif "attendance" in question:

            answer = "Attendance can be managed using the Attendance System."

        elif "flask" in question:

            answer = "Flask is a Python framework used for web development."
        elif "course" in question:

             answer = "This project manages student records, attendance and analytics."

        elif "project" in question:

            answer = "Student Performance Analytics System built using Flask and SQLite."
   
        elif "developer" in question:

            answer = "This project was developed by Piyush Ingole."

        elif "college" in question:

             answer = "P.R. Pote Patil College of Engineering and Management."

        elif "branch" in question:

             answer = "Artificial Intelligence and Machine Learning (AIML)."

        else:

            answer = "Sorry, I don't know that yet."

    return render_template(
        'chatbot.html',
        answer=answer
    )
# =========================
# RUN SERVER
# =========================

if __name__ == '__main__':

    app.run(debug=True)