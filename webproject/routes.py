from flask import render_template, request, redirect, session
from models import db, User


def init_routes(app):
    @app.route("/")
    def main():
        user = session.get("user")
        return render_template("main.html", user=user)

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/register", methods=["POST"])
    def register():
        login = request.form.get("login")

        if User.query.filter_by(login=login).first():
            return redirect("/register")

        user = User(
            name=request.form.get("name"),
            surname=request.form.get("surname"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            login=login,
            password=request.form.get("password")
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    @app.route("/login", methods=["POST"])
    def login():
        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(login=login, password=password).first()

        if user:
            session["user"] = user.name
            return redirect("/")
        else:
            return redirect("/login?error=1")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect("/")

    @app.route("/affiche")
    def affiche():
        event_id = request.args.get("id", 1)

        events = {
            1: {
                "title": "Бизнес форум",
                "type": "Конференция",
                "desc": "Обсуждение экономики и технологий",
                "image": "Rectangle 40.jpg",
                "lat": 55.751244,
                "lon": 37.618423
            }
        }

        event = events.get(int(event_id), events[1])

        with open("templates/affiche.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        event_script = f"""
        <script>
        document.getElementById("title").innerText = "{event['title']}";
        document.getElementById("type").innerText = "{event['type']}";
        document.getElementById("desc").innerText = "{event['desc']}";
        document.getElementById("img").src = "/static/img/{event['image']}";
        document.getElementById("map").src = "https://yandex.ru/map-widget/v1/?ll={event['lon']},{event['lat']}&z=14&pt={event['lon']},{event['lat']},pm2rdm";
        </script>
        """

        html_content = html_content.replace("</body>", event_script + "</body>")

        return html_content
