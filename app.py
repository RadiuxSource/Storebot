from flask import Flask, jsonify
import datetime
import pytz

app = Flask(__name__)

def get_india_time():
    tz_Mumbai = pytz.timezone('Asia/Kolkata')
    datetime_Mumbai = datetime.datetime.now(tz_Mumbai)
    return datetime_Mumbai.strftime('%Y-%m-%d %I:%M:%S %p')

@app.route('/')
def hello_world():
    bot_active = True  # assume the bot is active
    india_time = get_india_time()
    response = {'bot_active': bot_active, 'current_time': india_time}
    return jsonify(response)

if __name__ == "__main__":
    app.run()