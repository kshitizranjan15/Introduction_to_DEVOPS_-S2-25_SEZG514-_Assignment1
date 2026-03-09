from flask import Flask, jsonify, request, render_template, Response

# ---------------------------------------------------------------------------
# ACEest Fitness & Gym — Program data derived from all 10 version files
# (Aceestver-1.0 through Aceestver2.0.1 / Aceestver-3.2.4)
# ---------------------------------------------------------------------------

PROGRAMS = {
    "Fat Loss (FL)": {
        "code": "FL",
        "calorie_factor": 22,
        "color": "#e74c3c",
        "workout": (
            "Mon: Back Squat 5×5 + AMRAP Core\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: 10RFT Deadlifts / Box Jumps\n"
            "Fri: Zone 2 Cardio 30min (Active Recovery)"
        ),
        "diet": (
            "Breakfast: 3 Egg Whites + Oats Idli\n"
            "Lunch: Grilled Chicken + Brown Rice\n"
            "Dinner: Fish Curry + Millet Roti\n"
            "Target: ~2,000 kcal/day"
        ),
        "exercises": ["Back Squat", "Assault Bike", "Bench Press", "Deadlift", "Box Jumps"],
    },
    "Muscle Gain (MG)": {
        "code": "MG",
        "calorie_factor": 35,
        "color": "#2ecc71",
        "workout": (
            "Mon: Squat 5×5\n"
            "Tue: Bench Press 5×5\n"
            "Wed: Deadlift 4×6\n"
            "Thu: Front Squat 4×8\n"
            "Fri: Incline Press 4×10\n"
            "Sat: Barbell Rows 4×10"
        ),
        "diet": (
            "Breakfast: 4 Eggs + Peanut Butter Oats\n"
            "Lunch: Chicken Biryani (250g Chicken)\n"
            "Dinner: Mutton Curry + Jeera Rice\n"
            "Target: ~3,200 kcal/day"
        ),
        "exercises": ["Back Squat", "Bench Press", "Deadlift", "Front Squat", "Incline Press", "Barbell Row"],
    },
    "Beginner (BG)": {
        "code": "BG",
        "calorie_factor": 26,
        "color": "#3498db",
        "workout": (
            "Full Body Circuit (3×/week):\n"
            "- Air Squats\n"
            "- Ring Rows\n"
            "- Push-ups\n"
            "Focus: Technique Mastery & Consistency (90% threshold)"
        ),
        "diet": (
            "Balanced Tamil Meals:\n"
            "Idli / Dosa / Rice + Dal / Chapati\n"
            "Protein Target: 120g/day"
        ),
        "exercises": ["Air Squats", "Ring Rows", "Push-ups", "Plank", "Dumbbell Row"],
    },
}

GYM_METRICS = {
    "capacity": 150,
    "area_sqft": 10000,
    "breakeven_members": 250,
}


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates")

    # In-memory stores (replaceable by a DB — see Version history)
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

        # If there's no Accept header (e.g., pytest default client), return JSON to match tests.
        if request.headers.get('Accept') is None:
            app.logger.info('No Accept header, returning JSON')
            return jsonify({"service": "ACEest Fitness & Gym API", "status": "ok"}), 200

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


    # ------------------------------------------------------------------
    # Programs endpoint — returns all ACEest program definitions
    # (sourced from Aceestver-1.0 → Aceestver-3.2.4 program data)
    # ------------------------------------------------------------------
    @app.route("/programs", methods=["GET"])
    def programs():
        return jsonify(PROGRAMS), 200


    @app.route("/programs/<program_code>", methods=["GET"])
    def program_detail(program_code):
        """Return a single program by its short code (FL, MG, BG)."""
        for name, data in PROGRAMS.items():
            if data["code"].upper() == program_code.upper():
                return jsonify({"program": name, **data}), 200
        return jsonify({"error": f"Program '{program_code}' not found. Valid codes: FL, MG, BG"}), 404


    # ------------------------------------------------------------------
    # Calorie calculator — derived from calorie_factor logic in all versions
    # ------------------------------------------------------------------
    @app.route("/calories", methods=["POST"])
    def calories():
        payload = request.get_json() or {}
        weight = payload.get("weight_kg")
        program_code = payload.get("program_code", "").upper()

        if weight is None or not isinstance(weight, (int, float)) or weight <= 0:
            return jsonify({"error": "weight_kg must be a positive number"}), 400

        matched = None
        for name, data in PROGRAMS.items():
            if data["code"].upper() == program_code:
                matched = (name, data)
                break

        if not matched:
            return jsonify({"error": f"program_code must be one of: {', '.join(d['code'] for d in PROGRAMS.values())}"}), 400

        program_name, program_data = matched
        estimated = round(weight * program_data["calorie_factor"])
        return jsonify({
            "weight_kg": weight,
            "program": program_name,
            "calorie_factor": program_data["calorie_factor"],
            "estimated_daily_kcal": estimated,
        }), 200


    # ------------------------------------------------------------------
    # Gym metrics endpoint — capacity / area / break-even
    # ------------------------------------------------------------------
    @app.route("/gym-info", methods=["GET"])
    def gym_info():
        return jsonify(GYM_METRICS), 200


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
