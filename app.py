from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql, os
from db import connect_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на свой секретный ключ

# Папка для хранения загруженных файлов (рекомендуется создать папку static/uploads)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    return connect_db()

@app.route('/')
def index():
    total_tasks = completed_tasks = progress_percent = 0

    if 'user_id' in session:
        user_id = session['user_id']
        connection = connect_db()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM exercises")
                total_tasks = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(DISTINCT exercise_id) as completed FROM results WHERE user_id=%s", (user_id,))
                completed_tasks = cursor.fetchone()['completed']

            progress_percent = round((completed_tasks / total_tasks) * 100) if total_tasks else 0
        finally:
            connection.close()

    return render_template('index.html',
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           progress_percent=progress_percent)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, email, password, 'user'))
            connection.commit()
            flash('Регистрация прошла успешно! Войдите в систему.', 'success')
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError:
            flash('Пользователь с таким email уже существует.', 'danger')
        finally:
            connection.close()
    return render_template('register.html')
@app.route('/subjects')
def subjects():
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()
    connection.close()
    return render_template('subjects.html', subjects=subjects)


@app.route('/exercise/<int:exercise_id>', methods=['GET', 'POST'])
def exercise_detail(exercise_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM exercises WHERE id=%s", (exercise_id,))
            exercise = cursor.fetchone()

        if not exercise:
            flash('Задание не найдено.', 'danger')
            return redirect(url_for('subjects'))

        if request.method == 'POST':
            user_id = session['user_id']

            if exercise['type'] == 'test':
                user_answer = request.form.get('answer_text', '').strip()

                # Сохраняем ответ в таблицу submissions
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO submissions (user_id, exercise_id, answer_text) VALUES (%s, %s, %s)",
                        (user_id, exercise_id, user_answer)
                    )
                    connection.commit()

                # Автоматическая проверка для тестовых заданий
                correct_answer = (exercise['correct_answer'] or '').strip()
                score = 1 if user_answer.lower() == correct_answer.lower() else 0
                comment = 'Ответ верный!' if score else f'Ответ неверный. Правильный ответ: {correct_answer}'

                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO results (user_id, exercise_id, score, comment) VALUES (%s, %s, %s, %s)",
                        (user_id, exercise_id, score, comment)
                    )
                    connection.commit()

                flash(f'Ответ отправлен. {comment}', 'success')
                return redirect(url_for('exercises', subject_id=exercise['subject_id']))

            elif exercise['type'] == 'written':
                file = request.files.get('result_file')
                answer_text = request.form.get('answer_text', '').strip()

                if file and file.filename:
                    filename = f"{user_id}_{exercise_id}_{file.filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    relative_path = f'uploads/{filename}'

                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO submissions (user_id, exercise_id, file_path, answer_text) VALUES (%s, %s, %s, %s)",
                            (user_id, exercise_id, relative_path, answer_text)
                        )
                        connection.commit()
                    flash('Файл успешно отправлен на проверку.', 'success')
                elif answer_text:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO submissions (user_id, exercise_id, answer_text) VALUES (%s, %s, %s)",
                            (user_id, exercise_id, answer_text)
                        )
                        connection.commit()
                    flash('Ваш ответ отправлен на проверку.', 'success')
                else:
                    flash('Необходимо указать ответ или загрузить файл.', 'warning')
                    return redirect(request.url)

                return redirect(url_for('exercises', subject_id=exercise['subject_id']))

        return render_template('exercise_detail.html', exercise=exercise)
    finally:
        connection.close()


@app.route('/subject/<int:subject_id>/theory')
def theory(subject_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM theory WHERE subject_id=%s", (subject_id,))
        materials = cursor.fetchall()
    connection.close()
    return render_template('theory.html', materials=materials)

@app.route('/subject/<int:subject_id>/exercises')
def exercises(subject_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM exercises WHERE subject_id=%s", (subject_id,))
        exercises = cursor.fetchall()
    connection.close()
    return render_template('exercises.html', exercises=exercises, subject_id=subject_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email=%s AND password=%s"
                cursor.execute(sql, (email, password))
                user = cursor.fetchone()
                if user:
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['user_email'] = user['email']  # добавлено
                    session['user_role'] = user['role']
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Неверные учетные данные.', 'danger')
        finally:
            connection.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))
    # Пример расчёта прогресса (замените на свою логику)
    progress_percent = 50  # например, 50%
    progress_value = 3      # например, выполнено 3 задания
    return render_template('dashboard.html', progress_percent=progress_percent, progress_value=progress_value)



# Административная панель (уже существующая)
@app.route('/admin')
def admin():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            cursor.execute("SELECT * FROM subjects")
            subjects = cursor.fetchall()

            cursor.execute("SELECT * FROM exercises")
            exercises = cursor.fetchall()

            cursor.execute("SELECT * FROM submissions WHERE status='pending'")
            submissions = cursor.fetchall()
    finally:
        connection.close()

    return render_template('admin.html', users=users, subjects=subjects, exercises=exercises, submissions=submissions)
@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('login'))

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
        connection.commit()
        flash("Предмет успешно удалён.", "success")
    except Exception as e:
        flash(f"Ошибка при удалении предмета: {str(e)}", "danger")
    finally:
        connection.close()

    return redirect(url_for('admin'))
@app.route('/delete_exercise/<int:exercise_id>', methods=['POST'])
def delete_exercise(exercise_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('login'))

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))
        connection.commit()
        flash("Задание успешно удалено.", "success")
    except Exception as e:
        flash(f"Ошибка при удалении задания: {str(e)}", "danger")
    finally:
        connection.close()

    return redirect(url_for('admin'))

@app.route('/edit_subject', methods=['POST'])
def edit_subject():
    if 'user_role' in session and session['user_role'] == 'admin':
        subject_id = request.form['subject_id']
        title = request.form['title']
        description = request.form['description']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE subjects SET title=%s, description=%s WHERE id=%s",
                           (title, description, subject_id))
        connection.commit()
        connection.close()
        flash("Предмет обновлен", "success")
    return redirect(url_for('admin'))
@app.route('/edit_exercise', methods=['POST'])
def edit_exercise():
    if 'user_role' in session and session['user_role'] == 'admin':
        exercise_id = request.form['exercise_id']
        title = request.form['title']
        description = request.form['description']
        exercise_type = request.form['type']
        subject_id = request.form['subject_id']

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE exercises
                SET title=%s, description=%s, type=%s, subject_id=%s
                WHERE id=%s
            """, (title, description, exercise_type, subject_id, exercise_id))
        connection.commit()
        connection.close()

        flash('Задание успешно обновлено.', 'success')
    return redirect(url_for('admin'))

@app.route('/results')
def results():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT exercises.title, results.score, results.comment, results.date_checked
                FROM results
                JOIN exercises ON results.exercise_id = exercises.id
                WHERE results.user_id = %s
                ORDER BY results.date_checked DESC
            """
            cursor.execute(sql, (user_id,))
            user_results = cursor.fetchall()
    finally:
        connection.close()

    return render_template('results.html', user_results=user_results)


# Обработка редактирования пользователя
@app.route('/edit_user', methods=['POST'])
def edit_user():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('login'))
    user_id = request.form['user_id']
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE users SET name=%s, email=%s, role=%s WHERE id=%s"
        cursor.execute(sql, (name, email, role, user_id))
    connection.commit()
    connection.close()
    flash("Пользователь обновлен.", "success")
    return redirect(url_for('admin'))

# Удаление пользователя
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('login'))
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (user_id,))
    connection.commit()
    connection.close()
    flash("Пользователь удален.", "success")
    return redirect(url_for('admin'))

# Обработка редактирования курса
@app.route('/edit_course', methods=['POST'])
def edit_course():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Доступ запрещен.', 'danger')
        return redirect(url_for('login'))
    course_id = request.form['course_id']
    title = request.form['title']
    description = request.form['description']
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE courses SET title=%s, description=%s WHERE id=%s"
        cursor.execute(sql, (title, description, course_id))
    connection.commit()
    connection.close()
    flash("Курс обновлен.", "success")
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
