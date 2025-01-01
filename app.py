from App import app
import os
from config import config
from flask_mail import Mail, Message
import logging
from colorlog import ColoredFormatter



env = os.getenv("FLASK_ENV", "development")

app.config.from_object(config[env])
mail = Mail(app)

if __name__ == "__main__":
    app.run(debug=True)






