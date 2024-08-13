from server import app

import src.route

if __name__ == '__main__':
    app.run(debug=True, port=9988)