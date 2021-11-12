from waitress import serve

from kwork.wsgi import application

# Entry point on your production server

if __name__ == '__main__':
    serve(application, port='8000')
