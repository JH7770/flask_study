import sys

from flask_script import Manager
from app_init import create_app
from flask_twisted import Twisted
from twisted.python import log

if __name__ == "__main__":
    app = create_app()
    twisted = Twisted(app)
    app.logger.info(f"Running the app...")
    log.startLogging(sys.stdout)
    manager = Manager(app)
    manager.run()
