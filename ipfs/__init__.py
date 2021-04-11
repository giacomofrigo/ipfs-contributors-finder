import os, subprocess

from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = "True"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/areaClienti.db"
    app.config["SECRET_KEY"] = "HjuflJb&()sjhYN!mSikdnJ??b7298nHYSos"
    app.config["IPFS_DAEMON"] = subprocess.Popen(['/usr/local/bin/ipfs', 'daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # register blueprints 
    from ipfs.views import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    return app