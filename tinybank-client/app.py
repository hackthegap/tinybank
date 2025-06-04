from flask import Flask, render_template, request, redirect, session, url_for, flash
import requests, os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000/api')  # Django backend

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        payload = {
            'name': request.form['name'],
            'email': request.form['email']
        }
        resp = requests.post(f'{BACKEND_URL}/users/', json=payload)
        if resp.status_code == 201:
            flash("Registered successfully, please log in.")
            return redirect(url_for('login'))
        else:
            flash("Registration failed.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        users = requests.get(f'{BACKEND_URL}/users/').json()
        user = next((u for u in users if u['email'] == email), None)
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        flash("Login failed. Email not found.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_id = session['user']['id']
    user_data = requests.get(f'{BACKEND_URL}/users/{user_id}/').json()
    return render_template('dashboard.html', user=user_data)

@app.route('/transactions')
def transactions():
    if 'user' not in session:
        return redirect(url_for('login'))
    txs = requests.get(f'{BACKEND_URL}/transactions/').json()
    user_id = session['user']['id']
    filtered = [tx for tx in txs if tx['user'] == user_id]
    return render_template('transactions.html', transactions=filtered)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        payload = {
            'user': session['user']['id'],
            'tx_type': 'DEPOSIT',
            'amount': amount,
            'description': 'Deposit from client portal'
        }
        requests.post(f'{BACKEND_URL}/transactions/', json=payload)
        return redirect(url_for('dashboard'))
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        payload = {
            'user': session['user']['id'],
            'tx_type': 'WITHDRAW',
            'amount': amount,
            'description': 'Withdraw from client portal'
        }
        requests.post(f'{BACKEND_URL}/transactions/', json=payload)
        return redirect(url_for('dashboard'))
    return render_template('withdraw.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        recipient_email = request.form['email']
        amount = float(request.form['amount'])

        users = requests.get(f'{BACKEND_URL}/users/').json()
        recipient = next((u for u in users if u['email'] == recipient_email), None)

        if not recipient:
            flash("Recipient not found.")
            return redirect(url_for('transfer'))

        payload = {
            'user': session['user']['id'],
            'tx_type': 'TRANSFER',
            'amount': amount,
            'description': f'Transfer to {recipient_email}'
        }
        requests.post(f'{BACKEND_URL}/transactions/', json=payload)
        return redirect(url_for('dashboard'))

    return render_template('transfer.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)