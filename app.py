from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_learning'

# In-memory storage for users and calculation history
users_db = {}  # Format: {identifier: password}
calculation_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        identifier = request.form.get('identifier').strip()  # Email, Name, or Phone
        password = request.form.get('password')
        action = request.form.get('action')  # 'signup' or 'login'
        
        if action == 'signup':
            if len(password) < 8:
                error = "Password must be at least 8 characters long."
            elif identifier in users_db:
                error = "Account already exists with this identifier."
            else:
                users_db[identifier] = password
                session['username'] = identifier
                return redirect(url_for('calculator'))
                
        elif action == 'login':
            if identifier in users_db and users_db[identifier] == password:
                session['username'] = identifier
                return redirect(url_for('calculator'))
            else:
                error = "Invalid credentials or account doesn't exist."
                
    return render_template('index.html', error=error)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))
            operation = request.form.get('operation')
            
            if operation == 'add':
                result = num1 + num2
                op_symbol = '+'
            elif operation == 'subtract':
                result = num1 - num2
                op_symbol = '-'
            elif operation == 'multiply':
                result = num1 * num2
                op_symbol = '×'
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                    op_symbol = '÷'
                else:
                    result = "Error: Division by zero"
                    op_symbol = '÷'
            
            if isinstance(result, (int, float)):
                calc_record = f"{num1} {op_symbol} {num2} = {result}"
                calculation_history.append(calc_record)
                
        except ValueError:
            result = "Error: Invalid input"
            
    return render_template('calculator.html', calculation_result=result)

@app.route('/formulas', methods=['GET', 'POST'])
def formulas():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('formulas.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    username = session.get('username')
    return render_template('profile.html', username=username, history=calculation_history)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)