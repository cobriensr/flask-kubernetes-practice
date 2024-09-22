# app.py
import os
import logging
from urllib.parse import quote_plus
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'myapp')
db_user = os.getenv('DB_USER', 'myappuser')
db_password = os.getenv('DB_PASSWORD', 'myapppassword')

# Construct the database URI, ensuring proper URL encoding
db_user_encoded = quote_plus(db_user)
db_password_encoded = quote_plus(db_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user_encoded}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
logger.info(f"Connecting to database: postgresql://{db_user_encoded}:****@{db_host}:{db_port}/{db_name}")

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Note {self.id}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()
            logger.info(f"New note added: {content}")
        return redirect(url_for('index'))

    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 error: {request.url}")
    return render_template('404.html'), 404

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    try:
        init_db()
        logger.info("Starting the Flask application")
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        logger.error(f"Failed to start the application: {str(e)}")
        logger.exception("Detailed error information:")
