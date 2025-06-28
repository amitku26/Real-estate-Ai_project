# import streamlit as st
# import requests
# import streamlit.components.v1 as components
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader

# # ---------- Page Setup ----------
# st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

# # ---------- Load Auth Config ----------
# with open('./config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

# # ---------- User Login ----------
# auth_result = authenticator.login(location="main")

# if auth_result is not None:
#     name = auth_result["name"]
#     auth_status = auth_result["authenticated"]
#     username = auth_result["username"]
# else:
#     name = username = None
#     auth_status = None

# # ---------- Auth Handling ----------
# if auth_status is False:
#     st.error("❌ Incorrect username or password")
# elif auth_status is None:
#     st.warning("🛡️ Please enter your login details")
# elif auth_status:
#     authenticator.logout("🔓 Logout", "sidebar")
#     st.sidebar.success(f"✅ Logged in as: {name}")

#     # ---------- Custom Styling ----------
#     custom_css = """
#     <style>
#         .main {
#             background-color: #f8f9fa;
#             font-family: 'Segoe UI', sans-serif;
#         }
#         .stButton>button {
#             background-color: #0f4c81;
#             color: white;
#             font-size: 1rem;
#             padding: 0.5rem 1.2rem;
#             border-radius: 6px;
#         }
#         .stButton>button:hover {
#             background-color: #083c6c;
#         }
#     </style>
#     """
#     st.markdown(custom_css, unsafe_allow_html=True)

#     # ---------- Title ----------
#     st.markdown("<h2 style='color:#0f4c81;'>🏠 Real Estate Price & Risk Prediction</h2>", unsafe_allow_html=True)
#     st.markdown("Enter the property details below to get an estimated price and risk score.")

#     # ---------- Input Section ----------
#     st.markdown("### 📋 Property Details")
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col1:
#         bhk = st.number_input("BHK", 1, 5, step=1, key="input_bhk")
#     with col2:
#         area = st.number_input("Area (sqft)", 500, 10000, step=100, key="input_area")
#     with col3:
#         flood_zone = st.selectbox("Flood Zone", options=[0, 1, 2], format_func=lambda x: f"Zone {x}", key="input_flood")

#     # ---------- Predict Button ----------
#     if st.button("🔍 Predict Price & Risk", key="predict_button"):
#         payload = {"bhk": bhk, "area": area, "floodZone": flood_zone}
#         try:
#             res = requests.post("http://localhost:5000/api/predict", json=payload)
#             if res.ok:
#                 result = res.json()
#                 price = result["predicted_price"]
#                 risk = result["risk_score"]

#                 st.success(f"💰 Estimated Price: ₹{price} Lakhs")
#                 st.info(f"⚠️ Risk Score: {risk} / 100")

#                 # ---------- Risk Visualization ----------
#                 components.html(f"""
#                 <div style='margin-top:30px;'>
#                     <h4>📊 Risk Visualization</h4>
#                     <div style="width:100%; max-width:400px;">
#                         <svg width="100%" viewBox="0 0 200 100">
#                             <defs>
#                                 <linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
#                                     <stop offset="0%" stop-color="#3ac569"/>
#                                     <stop offset="50%" stop-color="#fbc634"/>
#                                     <stop offset="100%" stop-color="#f34a4a"/>
#                                 </linearGradient>
#                             </defs>
#                             <path d="M10,100 A90,90 0 0,1 190,100" fill="none" stroke="url(#g)" stroke-width="20" />
#                             <circle cx="{10 + 180 * risk / 100}" cy="100" r="10" fill="#000"/>
#                         </svg>
#                     </div>
#                 </div>
#                 """, height=180)
#             else:
#                 st.error("❌ Prediction failed. Check Flask API server.")
#         except Exception as e:
#             st.error(f"❌ Error contacting API: {e}")



# import streamlit as st
# import sqlite3
# import bcrypt

# # --- DB Setup ---
# conn = sqlite3.connect('users.db')
# c = conn.cursor()
# c.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL UNIQUE,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')
# conn.commit()

# # --- Utility Functions ---
# def hash_password(password):
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# def verify_password(password, hashed):
#     return bcrypt.checkpw(password.encode(), hashed.encode())

# def add_user(username, email, password):
#     try:
#         c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
#                   (username, email, hash_password(password)))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False

# def login_user(username, password):
#     c.execute("SELECT * FROM users WHERE username=?", (username,))
#     user = c.fetchone()
#     if user and verify_password(password, user[3]):
#         return user
#     return None

# # --- UI Config ---
# st.set_page_config(page_title="Real Estate Auth App", layout="centered")

# # --- Sidebar Navigation ---
# st.sidebar.title("🔐 Auth Panel")
# page = st.sidebar.radio("Choose Page", ["Login", "Register"])

# # --- Login Page ---
# if page == "Login":
#     st.title("🟢 Login to Dashboard")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         user = login_user(username, password)
#         if user:
#             st.success(f"Welcome back, {user[1]} 👋")
#             st.markdown("---")
#             st.header("🏠 Real Estate Dashboard")
#             st.info("✅ You are now logged in!")

#             # Add your dashboard logic here
#             col1, col2 = st.columns(2)
#             bhk = col1.number_input("BHK", 1, 5, step=1, key="bhk_input")
#             area = col2.number_input("Area (sqft)", 500, 10000, step=100, key="area_input")
#             flood = st.selectbox("Flood Zone", options=[0, 1, 2])

#             if st.button("Predict Price & Risk"):
#                 # Replace this with your model/API logic
#                 st.success("💰 Estimated Price: ₹80 Lakhs")
#                 st.info("⚠️ Risk Score: 35 / 100")
#         else:
#             st.error("❌ Invalid username or password")

# # --- Register Page ---
# elif page == "Register":
#     st.title("📝 Create New Account")
#     new_user = st.text_input("Username")
#     email = st.text_input("Email")
#     new_pass = st.text_input("Password", type="password")
#     confirm_pass = st.text_input("Confirm Password", type="password")

#     if st.button("Register"):
#         if new_pass != confirm_pass:
#             st.warning("⚠️ Passwords do not match")
#         elif not new_user or not email or not new_pass:
#             st.warning("⚠️ Please fill all fields")
#         else:
#             if add_user(new_user, email, new_pass):
#                 st.success("✅ Registered successfully! Please log in.")
#             else:
#                 st.error("❌ Username already exists")

# import streamlit as st
# import requests
# import yaml
# import streamlit_authenticator as stauth
# from yaml.loader import SafeLoader
# import streamlit.components.v1 as components

# # ---------- Page Config ----------
# st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

# # ---------- Load Login Credentials ----------
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
# )

# # ---------- Login Sidebar ----------
# authenticator.login('Login', 'sidebar')

# if st.session_state["authentication_status"]:
#     authenticator.logout("Logout", "sidebar")
#     st.sidebar.success(f"✅ Logged in as: {st.session_state['name']}")

#     # ---------- Custom Styling ----------
#     st.markdown("""
#         <style>
#             .main {
#                 background-color: #f5f7fa;
#                 font-family: 'Segoe UI', sans-serif;
#                 padding: 1.5rem;
#             }
#             .stButton>button {
#                 background-color: #0f4c81;
#                 color: white;
#                 font-size: 1rem;
#                 padding: 0.6rem 1.5rem;
#                 border-radius: 8px;
#             }
#             .stButton>button:hover {
#                 background-color: #083c6c;
#             }
#         </style>
#     """, unsafe_allow_html=True)

#     # ---------- Dashboard UI ----------
#     st.markdown("<h2 style='color:#0f4c81;'>🏠 Real Estate Price & Risk Prediction</h2>", unsafe_allow_html=True)
#     st.markdown("Fill in the details below to get an estimated price and risk score.")

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         bhk = st.number_input("BHK", 1, 5, step=1, key="bhk")
#     with col2:
#         area = st.number_input("Area (sqft)", 500, 10000, step=100, key="area")
#     with col3:
#         flood_zone = st.selectbox("Flood Zone", options=[0, 1, 2], format_func=lambda x: f"Zone {x}", key="flood")

#     if st.button("🔍 Predict Price & Risk"):
#         payload = {"bhk": bhk, "area": area, "floodZone": flood_zone}
#         try:
#             response = requests.post("http://localhost:5000/api/predict", json=payload)
#             if response.ok:
#                 result = response.json()
#                 st.success(f"💰 Estimated Price: ₹{result['predicted_price']} Lakhs")
#                 st.info(f"⚠️ Risk Score: {result['risk_score']} / 100")

#                 # ---------- Risk Gauge ----------
#                 components.html(f"""
#                     <div style='margin-top:30px;'>
#                         <h4>📊 Risk Visualization</h4>
#                         <div style="width:100%; max-width:400px;">
#                             <svg width="100%" viewBox="0 0 200 100">
#                                 <defs>
#                                     <linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
#                                         <stop offset="0%" stop-color="#3ac569"/>
#                                         <stop offset="50%" stop-color="#fbc634"/>
#                                         <stop offset="100%" stop-color="#f34a4a"/>
#                                     </linearGradient>
#                                 </defs>
#                                 <path d="M10,100 A90,90 0 0,1 190,100" fill="none" stroke="url(#g)" stroke-width="20" />
#                                 <circle cx="{10 + 180 * result['risk_score'] / 100}" cy="100" r="10" fill="#000"/>
#                             </svg>
#                         </div>
#                     </div>
#                 """, height=180)
#             else:
#                 st.error("❌ API Error: Unable to fetch prediction.")
#         except Exception as e:
#             st.error(f"🚨 Error connecting to API: {e}")

# elif st.session_state["authentication_status"] is False:
#     st.error("❌ Incorrect username or password.")
# elif st.session_state["authentication_status"] is None:
#     st.warning("🔐 Please enter your login credentials.")


import streamlit as st
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit.components.v1 as components

# ---------------------------- PAGE CONFIG ----------------------------
st.set_page_config(page_title="🏠 Real Estate Dashboard", layout="wide")

# ---------------------------- LOAD CONFIG ----------------------------
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# ---------------------------- LOGIN UI ----------------------------
authenticator.login(location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"✅ Logged in as: {st.session_state['name']}")

    # -------------------- DASHBOARD UI --------------------
    st.markdown("""
    <style>
        .main {
            background-color: #f4f6f8;
            font-family: 'Segoe UI', sans-serif;
            padding: 2rem;
        }
        .stButton>button {
            background-color: #0f4c81;
            color: white;
            font-size: 1rem;
            padding: 0.5rem 1.2rem;
            border-radius: 6px;
        }
        .stButton>button:hover {
            background-color: #083c6c;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#0f4c81;'>🏠 Real Estate Price & Risk Prediction</h2>", unsafe_allow_html=True)
    st.markdown("Enter the property details below to get an estimated price and risk score.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        bhk = st.number_input("BHK", 1, 5, step=1, key="input_bhk")
    with col2:
        area = st.number_input("Area (sqft)", 500, 10000, step=100, key="input_area")
    with col3:
        flood_zone = st.selectbox("Flood Zone", options=[0, 1, 2], format_func=lambda x: f"Zone {x}", key="input_flood")

    if st.button("🔍 Predict Price & Risk", key="predict_button"):
        payload = {"bhk": bhk, "area": area, "floodZone": flood_zone}
        try:
            res = requests.post("http://localhost:5000/api/predict", json=payload)
            if res.ok:
                result = res.json()
                price = result["predicted_price"]
                risk = result["risk_score"]

                st.success(f"💰 Estimated Price: ₹{price} Lakhs")
                st.info(f"⚠️ Risk Score: {risk} / 100")

                components.html(f"""
                <div style='margin-top:30px;'>
                    <h4>📊 Risk Visualization</h4>
                    <div style="width:100%; max-width:400px;">
                        <svg width="100%" viewBox="0 0 200 100">
                            <defs>
                                <linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
                                    <stop offset="0%" stop-color="#3ac569"/>
                                    <stop offset="50%" stop-color="#fbc634"/>
                                    <stop offset="100%" stop-color="#f34a4a"/>
                                </linearGradient>
                            </defs>
                            <path d="M10,100 A90,90 0 0,1 190,100" fill="none" stroke="url(#g)" stroke-width="20" />
                            <circle cx="{10 + 180 * risk / 100}" cy="100" r="10" fill="#000"/>
                        </svg>
                    </div>
                </div>
                """, height=180)
            else:
                st.error("❌ Prediction failed. Check API server.")
        except Exception as e:
            st.error(f"❌ Error contacting API: {e}")

elif st.session_state["authentication_status"] is False:
    st.error("❌ Incorrect username or password")
elif st.session_state["authentication_status"] is None:
    st.warning("🛡️ Please enter your login credentials")
