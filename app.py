from flask import Flask, jsonify, request, abort, render_template, Response


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates")

    # Simple in-memory stores (replaceable by a DB later)
    app.config.setdefault("WORKOUTS", [])
    app.config.setdefault("MEMBERS", [])


    @app.route("/favicon.ico")
    def favicon():
        # return a tiny SVG favicon to avoid 404 in the logs
        svg = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="100%" height="100%" fill="#0d6efd"/>'
            '<text x="50%" y="50%" font-size="32" fill="white" dy=".35em" text-anchor="middle">A</text>'
            '</svg>'
        )
        return Response(svg, mimetype='image/svg+xml')


    @app.route("/", methods=["GET"])
    def index():
        # Log headers for debugging why clients may prefer JSON
        app.logger.info('Index request Accept: %s', request.headers.get('Accept'))
        app.logger.info('Index request User-Agent: %s', request.headers.get('User-Agent'))

        # Force UI when query param ui=1 is present (handy for debugging or users behind proxies)
        if request.args.get('ui') == '1':
            app.logger.info('Forcing UI because ui=1')
            return render_template("index.html")

        # Use quality values to prefer text/html when equal or higher than application/json.
        q_html = request.accept_mimetypes['text/html'] if 'text/html' in request.accept_mimetypes else 0
        q_json = request.accept_mimetypes['application/json'] if 'application/json' in request.accept_mimetypes else 0
        app.logger.info('q_html=%s q_json=%s', q_html, q_json)

        if q_html >= q_json:
            return render_template("index.html")
        # otherwise fall back to machine-readable JSON
        return jsonify({"service": "ACEest Fitness & Gym API", "status": "ok"}), 200


    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy"}), 200


    @app.route("/workouts", methods=["GET", "POST"])
    def workouts():
        if request.method == "GET":
            return jsonify(app.config["WORKOUTS"]), 200

        # POST
        payload = request.get_json() or {}
        name = payload.get("name")
        duration = payload.get("duration_minutes")

        if not name or not isinstance(name, str):
            return jsonify({"error": "name is required and must be a string"}), 400
        if duration is None or not isinstance(duration, (int, float)) or duration <= 0:
            return jsonify({"error": "duration_minutes must be a positive number"}), 400

        workout = {"id": len(app.config["WORKOUTS"]) + 1, "name": name, "duration_minutes": duration}
        app.config["WORKOUTS"].append(workout)
        return jsonify(workout), 201


    @app.route("/members", methods=["GET", "POST"])
    def members():
        if request.method == "GET":
            return jsonify(app.config["MEMBERS"]), 200

        payload = request.get_json() or {}
        name = payload.get("name")
        email = payload.get("email")

        if not name or not isinstance(name, str):
            return jsonify({"error": "name is required and must be a string"}), 400
        if not email or not isinstance(email, str) or "@" not in email:
            return jsonify({"error": "a valid email is required"}), 400

        member = {"id": len(app.config["MEMBERS"]) + 1, "name": name, "email": email}
        app.config["MEMBERS"].append(member)
        return jsonify(member), 201


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
