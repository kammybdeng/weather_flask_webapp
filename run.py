import os
from flask_migrate import Migrate
from flask_script import Manager
from weatherflaskwebapp import app, db

app.config.from_object(os.getenv('APP_SETTINGS', "config.ProductionConfig"))

migrate = Migrate(app, db)
manager = Manager(app)


if __name__ == '__main__':
	app.run()
	manager.run()
