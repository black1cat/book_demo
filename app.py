from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
  return 'welcome to my book_demo!'