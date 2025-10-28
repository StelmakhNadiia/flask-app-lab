from flask import Blueprint, request, redirect, url_for, render_template, session, flash, make_response

# Створення blueprint
users_bp = Blueprint("users", __name__, template_folder="templates/users")


users = {
    "Nadiia": "123456",
    "admin": "adminpass"
}

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("login")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Невірне ім'я користувача або пароль", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html")


@users_bp.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if "username" not in session:
        flash("Будь ласка, увійдіть у систему", "warning")
        return redirect(url_for("users.login"))

    username_value = session["username"]
    theme_cookie = request.cookies.get("theme", "light")  # світла тема за замовчуванням
    response = make_response(render_template("profile.html", username=username_value, cookies=request.cookies, theme=theme_cookie))
    return response


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли з системи", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if "username" not in session:
        flash("Будь ласка, увійдіть у систему", "warning")
        return redirect(url_for("users.login"))

    if theme not in ["light", "dark"]:
        flash("Невірна тема", "danger")
        return redirect(url_for("users.get_profile"))

    # Зберігаємо вибрану тему в cookies
    response = make_response(redirect(url_for("users.get_profile")))
    response.set_cookie("theme", theme, max_age=60*60*24*30)  # 30 днів
    flash(f"Тему змінено на {theme}", "success")
    return response

