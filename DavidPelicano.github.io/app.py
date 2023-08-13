from flask import Flask
from views import views


app = Flask(__name__,static_url_path='/static')
app.register_blueprint(views, url_prefix="/")
app.secret_key = 'your_secret_key_here'

if __name__ == '__main__':
    #app.run(host="0.0.0.0",port=8000)

    app.run(debug=True, port=8000)