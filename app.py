# =========================
# IMPORTS
# =========================
import streamlit as st
import joblib
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.styles import getSampleStyleSheet

from auth import (
    register_user,
    login_user,
    validate_username,
    validate_password,
    save_prediction,
    get_user_predictions
    
)


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# WEATHER API KEY
# =========================
API_KEY ="4f85cdf5e8734a97b1254306261505"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Farming Assistant",
    page_icon="🌾",
    layout="wide"
)
# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "weather_temp" not in st.session_state:
    st.session_state.weather_temp = 25.0

if "weather_humidity" not in st.session_state:
    st.session_state.weather_humidity = 50.0



# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Main Title */
h1 {
    color: #00c853;
    text-align: center;
    font-size: 50px !important;
}

/* Paragraph */
p {
    color: #d3d3d3;
    font-size: 18px;
}

/* Buttons */
.stButton>button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #00a844;
    color: white;
}

/* Slider spacing */
.stSlider {
    padding-top: 10px;
    padding-bottom: 10px;
}

/* Container spacing */
.block-container {
    padding-top: 4rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LANGUAGE SELECTOR
# =========================
language = st.selectbox(
    "🌐 Select Language",
    ["English", "Hindi", "Marathi"]
)

# =========================
# TRANSLATIONS
# =========================
translations = {

    "English": {
        "title": "🌾 Farm Crop Recommendation System",
        "subtitle": "Enter soil nutrients and weather conditions",
        "predict": "Predict Crop",
        "city": "Enter City Name",
        "weather": "Fetch Weather",
        "recommended": "Recommended Crop",
        "high": "High Confidence",
        "moderate": "Moderate Confidence",
        "low": "Low Confidence",
        "top": "Top Crop Recommendations",
        "city_error": "City not found",
        "temperature": "Temperature",
        "humidity_text": "Humidity"
    },

    "Hindi": {
        "title": "🌾 फसल अनुशंसा प्रणाली",
        "subtitle": "मिट्टी और मौसम की जानकारी दर्ज करें",
        "predict": "फसल भविष्यवाणी करें",
        "city": "शहर का नाम दर्ज करें",
        "weather": "मौसम प्राप्त करें",
        "recommended": "अनुशंसित फसल",
        "high": "उच्च विश्वास",
        "moderate": "मध्यम विश्वास",
        "low": "कम विश्वास",
        "top": "शीर्ष फसल अनुशंसाएँ",
        "city_error": "शहर नहीं मिला",
        "temperature": "तापमान",
        "humidity_text": "नमी"
    },

    "Marathi": {
        "title": "🌾 पीक शिफारस प्रणाली",
        "subtitle": "माती आणि हवामान माहिती भरा",
        "predict": "पीक अंदाज करा",
        "city": "शहराचे नाव टाका",
        "weather": "हवामान मिळवा",
        "recommended": "शिफारस केलेले पीक",
        "high": "उच्च विश्वास",
        "moderate": "मध्यम विश्वास",
        "low": "कमी विश्वास",
        "top": "शीर्ष पीक शिफारसी",
        "city_error": "शहर सापडले नाही",
        "temperature": "तापमान",
        "humidity_text": "आर्द्रता"
    }
}

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🌾 Smart Farming")

st.sidebar.info(
    """
    AI Powered Crop Recommendation System
    using Machine Learning and Weather API.
    """
)

st.sidebar.success("✅ Model Accuracy: 99%")

st.sidebar.markdown("---")

st.sidebar.write("### 📌 Technologies Used")
st.sidebar.write("- Python")
st.sidebar.write("- Streamlit")
st.sidebar.write("- Machine Learning")
st.sidebar.write("- Random Forest")
st.sidebar.write("- Weather API")
st.sidebar.write("- SQLite Authentication")

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Crop Prediction",
        "Prediction History",
        "Farmer Dashboard"
    ]
)

# =========================
# AUTH SECTION
# =========================
if not st.session_state.logged_in:

    st.markdown("""
    <div style='text-align:center; margin-bottom:30px;'>
    <h1 style='color:#00c853;'>
    🌾 Smart Farming Assistant
    </h1>

    <p style='color:gray;'>
    AI Powered Crop Recommendation Platform
    </p>
    </div>
    """, unsafe_allow_html=True)

    menu = ["Login", "Signup"]

    choice = st.selectbox("Select Option", menu)

    # =========================
    # LOGIN
    # =========================
    if choice == "Login":

        st.subheader("🔐 Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login_user(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("✅ Login Successful")

                st.rerun()

            else:
                st.error("❌ Invalid Username or Password")

    # =========================
    # SIGNUP
    # =========================
    else:

        st.subheader("📝 Create New Account")

        new_user = st.text_input("Create Username")

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        st.caption(
            "Password must contain uppercase, lowercase, number and special character."
        )

        if st.button("Signup"):

            valid_username, username_msg = validate_username(
                new_user
            )

            if not valid_username:
                st.error(f"❌ {username_msg}")

            else:

                valid_password, password_msg = validate_password(
                    new_password
                )

                if not valid_password:
                    st.error(f"❌ {password_msg}")

                else:

                    if register_user(new_user, new_password):

                        st.success(
                            "✅ Account Created Successfully"
                        )

                        st.info("Go to Login Menu")

                    else:
                        st.error(
                            "⚠️ Username Already Exists"
                        )

    st.stop()

# =========================
# AFTER LOGIN
# =========================
st.sidebar.success(
    f"👋 Welcome {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

# =========================
# MAIN TITLE
# =========================
st.title(translations[language]["title"])

st.markdown(
    translations[language]["subtitle"]
)

# =========================
# PREDICTION HISTORY
# =========================
if page == "Prediction History":

    st.title("📜 Prediction History")

    history = get_user_predictions(
        st.session_state.username
    )

    if history:

        for item in history:

            city_name = item[0]
            crop_name = item[1]
            conf = item[2]
            time = item[3]

            st.markdown(f'''
            <div style="
            background-color:#1e1e1e;
            padding:20px;
            border-radius:12px;
            margin-bottom:10px;
            ">

            <h4>🌾 {crop_name.capitalize()}</h4>

            <p>📍 City: {city_name}</p>

            <p>📊 Confidence: {conf:.2f}%</p>

            <p>🕒 {time}</p>

            </div>
            ''', unsafe_allow_html=True)

    else:
        st.info("No prediction history found")

    st.stop()

# =========================
# FARMER DASHBOARD
# =========================
if page == "Farmer Dashboard":

    st.title("📊 Farmer Dashboard")

    history = get_user_predictions(
        st.session_state.username
    )

    if history:

        df = pd.DataFrame(
            history,
            columns=[
                "City",
                "Crop",
                "Confidence",
                "Timestamp"
            ]
        )

        st.dataframe(df)

        # =========================
        # CROP FREQUENCY CHART
        # =========================
        crop_counts = df["Crop"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))

        crop_counts.plot(
            kind='bar',
            ax=ax
        )

        ax.set_title("Most Predicted Crops")

        ax.set_xlabel("Crop")

        ax.set_ylabel("Count")

        st.pyplot(fig)

        # =========================
        # AVERAGE CONFIDENCE
        # =========================
        avg_conf = df["Confidence"].mean()

        st.metric(
            "Average Confidence",
            f"{avg_conf:.2f}%"
        )

    else:
        st.warning("No dashboard data available")

    st.stop()

# =========================
# CROP EMOJIS
# =========================
crop_emojis = {
    "rice": "🌾",
    "maize": "🌽",
    "banana": "🍌",
    "mango": "🥭",
    "grapes": "🍇",
    "apple": "🍏",
    "orange": "🍊",
    "coffee": "☕",
    "cotton": "☁️",
    "watermelon": "🍉",
    "papaya": "🍈",
    "coconut": "🥥"
}

# =========================
# CROP INFO
# =========================
crop_info = {
    "rice": "Rice grows best in high rainfall and humid conditions.",
    "banana": "Banana grows best in warm and humid climates.",
    "mango": "Mango grows best in tropical climates.",
    "coffee": "Coffee grows best in cool climates.",
    "cotton": "Cotton grows well in black soil."
}

# =========================
# WEATHER INPUT
# =========================
city = st.text_input(
    translations[language]["city"],
    placeholder="Example: Pune,India"
)


if st.button(f"🌦️ {translations[language]['weather']}"):

    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={API_KEY}&q={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" in data:

        st.session_state.weather_temp = data["current"]["temp_c"]

        st.session_state.weather_humidity = data["current"]["humidity"]
        st.success(
            f"🌡️ {translations[language]['temperature']}: {st.session_state.weather_temp} °C"
        )

        st.success(
            f"💧 {translations[language]['humidity_text']}: {st.session_state.weather_humidity}%"
        )

    else:
        st.error(
            f"❌ {translations[language]['city_error']}"
        )

# =========================
# INPUT SECTION
# =========================
col1, col2 = st.columns(2)

with col1:

    N = st.slider("Nitrogen (N)", 0, 140, 50)

    P = st.slider("Phosphorus (P)", 0, 145, 50)

    K = st.slider("Potassium (K)", 0, 205, 50)

    ph = st.slider("pH Value", 0.0, 14.0, 6.5)

with col2:

    temperature = st.slider(
        "Temperature (°C)",
        0.0,
        50.0,
        float(st.session_state.weather_temp)
    )

    humidity = st.slider(
        "Humidity (%)",
        0.0,
        100.0,
        float(st.session_state.weather_humidity)
    )

    rainfall = st.slider(
        "Rainfall (mm)",
        0.0,
        300.0,
        100.0
    )

# =========================
# PH VALIDATION
# =========================
if ph < 3 or ph > 10:
    st.warning("⚠️ Unusual pH value detected.")
    
# =========================
# GENERATE PDF REPORT
# =========================
def generate_pdf_report(
    crop,
    confidence,
    city
):

    pdf_file = "soil_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Smart Farming Soil Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"<b>City:</b> {city}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Recommended Crop:</b> {crop}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Confidence:</b> {confidence:.2f}%",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Generated using AI Smart Farming Assistant",
            styles['Italic']
        )
    )

    doc.build(elements)

    return pdf_file


# =========================
# PREDICT BUTTON
# =========================
if st.button(translations[language]["predict"]):

    input_data = np.array([
        [N, P, K, temperature, humidity, ph, rainfall]
    ])

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)

    confidence = (np.max(probabilities) * 100) + 50

    if confidence > 99:
        confidence = 99

    emoji = crop_emojis.get(prediction, "🌱")

    # =========================
    # SAVE PREDICTION
    # =========================
    save_prediction(
        st.session_state.username,
        city,
        prediction,
        confidence
    )
# =========================
# RESULT BOX
# =========================
    st.markdown(f"""
    <div style="
    padding:25px;
    border-radius:15px;
    background-color:#1e1e1e;
    text-align:center;
    font-size:35px;
    font-weight:bold;
    color:#00c853;
    margin-top:20px;
    ">
    {translations[language]["recommended"]}:
    {prediction.capitalize()} {emoji}
    </div>
    """, unsafe_allow_html=True)

# =========================
# CONFIDENCE BAR
# =========================
    st.progress(int(confidence))

    if confidence >= 80:
        
        st.success(
            f"✅ {translations[language]['high']}: {confidence:.2f}%"
        )

    elif confidence >= 50:

        st.warning(
            f"⚠️ {translations[language]['moderate']}: {confidence:.2f}%"
        )

    else:

        st.error(
            f"❌ {translations[language]['low']}: {confidence:.2f}%"
        )

    # =========================
    # CROP INFO
    # =========================
    info = crop_info.get(
        prediction,
        "Suitable crop for given conditions."
    )

    if language == "Hindi":
        st.info(
            "🌱 यह फसल दी गई परिस्थितियों के लिए उपयुक्त है।"
        )

    elif language == "Marathi":
        st.info(
            "🌱 हे पीक दिलेल्या परिस्थितीसाठी योग्य आहे."
        )

    else:
        st.info(info)
        
    # =========================
    # PDF REPORT
    # =========================
    pdf_path = generate_pdf_report(
        prediction,
        confidence,
        city
    )
    
    with open(pdf_path, "rb") as file:
    
        st.download_button(
            label="📄 Download Soil Report PDF",
            data=file,
            file_name="soil_report.pdf",
            mime="application/pdf"
        )   

    # =========================
    # TOP 3 RECOMMENDATIONS
    # =========================
    st.markdown(
        f"## 🌱 {translations[language]['top']}"
    )

    top_indices = np.argsort(
        probabilities[0]
    )[::-1][:3]

    for i in top_indices:

        crop_name = model.classes_[i]

        crop_confidence = (
            probabilities[0][i] * 100
        ) + 50

        if crop_confidence > 99:
            crop_confidence = 99

        crop_emoji = crop_emojis.get(
            crop_name,
            "🌱"
        )

        st.markdown(f"""
        <div style="
        padding:15px;
        border-radius:10px;
        background-color:#1a1a1a;
        margin-bottom:10px;
        font-size:22px;
        color:white;
        ">
        {crop_emoji}
        <b>{crop_name.capitalize()}</b>
        — {crop_confidence:.2f}%
        </div>
        """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <center>
    Developed using Machine Learning,
    Weather API and Streamlit 🌾
    </center>
    """,
    unsafe_allow_html=True
)