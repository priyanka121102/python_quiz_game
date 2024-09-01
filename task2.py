#using trivia api-->
import sqlite3

def setup_database():
    conn = sqlite3.connect('quiz_game.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            wrong_answer1 TEXT NOT NULL,
            wrong_answer2 TEXT NOT NULL,
            wrong_answer3 TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

setup_database()
def add_question(question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3):
    conn = sqlite3.connect('quiz_game.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO questions (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
        VALUES (?, ?, ?, ?, ?)
    ''', (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3))

    conn.commit()
    conn.close()

# Example questions
# add_question("What is the capital of France?", "Paris", "London", "Berlin", "Madrid")
# add_question("Which planet is known as the Red Planet?", "Mars", "Jupiter", "Saturn", "Venus")
import requests

def fetch_and_store_questions(amount=10):
    conn = sqlite3.connect('quiz_game.db')
    cursor = conn.cursor()

    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    
    response = requests.get(url)
    data = response.json()

    for item in data['results']:
        question = item['question']
        correct_answer = item['correct_answer']
        wrong_answers = item['incorrect_answers']

        cursor.execute('''
            INSERT INTO questions (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
            VALUES (?, ?, ?, ?, ?)
        ''', (question, correct_answer, *wrong_answers))

    conn.commit()
    conn.close()

# Fetch 10 questions and store them in the database
fetch_and_store_questions()

import random

def fetch_questions():
    conn = sqlite3.connect('quiz_game.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM questions ORDER BY RANDOM () LIMIT 5')
    questions = cursor.fetchall()

    conn.close()
    return questions

def play_game():
    questions = fetch_questions()
    random.shuffle(questions)
    score = 0

    for q in questions:
        question_id, question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3 = q
        answers = [correct_answer, wrong_answer1, wrong_answer2, wrong_answer3]
        random.shuffle(answers)

        print(f"\nQuestion: {question}")
        for i, answer in enumerate(answers):
            print(f"{i + 1}. {answer}")

        user_answer = input("Choose the correct answer (1-4): ")
        if answers[int(user_answer) - 1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {correct_answer}.")

    print(f"\nYour final score is {score*10}/{len(questions*10)}.")
    if score>(len(question)/2):
        print("you are winner")
    else:
        print("you are loser ! please try again")    

play_game()
