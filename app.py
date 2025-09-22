import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.models import model_from_json
from PIL import Image
from io import BytesIO
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes, allowing the web app to make requests to this API.
CORS(app)

# Define image dimensions and class names
IMG_HEIGHT = 224
IMG_WIDTH = 224
class_names = ['acne', 'dark spots', 'normal', 'puffy eyes', 'wrinkles']

# Create a dictionary of recommendations for each class, based on your provided logic.
recommendations = {
    'acne': "Recommendation: Use a gentle, non-comedogenic cleanser. Avoid touching your face and consider over-the-counter treatments with benzoyl peroxide or salicylic acid. For persistent cases, consult a dermatologist.",
    'dark spots': "Recommendation: Use a daily sunscreen with SPF 30 or higher to prevent further hyperpigmentation. Products containing Vitamin C, niacinamide, or retinoids can help fade existing spots. Consult a dermatologist for professional treatments.",
    'normal': "Recommendation: Your skin appears healthy and balanced! Maintain your routine with a daily cleanser, moisturizer, and broad-spectrum sunscreen. Listen to your skin's needs and stay hydrated.",
    'puffy eyes': "Recommendation: Get adequate sleep and reduce sodium intake. Applying a cool compress or an eye cream with caffeine can help. Gently massage the area to improve circulation.",
    'wrinkles': "Recommendation: Use products with anti-aging ingredients like retinoids, peptides, and antioxidants. Consistent sunscreen use is crucial to prevent further signs of aging. Stay hydrated and consider a healthy lifestyle."
}

# Load the model once when the application starts
try:
    with open('acne_model_architecture.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('acne_model_weights.weights.h5')
    print("Model loaded successfully.")
    
except Exception as e:
    print(f"Error loading model: {e}")
    loaded_model = None

# A simple helper function to preprocess the image
def preprocess_image(image_bytes):
    """
    Loads, resizes, and normalizes an image from a byte stream.
    """
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_HEIGHT, IMG_WIDTH))
    img_array = np.array(img, dtype=np.float32)
    img_array = (img_array * 2.0 / 255.0) - 1.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Define the prediction API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles POST requests with an image file to make a prediction.
    """
    if loaded_model is None:
        return jsonify({"error": "Model not loaded"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            image_bytes = file.read()
            processed_image = preprocess_image(image_bytes)
            
            # Make a prediction
            predictions = loaded_model.predict(processed_image)
            
            # Get the predicted class and confidence
            predicted_class_index = np.argmax(predictions)
            predicted_class = class_names[predicted_class_index]
            confidence = np.max(predictions)
            
            # Get the recommendation from the dictionary
            recommendation_text = recommendations.get(predicted_class, "No specific recommendation available for this skin condition.")
            
            # Return the result as a JSON object
            return jsonify({
                "predicted_class": predicted_class,
                "confidence": float(confidence),
                "recommendation": recommendation_text
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible from external machines
    # Debug is set to True for development purposes, but should be False in production
    app.run(host='0.0.0.0', port=5000, debug=True)