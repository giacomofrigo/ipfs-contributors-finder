import subprocess

from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = False
    app.config["SECRET_KEY"] = "pohu(jkC34&()sjhYN!mLoikdnJ??b7298YSos"
    app.config["IPFS_DAEMON"] = subprocess.Popen(['ipfs', 'daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # register blueprints 
    from ipfs.views import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        blueprint.app = app

    return app