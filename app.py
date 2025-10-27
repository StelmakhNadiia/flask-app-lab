from flask import Flask, request, redirect, url_for, render_template, session, flash, make_response

app = Flask(__name__)
app.secret_key = "secret_key_12345"

users = {
    "Nadiia": "123456",
    "admin": "adminpass"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("login")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("get_profile"))
        else:
            flash("Невірне ім'я користувача або пароль", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if "username" not in session:
        flash("Будь ласка, увійдіть у систему", "warning")
        return redirect(url_for("login"))

    username_value = session["username"]
    response = make_response(render_template("profile.html", username=username_value, cookies=request.cookies))

    # Додавання кукі
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            key = request.form.get("key")
            value = request.form.get("value")
            duration = int(request.form.get("duration", 60))
            if key and value:
                response.set_cookie(key, value, max_age=duration)
                flash(f"Кука '{key}' додана успішно!", "success")
            else:
                flash("Будь ласка, заповніть ключ і значення", "danger")

        elif action == "delete":
            key = request.form.get("key")
            if key:
                response.delete_cookie(key)
                flash(f"Кука '{key}' видалена", "info")
            else:
                # Видалити всі кукі
                for k in request.cookies.keys():
                    response.delete_cookie(k)
                flash("Усі кукі видалено", "info")

    return response

# Маршрут для зміни теми
@app.route("/set_theme/<theme>")
def set_theme(theme):
    if "username" not in session:
        flash("Будь ласка, увійдіть у систему", "warning")
        return redirect(url_for("login"))

    if theme not in ["light", "dark"]:
        flash("Невірна тема", "danger")
        return redirect(url_for("get_profile"))

    resp = redirect(url_for("get_profile"))
    resp.set_cookie("theme", theme, max_age=30*24*60*60)  # зберігаємо на 30 днів
    flash(f"Вибрано {theme} тему", "success")
    return resp

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
