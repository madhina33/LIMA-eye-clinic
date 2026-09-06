import os
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Upload folder configuration
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load our trained Retinal Disease Model
MODEL_PATH = 'models/retinal_model.h5'
model = None
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("LIMA Model loaded successfully!")

# Class labels for Diabetic Retinopathy (APTOS 2019 dataset classes)
CLASSES = {
    0: "No Diabetic Retinopathy (Healthy)",
    1: "Mild Non-Proliferative Retinopathy",
    2: "Moderate Non-Proliferative Retinopathy",
    3: "Severe Non-Proliferative Retinopathy",
    4: "Proliferative Diabetic Retinopathy (Critical)"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        if model is None:
            return "Model not found! Please train the model first."

        # Preprocess image for the model
        img = image.load_img(filepath, target_size=(224, 224))
        x = image.img_to_array(img)
        x = x / 255.0
        x = np.expand_dims(x, axis=0)
        
        # Predict
        preds = model.predict(x)
        class_idx = np.argmax(preds[0])
        confidence = float(np.max(preds[0])) * 100
        
        result_text = CLASSES.get(class_idx, "Unknown")
        
        return render_template('result.html', 
                               prediction=result_text, 
                               confidence=round(confidence, 2),
                               image_path=filepath)
@app.route('/diseases')
def diseases():
    return render_template('diseases.html')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)