from flask import Flask, render_template, request, jsonify
import sqlite3
from scraper import count
import pandas as pd

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    # Create tables for each class
    classes = ['CSE_A', 'CSE_B', 'CSE_C']  # You can modify this list
    for class_name in classes:
        c.execute(f'''CREATE TABLE IF NOT EXISTS {class_name}
                     (s_no INTEGER PRIMARY KEY,
                      user_name TEXT,
                      roll_no TEXT,
                      previous_week INTEGER,
                      recent_week INTEGER,
                      count INTEGER)''')
    conn.commit()
    conn.close()

def get_classes():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    # Get list of all tables (classes)
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    classes = [row[0] for row in c.fetchall()]
    conn.close()
    
    return classes

@app.route('/')
def home():
    classes = get_classes()
    return render_template('index.html', classes=classes)

@app.route('/update/<class_name>', methods=['POST'])
def update_scores(class_name):
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        # Get all usernames for the selected class
        c.execute(f'SELECT user_name FROM {class_name}')
        usernames = [row[0] for row in c.fetchall()]
        if not usernames:
            return jsonify({"error": "No students found in this class"}), 404
        
        # Get new scores
        new_scores = count(usernames)
        print(usernames,new_scores)
        # Update database
        for username, new_score in zip(usernames, new_scores):
            # Get current recent score to make it previous score
            c.execute(f'SELECT recent_week FROM {class_name} WHERE user_name = ?', (username,))
            current_score = c.fetchone()[0]
            
            # Calculate count (difference)
            score_difference = int(new_score) - int(current_score)
            
            # Update scores
            c.execute(f'''UPDATE {class_name}
                        SET previous_week = ?,
                            recent_week = ?,
                            count = ?
                        WHERE user_name = ?''',
                     (current_score, new_score, score_difference, username))
        
        conn.commit()
        conn.close()
        return jsonify({"message": f"Scores updated successfully for {class_name}"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/show/<class_name>')
def show_scores(class_name):
    try:
        conn = sqlite3.connect('students.db')
        df = pd.read_sql_query(f'''SELECT s_no, user_name, roll_no, 
                                  previous_week, recent_week, count 
                                  FROM {class_name}
                                  ORDER BY s_no''', conn)
        conn.close()
        return render_template('scores.html', 
                             tables=[df.to_html(classes='data', index=False)],
                             titles=df.columns.values,
                             class_name=class_name)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)