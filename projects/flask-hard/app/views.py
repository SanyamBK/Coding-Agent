from flask import request, jsonify, Blueprint
from app.models import LogRecord
from pydantic import ValidationError
from app.log_processor import LogProcessor


# single shared processor for the app
processor = LogProcessor()

logs_blueprint = Blueprint("logs", __name__, url_prefix="/")


@logs_blueprint.route("/logs", methods=["POST"])
def add_log():
    try:
        # Validate and process the incoming LogRecord data
        log_record = LogRecord(**request.json)
    except ValidationError as e:
        # Return a 400 response with validation errors if data is invalid
        return jsonify({"error": "Invalid log data", "details": e.errors()}), 400

    # Process the validated log
    processor.process_log(log_record.model_dump())
    return jsonify({"status": "Log processed successfully"}), 201


@logs_blueprint.route("/logs", methods=["GET"])
def get_logs():
    level = request.args.get('level')
    logs = processor.get_logs(level=level)
    return jsonify(logs), 200


@logs_blueprint.route("/metrics", methods=["GET"])
def get_metrics():
    return jsonify(processor.metrics.get_all_metrics()), 200
