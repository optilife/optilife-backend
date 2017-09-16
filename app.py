import os
from flask import Flask

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


port = int(os.getenv('PORT', '3000'))


@app.route('/')
def hello_world():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)