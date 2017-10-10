from app import create_app

app = create_app('develop')

if __name__ == '__main__':
    app.run(threaded=True)
