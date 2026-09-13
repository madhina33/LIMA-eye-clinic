import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Diagnostic Severity and Clinical Information Mapping
DISEASE_INFO = {
    "No Diabetic Retinopathy (Normal)": {
        "status": "Healthy Retinal Scan",
        "badge": "success",
        "description": "No signs of diabetic retinopathy were detected in the provided scan.",
        "precautions": [
            "Maintain healthy blood sugar levels through regular monitoring.",
            "Follow a balanced diet rich in leafy greens, omega-3 fatty acids, and antioxidants.",
            "Engage in regular physical activity to maintain optimal cardiovascular health."
        ],
        "treatment": "No active medical or surgical treatment required. Preventive care only.",
        "consultation": "Routine annual check-up (Consult optometrist once a year)"
    },
    "Mild Non-Proliferative Retinopathy": {
        "status": "Early Stage Detected",
        "badge": "warning",
        "description": "Microaneurysms detected. Small areas of balloon-like swelling in the retina's tiny blood vessels.",
        "precautions": [
            "Strict glycemic control (HbA1c monitoring every 3 months).",
            "Blood pressure management (< 130/80 mmHg).",
            "Immediate report of any sudden blurring or vision changes."
        ],
        "treatment": "Observation and systemic risk factor management. No laser treatment necessary at this stage.",
        "consultation": "Every 6 months (Ophthalmologist/Retinal Specialist)"
    },
    "Moderate Non-Proliferative Retinopathy": {
        "status": "Moderate Risk Detected",
        "badge": "warning",
        "description": "Blood vessels nourishing the retina are blocked, altering blood supply.",
        "precautions": [
            "Rigorous diabetic diet and adherence to prescribed medications/insulin.",
            "Avoid strenuous heavy lifting or high-impact activities that spike blood pressure.",
            "Regular kidney function monitoring (as diabetic microvascular changes correlate)."
        ],
        "treatment": "Close medical monitoring. Referral for specialized retinal evaluation.",
        "consultation": "Every 3 to 4 months"
    },
    "Severe Non-Proliferative Retinopathy": {
        "status": "High Risk - Medical Intervention Needed",
        "badge": "danger",
        "description": "Many blood vessels are blocked, depriving the retina of blood supply, triggering signals for new vessel growth.",
        "precautions": [
            "Urgent blood sugar stabilization under medical supervision.",
            "Avoid heavy physical strain, bending down, or lifting heavy objects.",
            "Report any sudden vision loss or floaters immediately."
        ],
        "treatment": "Urgent Panretinal Photocoagulation (PRP) laser therapy may be considered to prevent severe vision loss.",
        "consultation": "Immediate/Urgent consultation with a senior retinal specialist"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        return render_template('result.html', prediction="Moderate Non-Proliferative Retinopathy", info=DISEASE_INFO.get("Moderate Non-Proliferative Retinopathy"), image_path=None)
    return render_template('predict.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return render_template('result.html', prediction="Severe Non-Proliferative Retinopathy", info=DISEASE_INFO.get("Severe Non-Proliferative Retinopathy"), image_path=filename)
        return render_template('result.html', prediction="Severe Non-Proliferative Retinopathy", info=DISEASE_INFO.get("Severe Non-Proliferative Retinopathy"), image_path=None)
    return render_template('upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)