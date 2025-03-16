from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Aditya'

@app.route('/logs')
def read_logs():
    try:
        with open('zenova.log', 'r') as f:
            return Response(f.read(), mimetype="text/plain")
    except FileNotFoundError:
        return Response("Log file not found", status=404)
    except Exception as e:
        return Response(str(e), status=500)

if __name__ == "__main__":
    app.run(debug=True)
