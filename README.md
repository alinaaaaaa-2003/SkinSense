
# ✨ SkinSense: Your skin's health, sensed with intelligence. 💧

#### From image to insight. SkinSense is the intelligent core of an application that provides instant, data-driven analysis and personalized recommendations for a healthier complexion.

-----

### **Overview** 🔬

SkinSense is a powerful web application that turns a simple image into actionable skincare advice. The project is built on a custom-trained **MobileNetV2** deep learning model 🧠, a state-of-the-art vision architecture fine-tuned on several unique, combined datasets from Kaggle 🌿. The model is designed to detect your skin's condition from an image and give you expert recommendations.

### **Model Performance** 📊

The model was meticulously trained and validated to ensure high accuracy and reliable predictions.

  * **Accuracy:** 0.8968 ✅
  * **Macro F1 Score:** 0.8954 ✅

### **Core Features** 🌟

  * **📸 AI-Powered Analysis:** The app instantly classifies skin conditions into one of five categories: `acne`, `wrinkles`, `dark spots`, `puffy eyes`, or `normal` skin.
  * **🌿 Personalized Recommendations:** Based on the analysis, the app provides tailored and expert skincare recommendations to help you achieve a healthier complexion.
  * **🌐 User-Friendly Interface:** Built with Streamlit, the app is a single, elegant webpage with a minimal design that makes your skin scan a seamless and effortless experience.

-----

### **Tools and Frameworks** ⚙️

This project leverages a proven stack for robust performance and reliability.

| Technology | Purpose |
| :--- | :--- |
| **Python** 🐍 | The core programming language. |
| **Streamlit** 🚀 | The framework for the web application. |
| **TensorFlow** 🧠 | The engine for the deep learning model. |
| **Keras** | The high-level API for building the neural network. |
| **Pillow** | For image processing and handling. |
| **NumPy** | For numerical operations and data manipulation. |

### **Try it Here\!** 🚀

Ready to see it in action? Click the link below to open the application in your browser.

#### [**Try it here\!**](https://www.google.com/search?q=http://localhost:8501/)

*Note: This link works only when you have the application running on your local machine. Please follow the setup instructions below to get started.*

### **Local Setup** 💻

Follow these steps to get the SkinSense app running on your local machine.

1.  Clone this repository to your local machine:

    ```bash
    git clone https://your-repository-url
    cd your-repository-name
    ```

2.  Ensure you have the necessary model files in the same directory:

      * `acne_model_architecture.json`
      * `acne_model_weights.weights.h5`

3.  Install the required Python libraries. It's recommended to do this in a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

4.  To launch the app, open your terminal in the project directory and run the following command:

    ```bash
    streamlit run app.py
    ```

### **License** 📜

This project is licensed under the MIT License. See the `LICENSE` file for details.

Made by Alina✨

-----
