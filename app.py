from ipfs import create_app
import logging

if __name__ == '__main__':
    app = create_app()
    app.logger.addHandler(logging.StreamHandler())
    app.run('0.0.0.0', 4444)