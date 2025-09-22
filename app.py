import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from PIL import Image
import numpy as np
import io

# Define image dimensions and class names
IMG_HEIGHT = 224
IMG_WIDTH = 224
class_names = ['acne', 'dark spots', 'normal', 'puffy eyes', 'wrinkles']

# Recommendations dictionary
recommendations = {
    'acne': "✨ Use a gentle, non-comedogenic cleanser. Avoid touching your face and try treatments with benzoyl peroxide or salicylic acid. For persistent cases, consult a dermatologist.",
    'dark spots': "🌞 Always apply sunscreen SPF 30+ to prevent further spots. Products with Vitamin C, niacinamide, or retinoids can help fade marks.",
    'normal': "💧 Your skin looks balanced and healthy! Keep up your routine: cleanser, moisturizer, and sunscreen. Stay hydrated and listen to your skin.",
    'puffy eyes': "😴 Ensure proper sleep and reduce sodium intake. Try a cool compress or caffeine-based eye cream. Gentle massage boosts circulation.",
    'wrinkles': "🌿 Use anti-aging ingredients like retinoids, peptides, and antioxidants. Daily sunscreen is key. Stay hydrated and maintain a healthy lifestyle."
}

# Streamlit page config
st.set_page_config(
    page_title="SkinSense",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f7f5, #f9fdfd);
    }

    /* Glowing Header */
    h1 {
        text-align: center;
        font-weight: 2000;
        color: #009688;
        text-shadow: 0 0 20px #80cbc4, 0 0 40px #4db6ac;
        margin-bottom: 0.8rem;
        font-size: 15rem;
    }

    .subheader {
        text-align: center;
        color: #26a69a;
        font-style: italic;
        font-size: 2rem;
        margin-bottom: 2rem;
    }

/* Transparent centered uploader button */
[data-testid="stFileUploaderDropzone"] {
    width: 220px !important;
    height: 50px !important;
    margin: auto !important;
    border-radius: 10px !important;
    background-color: transparent !important;
    border: 2px dashed #bdbdbd !important; /* subtle dashed border */
    box-shadow: none !important;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    flex-direction: column;  
}

/* Hover effect */
[data-testid="stFileUploaderDropzone"]:hover {
    background-color: rgba(158, 158, 158, 0.1) !important;
    transform: scale(1.05);
}

/* Hide Streamlit’s default drag-drop text */
[data-testid="stFileUploaderDropzone"] div div span {
    display: none !important;
}

/* Custom "Drag & Drop" text above button */
[data-testid="stFileUploaderDropzone"]::before {
    content: "Click to scan your skin";
    font-size: 0.75rem;        /* smaller font */
    font-weight: 600;
    color: #9e9e9e;            /* light grey */
    margin-bottom: 5px;
    text-align: center;
    display: block;
}

/* Text inside the button (Browse/Click) */
[data-testid="stFileUploaderDropzone"] div { 
    font-size: 0.2rem !important;
    font-weight: 200 !important;
    color: #009688 !important; /* teal */
}

.result-card {
    background: linear-gradient(135deg, #e0f2f1, #ffffff); /* same gradient as recommendation */
    border-left: 6px solid #009688; /* dark teal accent */
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    text-align: center;
    font-size: 1.05rem;
    line-height: 1.6;
    animation: fadeIn 1.5s ease-in-out;
}

.result-card h4 {
    color: #004d40; /* dark teal header */
    font-weight: 700;
    margin-bottom: 0.8rem;
}


    /* Fancy Recommendation Card */
    .recommendation-card {
        background: linear-gradient(135deg, #e0f2f1, #ffffff);
        border-left: 6px solid #009688;
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        font-size: 1.05rem;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-in-out;
    }
    .recommendation-card h4 {
        color: #004d40;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        with open('acne_model_architecture.json', 'r') as json_file:
            loaded_model_json = json_file.read()
        
        model = model_from_json(loaded_model_json)
        model.load_weights('acne_model_weights.weights.h5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# --- HEADER SECTION ---
st.markdown("<h1>SkinSense</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Your skin's health, sensed with intelligence 🌿</p>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
with st.container(border=True):
    st.markdown("<h3 style='color:#004d40; text-align:center;'>Your Skin Analysis</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Upload a picture and let SkinSense reveal the secrets to a glowing complexion ✨</p><br><br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="unique_uploader_key")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Image for Analysis", use_container_width=True)
        
        if model is not None:
            with st.spinner('Analyzing your image...'):
                my_bar = st.progress(0)
                
                image_bytes = uploaded_file.read()
                img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
                my_bar.progress(30)
                
                img = img.resize((IMG_HEIGHT, IMG_WIDTH))
                img_array = np.array(img, dtype=np.float32)
                img_array = (img_array * 2.0 / 255.0) - 1.0
                img_array = np.expand_dims(img_array, axis=0)
                my_bar.progress(60)
                
                predictions = model.predict(img_array)
                predicted_class_index = np.argmax(predictions)
                predicted_class = class_names[predicted_class_index]
                confidence = np.max(predictions) * 100
                my_bar.progress(100)
                
                st.markdown(
                    f"<div class='result-card'>"
                    f"<h4>✅ Analysis Complete!</h4>"
                    f"<p><strong>Condition:</strong> <span style='color:#004d40; font-size:1.3em; font-weight:600;'>{predicted_class.title()}</span></p>"
                    f"<p><strong>Confidence:</strong> <span style='color:#00796b;'>{confidence:.2f}%</span></p>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"<div class='recommendation-card'>"
                    f"<h4>💡 Your Personalized Recommendation:</h4>"
                    f"<p>{recommendations.get(predicted_class, 'No specific recommendation available for this skin condition.')}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.error("Model could not be loaded. Please check your model files.")
    else:
        st.markdown("<p style='text-align: center; color: #555; margin-top: 1rem;'><br><br><br>🌸 The journey to healthy skin starts here. Upload your picture to begin!</p>", unsafe_allow_html=True)

