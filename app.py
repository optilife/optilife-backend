import os
from flask import Flask

app = Flask(__name__)

port = int(os.getenv('PORT', '3000'))

@app.route('/')
def hello_world():
    return 'Hello OptiLife'

# start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)