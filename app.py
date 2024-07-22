from flask import Flask, render_template, request
from weather_notifier import get_weather_details

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    source = request.form['source']
    destination = request.form['destination']
    try:
        weather_details = get_weather_details(source, destination)
        return render_template('results.html', weather_details=weather_details)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
