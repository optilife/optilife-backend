import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/optilife'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


port = int(os.getenv('PORT', '3000'))


@app.route('/')
def hello_world():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)