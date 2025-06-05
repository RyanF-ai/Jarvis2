
import streamlit as st
import pandas as pd
import numpy as np
from hashlib import sha256

# Dummy user database with one example user (email: user@example.com, password: password123)
USERS = {
    "user@example.com": sha256("password123".encode()).hexdigest(),
}

# Simulated contact form handler (placeholder for real email integration)
def process_contact_form(name, email, message):
    st.success(f"Thank you, {name}. Your message has been sent!")

# ROI calculator function
# Calculates annual return on investment based on purchase price, monthly income, and expenses
def calculate_roi(purchase_price, rental_income, expenses):
    annual_income = rental_income * 12
    annual_expenses = expenses * 12
    roi = ((annual_income - annual_expenses) / purchase_price) * 100
    return roi

# Login function to handle user authentication
# Uses Streamlit sidebar for input fields
# Compares hashed password with stored value in USERS
def login():
    st.sidebar.title("🔐 Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    hashed_pw = sha256(password.encode()).hexdigest()

    # On button click, check credentials
    if st.sidebar.button("Login"):
        if USERS.get(email) == hashed_pw:
            st.session_state["authenticated"] = True
            st.session_state["user"] = email
        else:
            st.sidebar.error("Invalid email or password")

# Main app logic
# Handles login status, UI layout, and tabbed interface
def main():
    st.set_page_config(page_title="Jarvis2 Real Estate Agent", layout="wide")

    # Initialize login state if not already present
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Display login screen if not authenticated
    if not st.session_state["authenticated"]:
        login()
        return

    # Main UI after successful login
    st.title("🤖 Welcome to Jarvis2")
    st.subheader(f"Logged in as {st.session_state['user']}")

    # Define four tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Property Search", "📊 ROI Calculator", "📩 Contact Jarvis2", "🔓 Logout"])

    # ----- Tab 1: Property Search -----
    with tab1:
        st.header("Property Search")
        try:
            # Load property data from a CSV file
            df = pd.read_csv("properties.csv")
            st.dataframe(df)  # Display full data before filtering

            # Filter by city
            city_filter = st.selectbox("Select City", options=["All"] + df["City"].unique().tolist())
            if city_filter != "All":
                df = df[df["City"] == city_filter]

            # Filter by price range using a slider
            price_range = st.slider(
                "Price Range",
                min_value=int(df["Price"].min()),
                max_value=int(df["Price"].max()),
                value=(int(df["Price"].min()), int(df["Price"].max()))
            )
            df_filtered = df[(df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1])]
            st.dataframe(df_filtered)  # Display filtered data

        except FileNotFoundError:
            # Inform user if CSV file is missing
            st.warning("Property CSV file not found. Please upload 'properties.csv' to view property listings.")

    # ----- Tab 2: ROI Calculator -----
    with tab2:
        st.header("Investment ROI Calculator")

        # Input fields for investment values
        price = st.number_input("Purchase Price ($)", min_value=10000.0, step=1000.0)
        income = st.number_input("Monthly Rental Income ($)", min_value=0.0, step=100.0)
        expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, step=100.0)

        # Calculate ROI on button click
        if st.button("Calculate ROI"):
            roi = calculate_roi(price, income, expenses)
            st.success(f"Estimated ROI: {roi:.2f}%")

    # ----- Tab 3: Contact Form -----
    with tab3:
        st.header("Contact Jarvis2")
        with st.form("contact_form"):
            # Form fields for contacting
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Your Message")
            submitted = st.form_submit_button("Send Message")

            # Simulate sending form
            if submitted:
                process_contact_form(name, email, message)

    # ----- Tab 4: Logout -----
    with tab4:
        # Reset session state and reload app
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
