"""
app.py — Defines the Flask application, configuration, and all route handlers.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import db
from models import User, Robot, Ticket, TicketUpdate
from helpers import generate_ticket_ref, login_required, admin_required
from validation import validate_robot, validate_ticket, ValidationError, validate_registration, validate_login

app = Flask(__name__, template_folder="templates")

# Database config — SQLite file stored locally as data.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key-change-later"

db.init_app(app)

# Create tables and auto-seed if db empty
with app.app_context():
    db.create_all()
    from models import User
    if User.query.count() == 0:
        from seed import seed
        seed()

# ---------------------------------------------------------------------------
# General routes
# ---------------------------------------------------------------------------


@app.route("/")
def home():
    return redirect(url_for("login"))  # Redirect to the login page


# ---------------------------------------------------------------------------
# Authentication routes
# ---------------------------------------------------------------------------


@app.route("/register", methods=["GET", "POST"])  # New user registration
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            role = request.form.get("role", "regular").strip()

            validate_registration(name, email, password, role)

            existing = User.query.filter_by(email=email).first()  # No duplicate emails
            if existing:
                raise ValidationError("An account with this email already exists.")

            user = User(name=name, email=email, role=role)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        except ValidationError as e:
            flash(str(e), "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])  # Validate credentials and store user info in session
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            validate_login(email, password)

            user = User.query.filter_by(email=email).first()

            if user is None or not user.check_password(password):
                raise ValidationError("Invalid email or password.")

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role

            flash("Logged in successfully.", "success")
            return redirect(url_for("list_tickets"))

        except ValidationError as e:
            flash(str(e), "danger")
            return render_template("login.html"), 200

        except Exception as e:
            print("LOGIN ERROR:", e)
            flash("Unexpected error during login.", "danger")
            return render_template("login.html"), 200

    return render_template("login.html")


@app.route("/logout")  # Clear the session and redirect to the login page
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ---------------------------------------------------------------------------
# Ticket routes
# ---------------------------------------------------------------------------


@app.route("/tickets")  # Display all tickets
@login_required
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()
    return render_template("tickets.html", tickets=tickets)


@app.route("/tickets/add", methods=["GET", "POST"])  # Create new ticket
@login_required
def add_ticket():
    users = User.query.order_by(User.name.asc()).all()
    robots = Robot.query.order_by(Robot.name.asc()).all()

    if request.method == "POST":
        try:
            created_by = db.session.get(User, session["user_id"])
            if not created_by:
                raise ValidationError("Logged-in user not found.")

            robot_id_raw = request.form.get("robot_id", "").strip()
            if not robot_id_raw:
                raise ValidationError("Robot is required.")
            robot_id = int(robot_id_raw)

            assigned_to_id_raw = request.form.get("assigned_to_id", "").strip()
            assigned_to_id = int(assigned_to_id_raw) if assigned_to_id_raw else None

            category = request.form.get("category", "").strip()
            subject = request.form.get("subject", "").strip()
            description = request.form.get("description", "").strip()
            status = request.form.get("status", "New").strip()

            validate_ticket(category, subject, description, status)

            ticket = Ticket(
                ticket_ref=generate_ticket_ref(),
                robot_id=robot_id,
                created_by_user_id=created_by.id,
                assigned_to_user_id=assigned_to_id,
                category=category,
                subject=subject,
                description=description,
                status=status
            )
            db.session.add(ticket)
            db.session.flush()

            db.session.add(
                TicketUpdate(
                    ticket_id=ticket.id,
                    updated_by_user_id=created_by.id,
                    note="Ticket created."
                )
            )
            db.session.commit()

            flash("Ticket created successfully.", "success")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        except ValidationError as e:
            flash(str(e), "danger")

    return render_template("add_ticket.html", users=users, robots=robots)


@app.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])  # Display a ticket and its update history
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":
        try:
            note = request.form.get("note", "").strip()

            if not note:
                raise ValidationError("Update note cannot be empty.")

            current_user = db.session.get(User, session["user_id"])
            if not current_user:
                raise ValidationError("Logged in user not found.")

            update = TicketUpdate(
                ticket_id=ticket.id,
                updated_by_user_id=current_user.id,
                note=note
            )

            db.session.add(update)
            db.session.commit()

            flash("Update added.", "success")

            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        except ValidationError as e:
            flash(str(e), "danger")

    updates = (
        TicketUpdate.query
        .filter_by(ticket_id=ticket.id)
        .order_by(TicketUpdate.created_at.desc())
        .all()
    )

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        updates=updates
    )


@app.route("/tickets/<int:ticket_id>/edit", methods=["GET", "POST"])  # Edit ticket
@login_required
def edit_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    users = User.query.order_by(User.name.asc()).all()
    robots = Robot.query.order_by(Robot.name.asc()).all()

    if request.method == "POST":
        try:
            ticket.robot_id = int(request.form.get("robot_id"))
            assigned_to_id_raw = request.form.get("assigned_to_id", "").strip()
            ticket.assigned_to_user_id = int(assigned_to_id_raw) if assigned_to_id_raw else None

            category = request.form.get("category", "").strip()
            subject = request.form.get("subject", "").strip()
            description = request.form.get("description", "").strip()
            status = request.form.get("status", "").strip()

            validate_ticket(category, subject, description, status)

            ticket.category = category
            ticket.subject = subject
            ticket.description = description
            ticket.status = status

            db.session.add(TicketUpdate(ticket_id=ticket.id, updated_by_user_id=session["user_id"], note="Ticket edited."))
            db.session.commit()
            flash("Ticket updated successfully.", "success")
            return redirect(url_for("ticket_detail", ticket_id=ticket.id))

        except ValidationError as e:
            flash(str(e), "danger")
            return render_template("edit_ticket.html", ticket=ticket, users=users, robots=robots)

    return render_template("edit_ticket.html", ticket=ticket, users=users, robots=robots)


@app.post("/tickets/<int:ticket_id>/delete")  # Delete ticket (admin only)
@admin_required
def delete_ticket(ticket_id: int):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket deleted.", "success")
    return redirect(url_for("list_tickets"))

# ---------------------------------------------------------------------------
# Robot routes
# ---------------------------------------------------------------------------


@app.route("/robots/add", methods=["GET", "POST"])  # Add a new robot (admin only)
@admin_required
def add_robot():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            platform = request.form.get("platform", "").strip()
            is_active = request.form.get("is_active") == "on"

            validate_robot(name, platform)

            r = Robot(name=name, platform=platform, is_active=is_active)
            db.session.add(r)
            db.session.commit()
            flash("Robot added successfully.", "success")
            return redirect(url_for("list_tickets"))
        except ValidationError as e:
            flash(str(e), "danger")
            return render_template("add_robot.html")

    return render_template("add_robot.html")


# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
