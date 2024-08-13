from server import app

@app.route('/')
def index():
    return {"Data": "12345"}