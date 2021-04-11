from ipfs import create_app

if __name__ == '__main__':
    app = create_app()
    app.run('localhost', 4444)