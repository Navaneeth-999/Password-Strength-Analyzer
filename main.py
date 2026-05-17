from flask import Flask, render_template, request
import re
import random
import string

app = Flask(__name__)

# Load common passwords
with open("common_passwords.txt", "r") as file:
    common_passwords = file.read().splitlines()


# Function to generate strong password
def generate_strong_password():

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    return ''.join(random.choice(characters) for i in range(12))


# Function to check password strength
def check_password_strength(password):

    # Common password check
    if password.lower() in common_passwords:
        return "Very Weak Password"

    score = 0

    # Length check
    if len(password) >= 8:
        score += 1

    # Uppercase check
    if re.search(r"[A-Z]", password):
        score += 1

    # Lowercase check
    if re.search(r"[a-z]", password):
        score += 1

    # Number check
    if re.search(r"\d", password):
        score += 1

    # Special character check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    # Final strength result
    if score <= 2:
        return "Weak Password"

    elif score <= 4:
        return "Moderate Password"

    else:
        return "Strong Password"


# Home Route
@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    suggestion = ""
    color = ""

    if request.method == "POST":

        password = request.form["password"]

        result = check_password_strength(password)

        # Generate suggestion for weak passwords
        if result == "Weak Password" or result == "Very Weak Password":
            suggestion = generate_strong_password()

        # Strength Colors
        if "Weak" in result:
            color = "red"

        elif "Moderate" in result:
            color = "orange"

        elif "Strong" in result:
            color = "green"

    return render_template(
        "index.html",
        result=result,
        suggestion=suggestion,
        color=color
    )


# Run Application
if __name__ == "__main__":
    app.run(debug=True)