from server import app
import src.route

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9988)