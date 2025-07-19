from flask import Flask, render_template, request, session
from captcha.image import ImageCaptcha
from cryptography.fernet import Fernet
import os, random, string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load encryption key
with open("encryption_key.key", "rb") as file:
    key = file.read()
fernet = Fernet(key)

@app.route("/")
def login():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    image = ImageCaptcha()
    image_path = f"static/captcha/captcha.png"
    image.write(captcha_text, image_path)

    # Encrypt the CAPTCHA
    encrypted = fernet.encrypt(captcha_text.encode())
    session["captcha"] = encrypted

    return render_template("login.html", image_path=image_path)

@app.route("/verify", methods=["POST"])
def verify():
    user_input = request.form["captcha_input"]
    encrypted = session.get("captcha", None)

    if not encrypted:
        return "Session expired. Refresh the page."

    try:
        decrypted = fernet.decrypt(encrypted).decode()
        if user_input.strip().upper() == decrypted:
            return "✅ CAPTCHA correct. Login successful."
        else:
            return "❌ CAPTCHA incorrect. Try again."
    except:
        return "⚠️ CAPTCHA validation error."

if __name__ == "__main__":
    app.run(debug=True)
