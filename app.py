from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Функция render_template ищет файл в папке 'templates' и отдает его браузеру
    return render_template('landing.html')

if __name__ == "__main__":
    app.run(debug=True)
