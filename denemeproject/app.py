from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from quiz import Quiz

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/')
def index():
    username = session.get('username', None)
    best_score = Database.get_user_best_score(username) if username else None
    return render_template('index.html', username=username, best_score=best_score)

@app.route('/set_name', methods=['POST'])
def set_name():
    username = request.form.get('username')
    if username:
        session['username'] = username
        if Database.get_user_best_score(username) is None:
            Database.update_user_score(username, 0)
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    username = session.get('username', None)
    if not username:
        return redirect(url_for('index'))

    questions_with_indexes = []
    for idx, question in enumerate(Quiz.questions):
        questions_with_indexes.append({
            "id": idx,
            "question": question["question"],
            "options": list(enumerate(question["options"]))
        })

    if request.method == 'POST':
        correct_answers = 0
        total_questions = len(Quiz.questions)

        for i, question in enumerate(Quiz.questions):
            user_answer = request.form.get(f'answer_{i}')
            if user_answer is not None and int(user_answer) == question['answer']:
                correct_answers += 1

        score = int((correct_answers / total_questions) * 100)

        Database.update_user_score(username, score)
        return redirect(url_for('result', score=score))

    return render_template('quiz.html', questions=questions_with_indexes)

@app.route('/result')
def result():
    score = request.args.get('score', 0, type=int)
    username = session.get('username', '')
    best_score = Database.get_user_best_score(username)
    return render_template('result.html', score=score, best_score=best_score)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    Database.create_db()
    app.run(debug=True)