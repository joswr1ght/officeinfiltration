from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Generate unique, non-guessable paths for levels
LEVEL_PATHS = {
    1: '/',
    2: f'/level/{secrets.token_urlsafe(16)}',
    3: f'/level/{secrets.token_urlsafe(16)}',
    4: f'/level/{secrets.token_urlsafe(16)}',
    5: f'/level/{secrets.token_urlsafe(16)}',
}

LEVEL_DATA = {
    1: {
        "title": "Level 1: The Turnstile",
        "image": "floor1.png",
        "challenge_description": "Bypass the main entrance turnstile. You see a card reader and a security guard nearby.",
        "correct_answer": "swipe a cloned badge", # Example answer
        "next_level_path": LEVEL_PATHS[2]
    },
    2: {
        "title": "Level 2: The Elevator Door",
        "image": "floor2.png",
        "challenge_description": "Gain access to the secure elevator. It requires a special key or code.",
        "correct_answer": "use the maintenance key", # Example answer
        "next_level_path": LEVEL_PATHS[3]
    },
    3: {
        "title": "Level 3: Floor 42 Access",
        "image": "floor3.png",
        "challenge_description": "The elevator panel for floor 42 is locked. Find a way to activate it.",
        "correct_answer": "override elevator control", # Example answer
        "next_level_path": LEVEL_PATHS[4]
    },
    4: {
        "title": "Level 4: The Entry Door",
        "image": "floor4.png",
        "challenge_description": "You're at the main door to the target office on floor 42. It's a reinforced door with a keypad and biometric scanner.",
        "correct_answer": "enter code 1234", # Example answer
        "next_level_path": LEVEL_PATHS[5]
    },
    5: {
        "title": "Level 5: The Workstation",
        "image": "floor5.png",
        "challenge_description": "Access the CEO's workstation. It's password protected.",
        "correct_answer": "guess password", # Example answer
        "next_level_path": "/congratulations" # Or a final page
    }
}

def get_current_level():
    return session.get('current_level', 1)

def set_current_level(level):
    session['current_level'] = level

@app.route('/')
def level1():
    set_current_level(1)
    return render_template('level.html', level_data=LEVEL_DATA[1], current_path=LEVEL_PATHS[1])

@app.route(LEVEL_PATHS[2], methods=['GET', 'POST'])
def level2():
    if get_current_level() < 2:
        return redirect(url_for('level1')) # Or some other appropriate redirect
    set_current_level(2)
    return render_template('level.html', level_data=LEVEL_DATA[2], current_path=LEVEL_PATHS[2])

@app.route(LEVEL_PATHS[3], methods=['GET', 'POST'])
def level3():
    if get_current_level() < 3:
        return redirect(LEVEL_PATHS.get(get_current_level(), '/'))
    set_current_level(3)
    return render_template('level.html', level_data=LEVEL_DATA[3], current_path=LEVEL_PATHS[3])

@app.route(LEVEL_PATHS[4], methods=['GET', 'POST'])
def level4():
    if get_current_level() < 4:
        return redirect(LEVEL_PATHS.get(get_current_level(), '/'))
    set_current_level(4)
    return render_template('level.html', level_data=LEVEL_DATA[4], current_path=LEVEL_PATHS[4])

@app.route(LEVEL_PATHS[5], methods=['GET', 'POST'])
def level5():
    if get_current_level() < 5:
        return redirect(LEVEL_PATHS.get(get_current_level(), '/'))
    set_current_level(5)
    return render_template('level.html', level_data=LEVEL_DATA[5], current_path=LEVEL_PATHS[5])

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    user_question = request.form.get('ai_question')
    current_level_num = get_current_level()
    # Placeholder AI response logic
    ai_response = f"AI response to '{user_question}' for level {current_level_num}. The image shows {LEVEL_DATA[current_level_num]['image']}."
    # In a real app, you'd query your AI model here based on user_question and current_level_num
    return ai_response

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form.get('user_answer')
    current_level_num = get_current_level()
    level_data = LEVEL_DATA.get(current_level_num)

    if not level_data:
        return "Error: Level data not found.", 400

    # Case-insensitive comparison for the answer
    if user_answer and user_answer.lower() == level_data['correct_answer'].lower():
        next_level_num = current_level_num + 1
        if next_level_num > 5: # Max levels
            return redirect(url_for('congratulations'))

        set_current_level(next_level_num)
        next_path = LEVEL_PATHS.get(next_level_num)
        if next_path:
            return redirect(next_path)
        else:
            return "Error: Next level path not found.", 500
    else:
        # Stay on the current level, maybe provide feedback
        # For simplicity, just re-rendering the current level's page
        # A more advanced version might pass an error message to the template
        current_path = LEVEL_PATHS.get(current_level_num)
        if not current_path:
             return "Error: Current level path not found.", 500
        # Need to reconstruct the route function name or redirect to the path directly
        if current_level_num == 1:
            return redirect(url_for('level1', error="Incorrect answer. Try again."))
        # For other levels, we redirect to their specific paths
        # We pass an error message via query parameter for simplicity here
        return redirect(f"{current_path}?error=Incorrect+answer.+Try+again.")


@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')

if __name__ == '__main__':
    app.run(debug=True)
