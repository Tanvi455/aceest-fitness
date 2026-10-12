from flask import Flask, jsonify, request

DEFAULT_CLASSES = [
    {
        "id": 1,
        "name": "Strength & Conditioning",
        "instructor": "Alex Morgan",
        "capacity": 12,
        "enrolled": 0,
        "schedule": "Monday 18:00",
    },
    {
        "id": 2,
        "name": "Morning Yoga",
        "instructor": "Jamie Lee",
        "capacity": 16,
        "enrolled": 0,
        "schedule": "Wednesday 07:00",
    },
]


def create_app(initial_classes=None):
    app = Flask(__name__)
    classes = [dict(fitness_class) for fitness_class in (
        DEFAULT_CLASSES if initial_classes is None else initial_classes
    )]
    next_id = max((fitness_class["id"] for fitness_class in classes), default=0) + 1

    @app.get("/")
    def index():
        return jsonify(
            {
                "name": "ACEest Fitness & Gym API",
                "status": "online",
                "endpoints": ["/health", "/classes", "/classes/<id>"],
            }
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/classes", methods=["GET", "POST"])
    def class_collection():
        nonlocal next_id

        if request.method == "GET":
            return jsonify({"classes": classes})

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "A JSON object is required."}), 400

        name = payload.get("name")
        instructor = payload.get("instructor")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "A non-empty name is required."}), 400
        if not isinstance(instructor, str) or not instructor.strip():
            return jsonify({"error": "A non-empty instructor is required."}), 400

        capacity = payload.get("capacity", 12)
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            return jsonify({"error": "Capacity must be a positive integer."}), 400

        fitness_class = {
            "id": next_id,
            "name": name.strip(),
            "instructor": instructor.strip(),
            "capacity": capacity,
            "enrolled": 0,
            "schedule": payload.get("schedule", "To be announced"),
        }
        classes.append(fitness_class)
        next_id += 1
        return jsonify(fitness_class), 201

    @app.get("/classes/<int:class_id>")
    def class_detail(class_id):
        fitness_class = next(
            (item for item in classes if item["id"] == class_id), None
        )
        if fitness_class is None:
            return jsonify({"error": "Class not found."}), 404
        return jsonify(fitness_class)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
