from flask import Flask, render_template, url_for
from read_firebase import get_all_data

app = Flask(__name__)

@app.route('/')
def index():
    # Data from firebase line below
    # data = get_all_data() 

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)