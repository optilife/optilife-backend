import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/optilife'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

port = int(os.getenv('PORT', '3000'))


@app.route('/')
def hello_world():
    return


@app.route('/setup_db')
def setup_db():
    msg = "DB created"
    try:
        engine = db.create_engine('mysql+pymysql://root:@localhost')
        engine.execute("CREATE DATABASE IF NOT EXISTS optilife")
        engine.execute("USE optilife")
        db.drop_all()
        db.create_all()
        
    except Exception as ex:
        msg = str(ex)

    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)