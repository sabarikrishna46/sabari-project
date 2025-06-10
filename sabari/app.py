# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector
# from mysql.connector import Error
# from datetime import datetimem

# app = Flask(__name__)

# # MySQL Database configuration
# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',     # Replace with your MySQL username
#     'password':'Digidara1000',
#     'database': 'examdb'         # Replace with your MySQL database name
# }

# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)

# # Initialize MySQL database for exams
# def init_db():
#     con=None
#     cursor=None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS exams (
#                 exam_code VARCHAR(20) PRIMARY KEY,
#                 subject VARCHAR(100),
#                 semester VARCHAR(10),
#                 department VARCHAR(50),
#                 exam_date DATE,
#                 start_time VARCHAR(20),
#                 end_time VARCHAR(20)
#             )
#         ''')
#         conn.commit()
#     except Error as e:
#         print(f"Error initializing DB: {e}")
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/index', methods=['GET'])
# def index():
#     semester = request.args.get('semester', '')
#     department = request.args.get('department', '')

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = '''
#             SELECT exam_code, subject, semester, department, exam_date, start_time, end_time 
#             FROM exams WHERE 1=1
#         '''
#         params = []
#         if semester:
#             query += ' AND semester = %s'
#             params.append(semester)
#         if department:
#             query += ' AND (department = %s OR department = "ALL")'
#             params.append(department)
        
#         cursor.execute(query, params)
#         exams = [
#             {
#                 'exam_code': row[0],
#                 'subject': row[1],
#                 'semester': row[2],
#                 'department': row[3],
#                 'exam_date': row[4].strftime('%d-%m-%Y'),
#                 'start_time': row[5],
#                 'end_time': row[6]
#             } for row in cursor.fetchall()
#         ]
#     except Error as e:
#         exams = []
#         print(f"Error fetching exams: {e}")
#     finally:
#         cursor.close()
#         conn.close()

#     return render_template('index.html', exams=exams)

# @app.route('/login',methods=['GET','POST'])
# def login():
#     error=None
#     next_page=request.args.get('next','')
#     if request.method == 'POST':
#         email=request.form.get('email')
#         password=request.form.get('pass')
#         next_page=request.form.get('next')
#         if email =='sabarilathapandi@gmail.com' and password=='sabari2346':
#             if next_page =='add':
#                 return redirect(url_for('add_exam'))
#             elif next_page =='manage':
#                 return redirect(url_for('admin'))
#             else:
#                 return redirect(url_for('home'))
#         else:
#             error='invalid email or password.'
#     return render_template('login.html', error=error, request=request)

# @app.route('/add', methods=['GET', 'POST'])
# def add_exam():
#     if request.method == 'POST':
#         exam_code = request.form['exam_code'].upper()
#         subject = request.form['subject'].upper()
#         semester = request.form['semester']
#         department = request.form['department'].upper()
#         exam_date_input = request.form['exam_date']
#         exam_date = datetime.strptime(exam_date_input, '%d.%m.%Y').strftime('%Y-%m-%d')
#         start_time = request.form['start_time']
#         end_time = request.form['end_time']

#         if not all([exam_code, subject, semester, department, exam_date, start_time, end_time]):
#             return render_template('add.html', error="All fields are required.")

#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('SELECT exam_code FROM exams WHERE exam_code = %s', (exam_code,))
#             if cursor.fetchone():
#                 return render_template('add.html', error="Exam code already exists. Please use a unique code.")
            
#             cursor.execute('''
#                 INSERT INTO exams (exam_code, subject, semester, department, exam_date, start_time, end_time)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#             ''', (exam_code, subject, semester, department, exam_date, start_time, end_time))
#             conn.commit()
#             return redirect(url_for('index'))
#         except Error as e:
#             return render_template('add.html', error=f"Error adding exam: {str(e)}")
#         finally:
#             cursor.close()
#             conn.close()

#     return render_template('add.html', error=None)

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         action = request.form.get('action')
#         exam_code = request.form.get('exam_code')

#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor()

#             if action == 'delete':
#                 cursor.execute('DELETE FROM exams WHERE exam_code = %s', (exam_code,))
#                 conn.commit()
#             elif action == 'edit':
#                 subject = request.form.get('subject').upper()
#                 semester = request.form.get('semester')
#                 department = request.form.get('department').upper()
#                 exam_date = request.form.get('exam_date')
#                 start_time = request.form.get('start_time')
#                 end_time = request.form.get('end_time')

#                 if not all([subject, semester, department, exam_date, start_time, end_time]):
#                     return render_template('admin.html', error="All fields are required for editing.", exams=[])

#                 cursor.execute('''
#                     UPDATE exams 
#                     SET subject = %s, semester = %s, department = %s, exam_date = %s, start_time = %s, end_time = %s
#                     WHERE exam_code = %s
#                 ''', (subject, semester, department, exam_date, start_time, end_time, exam_code))
#                 conn.commit()
#             return redirect(url_for('admin'))
#         except Error as e:
#             return render_template('admin.html', error=f"Error processing action: {str(e)}", exams=[])
#         finally:
#             cursor.close()
#             conn.close()

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT exam_code, subject, semester, department, exam_date, start_time, end_time FROM exams')
#         exams = [
#             {
#                 'exam_code': row[0],
#                 'subject': row[1],
#                 'semester': row[2],
#                 'department': row[3],
#                 'exam_date': row[4].strftime('%Y-%m-%d'),
#                 'start_time': row[5],
#                 'end_time': row[6]
#             } for row in cursor.fetchall()
#         ]
#     except Error as e:
#         exams = []
#         return render_template('admin.html', exams=exams, error=f"Error loading exams: {e}")
#     finally:
#         cursor.close()
#         conn.close()

#     return render_template('admin.html', exams=exams, error=None)

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

app = Flask(__name__)

# MySQL Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Digidara1000',
    'database': 'examdb'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Initialize exams table
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                exam_code VARCHAR(20) PRIMARY KEY,
                subject VARCHAR(100),
                semester VARCHAR(10),
                department VARCHAR(50),
                exam_date DATE,
                start_time VARCHAR(20),
                end_time VARCHAR(20)
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error initializing DB: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
    semester = request.args.get('semester', '')
    department = request.args.get('department', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = '''
            SELECT exam_code, subject, semester, department, exam_date, start_time, end_time 
            FROM exams WHERE 1=1
        '''
        params = []
        if semester:
            query += ' AND semester = %s'
            params.append(semester)
        if department:
            query += ' AND (department = %s OR department = "ALL")'
            params.append(department)

        cursor.execute(query, params)
        exams = [
            {
                'exam_code': row[0],
                'subject': row[1],
                'semester': row[2],
                'department': row[3],
                'exam_date': row[4].strftime('%d-%m-%Y'),
                'start_time': row[5],
                'end_time': row[6]
            } for row in cursor.fetchall()
        ]
    except Error as e:
        exams = []
        print(f"Error fetching exams: {e}")
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', exams=exams)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        next_page = request.form.get('next')
        if email == 'sabarilathapandi@gmail.com' and password == 'sabari2346':
            if next_page == 'add':
                return redirect(url_for('add_exam'))
            elif next_page == 'manage':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            error = 'Invalid email or password.'
    return render_template('login.html', error=error, request=request)

@app.route('/add', methods=['GET', 'POST'])
def add_exam():
    if request.method == 'POST':
        exam_code = request.form['exam_code'].upper()
        subject = request.form['subject'].upper()
        semester = request.form['semester']
        department = request.form['department'].upper()
        exam_date_input = request.form['exam_date']
        exam_date = datetime.strptime(exam_date_input, '%d.%m.%Y').strftime('%Y-%m-%d')
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        if not all([exam_code, subject, semester, department, exam_date, start_time, end_time]):
            return render_template('add.html', error="All fields are required.")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT exam_code FROM exams WHERE exam_code = %s', (exam_code,))
            if cursor.fetchone():
                return render_template('add.html', error="Exam code already exists.")
            cursor.execute('''
                INSERT INTO exams (exam_code, subject, semester, department, exam_date, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (exam_code, subject, semester, department, exam_date, start_time, end_time))
            conn.commit()
            return redirect(url_for('index'))
        except Error as e:
            return render_template('add.html', error=f"Error adding exam: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    return render_template('add.html', error=None)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        exam_code = request.form.get('exam_code')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if action == 'delete':
                cursor.execute('DELETE FROM exams WHERE exam_code = %s', (exam_code,))
                conn.commit()
            elif action == 'edit':
                subject = request.form.get('subject').upper()
                semester = request.form.get('semester')
                department = request.form.get('department').upper()
                exam_date = request.form.get('exam_date')
                start_time = request.form.get('start_time')
                end_time = request.form.get('end_time')

                if not all([subject, semester, department, exam_date, start_time, end_time]):
                    return render_template('admin.html', error="All fields are required for editing.", exams=[])

                cursor.execute('''
                    UPDATE exams 
                    SET subject = %s, semester = %s, department = %s, exam_date = %s, start_time = %s, end_time = %s
                    WHERE exam_code = %s
                ''', (subject, semester, department, exam_date, start_time, end_time, exam_code))
                conn.commit()
            return redirect(url_for('admin'))
        except Error as e:
            return render_template('admin.html', error=f"Error processing action: {str(e)}", exams=[])
        finally:
            cursor.close()
            conn.close()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT exam_code, subject, semester, department, exam_date, start_time, end_time FROM exams')
        exams = [
            {
                'exam_code': row[0],
                'subject': row[1],
                'semester': row[2],
                'department': row[3],
                'exam_date': row[4].strftime('%Y-%m-%d'),
                'start_time': row[5],
                'end_time': row[6]
            } for row in cursor.fetchall()
        ]
    except Error as e:
        exams = []
        return render_template('admin.html', exams=exams, error=f"Error loading exams: {e}")
    finally:
        cursor.close()
        conn.close()

    return render_template('admin.html', exams=exams, error=None)

@app.route('/download_pdf')
def download_pdf():
    semester = request.args.get('semester', '')
    department = request.args.get('department', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = '''
            SELECT exam_code, subject, semester, department, exam_date, start_time, end_time 
            FROM exams WHERE 1=1
        '''
        params = []
        if semester:
            query += ' AND semester = %s'
            params.append(semester)
        if department:
            query += ' AND (department = %s OR department = "ALL")'
            params.append(department)

        cursor.execute(query, params)
        exams = cursor.fetchall()
    except Error as e:
        return f"Error generating PDF: {str(e)}"
    finally:
        cursor.close()
        conn.close()

    output_dir = os.path.join(app.root_path, 'static', 'pdf')
    os.makedirs(output_dir, exist_ok=True)
    filename = 'exam_schedule.pdf'
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, y, "Exam Schedule")
    y -= 30

    c.setFont("Helvetica", 10)
    for exam in exams:
        line = f"{exam[0]} | {exam[1]} | Sem: {exam[2]} | Dept: {exam[3]} | Date: {exam[4].strftime('%d-%m-%Y')} | {exam[5]} - {exam[6]}"
        c.drawString(30, y, line)
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    return send_from_directory(directory=output_dir, path=filename, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
