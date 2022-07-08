from app import app

app.config['SECRET_KEY'] = 'secret'
app.run(debug=True)