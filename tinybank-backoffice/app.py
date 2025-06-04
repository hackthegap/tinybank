from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000/api')

@app.route('/')
def index():
    return redirect('/transactions')

@app.route('/transactions')
def all_transactions():
    txs = requests.get(f'{BACKEND_URL}/transactions/').json()
    users = requests.get(f'{BACKEND_URL}/users/').json()
    user_map = {u['id']: u['email'] for u in users}
    return render_template('transactions.html', transactions=txs, user_map=user_map)

@app.route('/transactions/by-user', methods=['GET', 'POST'])
def transactions_by_user():
    users = requests.get(f'{BACKEND_URL}/users/').json()
    selected_user_id = request.form.get('user_id')
    txs = []
    if request.method == 'POST' and selected_user_id:
        all_txs = requests.get(f'{BACKEND_URL}/transactions/').json()
        txs = [t for t in all_txs if str(t['user']) == selected_user_id]
    return render_template('user_filter.html', users=users, transactions=txs)

@app.route('/transactions/delete/<int:tx_id>', methods=['POST'])
def delete_transaction(tx_id):
    requests.delete(f'{BACKEND_URL}/transactions/{tx_id}/')
    return redirect('/transactions')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

