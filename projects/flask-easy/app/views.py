from datetime import datetime, date
from flask import Blueprint, jsonify, request
from app import db
from app.models import Event

event_blueprint = Blueprint("events", __name__, url_prefix="/events")


def event_to_json(event: Event) -> dict:
    return {
        "id": event.id,
        "name": event.name,
        "date": event.date.strftime("%d-%m-%Y") if isinstance(event.date, date) else event.date,
        "venue": event.venue,
        "available_tickets": event.available_tickets,
        "price": event.price,
    }


@event_blueprint.route("", methods=["GET", "POST"])
def events():
    # Create new event
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request body"}), 400
        required = ["name", "date", "venue", "available_tickets", "price"]
        if not all(k in data for k in required):
            return jsonify({"error": "Invalid request body"}), 400
        try:
            event_date = datetime.strptime(data["date"], "%d-%m-%Y").date()
        except Exception:
            return jsonify({"error": "Invalid date format. Use dd-mm-yyyy"}), 400

        try:
            event = Event(
                name=data["name"],
                date=event_date,
                venue=data["venue"],
                available_tickets=int(data["available_tickets"]),
                price=float(data["price"]),
            )
        except Exception:
            return jsonify({"error": "Invalid request body"}), 400

        db.session.add(event)
        db.session.commit()
        return jsonify(event_to_json(event)), 201

    # GET -> list events ordered by date
    events = Event.query.order_by(Event.date).all()
    return jsonify([event_to_json(e) for e in events]), 200


@event_blueprint.route("/<int:event_id>", methods=["GET", "DELETE"])
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if request.method == "GET":
        return jsonify(event_to_json(event)), 200
    # DELETE
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200


@event_blueprint.route("/purchase", methods=["POST"])
def purchase_tickets():
    data = request.get_json()
    if not data or "event_id" not in data or "quantity" not in data:
        return jsonify({"error": "Invalid request body"}), 400
    event = db.session.get(Event, data["event_id"])
    if not event:
        return jsonify({"error": "Event not found"}), 404
    try:
        qty = int(data["quantity"])
    except Exception:
        return jsonify({"error": "Invalid request body"}), 400
    if qty > event.available_tickets:
        return jsonify({"error": "Not enough tickets available"}), 400
    event.available_tickets -= qty
    db.session.commit()
    return (
        jsonify({"message": "Purchase successful", "available_tickets": event.available_tickets}),
        201,
    )


@event_blueprint.route("/upcoming", methods=["GET"])
def upcoming_events():
    start = request.args.get("startDate")
    end = request.args.get("endDate")

    # Default start to today if not provided
    if not start:
        start_date = datetime.utcnow().date()
    else:
        try:
            start_date = datetime.strptime(start, "%d-%m-%Y").date()
        except Exception:
            return jsonify({"error": "Invalid date format. Use dd-mm-yyyy"}), 400

    if end:
        try:
            end_date = datetime.strptime(end, "%d-%m-%Y").date()
        except Exception:
            return jsonify({"error": "Invalid date format. Use dd-mm-yyyy"}), 400
        if start_date > end_date:
            return jsonify({"error": "Start date cannot be after end date"}), 400
    else:
        end_date = None

    query = Event.query.filter(Event.date >= start_date)
    if end_date:
        query = query.filter(Event.date <= end_date)
    events = query.order_by(Event.date).all()
    return jsonify([event_to_json(e) for e in events]), 200
