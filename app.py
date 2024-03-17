from ocr.ocr import ocr_bp
from day_planning.day_planning import to_do_bp
from date_converter.date_converter import date_converter_bp
from auto_certification.auto_certification_1 import auto_certification_bp
from flask import Flask, render_template

app = Flask(__name__)

app.config["OUTPUT_FOLDER"] = "output/"
app.config["UPLOAD_FOLDER"] = "uploads/"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':    
    app.register_blueprint(ocr_bp)
    app.register_blueprint(to_do_bp)
    app.register_blueprint(date_converter_bp)
    app.register_blueprint(auto_certification_bp)
    app.run(debug=True)
