"""
seed.py — Populates the database with sample data for testing.
"""

from db import db
from models import User, Robot, Ticket, TicketUpdate
from helpers import generate_ticket_ref


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------


# Three admins (Gandalf, Aragorn, Arwen) and seven regular users
USERS = [
    {"name": "Frodo Baggins", "email": "frodo@portal.com", "role": "regular"},
    {"name": "Samwise Gamgee", "email": "sam@portal.com", "role": "regular"},
    {"name": "Gandalf Grey", "email": "gandalf@portal.com", "role": "admin"},
    {"name": "Aragorn Elessar", "email": "aragorn@portal.com", "role": "admin"},
    {"name": "Legolas Greenleaf", "email": "legolas@portal.com", "role": "regular"},
    {"name": "Gimli Son of Gloin", "email": "gimli@portal.com", "role": "regular"},
    {"name": "Boromir Gondor", "email": "boromir@portal.com", "role": "regular"},
    {"name": "Meriadoc Brandybuck", "email": "merry@portal.com", "role": "regular"},
    {"name": "Peregrin Took", "email": "pippin@portal.com", "role": "regular"},
    {"name": "Arwen Undomiel", "email": "arwen@portal.com", "role": "admin"},
]

# All seed accounts share the same default password for ease of testing
DEFAULT_PASSWORD = "password123"


# Mix of UiPath and Power Automate platforms, some marked inactive
ROBOTS = [
    {"name": "Rivendell", "platform": "UiPath", "is_active": True},
    {"name": "Mordor", "platform": "Power Automate", "is_active": True},
    {"name": "Rohan", "platform": "UiPath", "is_active": True},
    {"name": "Gondor", "platform": "Power Automate", "is_active": True},
    {"name": "Lothlórien", "platform": "UiPath", "is_active": True},
    {"name": "The Shire", "platform": "Power Automate", "is_active": False},
    {"name": "Mirkwood", "platform": "UiPath", "is_active": True},
    {"name": "Isengard", "platform": "Power Automate", "is_active": False},
    {"name": "Minas Tirith", "platform": "UiPath", "is_active": True},
    {"name": "Helm's Deep", "platform": "Power Automate", "is_active": True},
]


TICKETS = [
    {
        "created_by": "frodo@portal.com",
        "assigned_to": "gandalf@portal.com",
        "robot": "Rivendell",
        "category": "StatusCheck",
        "subject": "Is Rivendell robot currently running?",
        "description": "Need to confirm whether the Rivendell automation is active and processing today.",
        "status": "New",
    },
    {
        "created_by": "sam@portal.com",
        "assigned_to": "aragorn@portal.com",
        "robot": "Mordor",
        "category": "Incident",
        "subject": "Mordor robot has stopped processing cases",
        "description": "The Mordor Power Automate robot failed at 08:30 and has not restarted. No cases processed since.",
        "status": "In Progress",
    },
    {
        "created_by": "legolas@portal.com",
        "assigned_to": None,
        "robot": "Rohan",
        "category": "StatsRequest",
        "subject": "How many cases did Rohan process this week?",
        "description": "Please provide a breakdown of cases processed by the Rohan robot from Monday to Friday this week.",
        "status": "New",
    },
    {
        "created_by": "gimli@portal.com",
        "assigned_to": "arwen@portal.com",
        "robot": "Gondor",
        "category": "ChangeRequest",
        "subject": "Update Gondor robot input folder path",
        "description": "The shared drive path for Gondor's input files has changed. Please update the robot configuration.",
        "status": "Waiting on Requestor",
    },
    {
        "created_by": "boromir@portal.com",
        "assigned_to": "gandalf@portal.com",
        "robot": "Lothlórien",
        "category": "Incident",
        "subject": "Lothlórien robot throwing login exception",
        "description": "Robot fails at login step with a credential exception. Suspected password expiry on the service account.",
        "status": "In Progress",
    },
    {
        "created_by": "merry@portal.com",
        "assigned_to": None,
        "robot": "Mirkwood",
        "category": "StatusCheck",
        "subject": "Confirm Mirkwood last successful run time",
        "description": "Can someone check Orchestrator and confirm the last successful run time for the Mirkwood robot?",
        "status": "Resolved",
    },
    {
        "created_by": "pippin@portal.com",
        "assigned_to": "aragorn@portal.com",
        "robot": "Minas Tirith",
        "category": "StatsRequest",
        "subject": "Monthly stats for Minas Tirith robot",
        "description": "Please provide total cases processed, exceptions, and average handle time for Minas Tirith for last month.",
        "status": "New",
    },
    {
        "created_by": "frodo@portal.com",
        "assigned_to": "arwen@portal.com",
        "robot": "Helm's Deep",
        "category": "ChangeRequest",
        "subject": "Add new exception handling step to Helm's Deep",
        "description": "Business has requested an additional validation step be added when the robot encounters a duplicate record.",
        "status": "In Progress",
    },
    {
        "created_by": "legolas@portal.com",
        "assigned_to": "gandalf@portal.com",
        "robot": "Rivendell",
        "category": "Other",
        "subject": "Rivendell robot schedule change request",
        "description": "Can the Rivendell robot run time be moved from 07:00 to 06:00 to align with the new shift pattern?",
        "status": "Closed",
    },
    {
        "created_by": "sam@portal.com",
        "assigned_to": None,
        "robot": "Gondor",
        "category": "Incident",
        "subject": "Gondor robot produced incorrect output file",
        "description": "Output file from yesterday's Gondor run contains duplicate rows. Needs investigation before reprocessing.",
        "status": "Waiting on Requestor",
    },
]


UPDATES = [
    {"ticket_ref_index": 0, "updated_by": "gandalf@portal.com", "note": "Checked Orchestrator — Rivendell is running and last completed at 07:45 this morning."},
    {"ticket_ref_index": 1, "updated_by": "aragorn@portal.com", "note": "Investigated failure. Root cause is a locked queue item. Clearing and restarting now."},
    {"ticket_ref_index": 1, "updated_by": "aragorn@portal.com", "note": "Robot restarted successfully. Monitoring for the next 30 minutes."},
    {"ticket_ref_index": 2, "updated_by": "arwen@portal.com",   "note": "Stats pulled from Orchestrator. Preparing summary report to send to requestor."},
    {"ticket_ref_index": 3, "updated_by": "arwen@portal.com",   "note": "Waiting on confirmation of the new folder path from the business team before updating config."},
    {"ticket_ref_index": 4, "updated_by": "gandalf@portal.com", "note": "Confirmed service account password expired. Raised with IT to reset. Robot paused in the meantime."},
    {"ticket_ref_index": 5, "updated_by": "gandalf@portal.com", "note": "Last successful run confirmed as 09:12 yesterday. 312 items processed. Ticket resolved."},
    {"ticket_ref_index": 6, "updated_by": "aragorn@portal.com", "note": "Requested stats from reporting team. Will update once received."},
    {"ticket_ref_index": 7, "updated_by": "arwen@portal.com",   "note": "Change request logged with the development team. Estimated delivery next sprint."},
    {"ticket_ref_index": 8, "updated_by": "gandalf@portal.com", "note": "Schedule updated in Orchestrator. Confirmed running at 06:00 from Monday. Ticket closed."},
]


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------

def seed():
    """Populate the database with sample users, robots, tickets, and updates."""

    print("Seeding database...")

    # --- Users ---
    print("Seeding users...")
    user_map = {}
    for u in USERS:
        user = User(name=u["name"], email=u["email"], role=u["role"])
        user.set_password(DEFAULT_PASSWORD)
        db.session.add(user)
        db.session.flush()
        user_map[u["email"]] = user
    db.session.commit()
    print(f"  {len(user_map)} users created.")

    # --- Robots ---
    print("Seeding robots...")
    robot_map = {}
    for r in ROBOTS:
        robot = Robot(name=r["name"], platform=r["platform"], is_active=r["is_active"])
        db.session.add(robot)
        db.session.flush()
        robot_map[r["name"]] = robot
    db.session.commit()
    print(f"  {len(robot_map)} robots created.")

    # --- Tickets ---
    print("Seeding tickets...")
    ticket_list = []
    for t in TICKETS:
        created_by = user_map[t["created_by"]]
        assigned_to = user_map[t["assigned_to"]] if t["assigned_to"] else None
        robot = robot_map[t["robot"]]

        ticket = Ticket(
            ticket_ref=generate_ticket_ref(),
            robot_id=robot.id,
            created_by_user_id=created_by.id,
            assigned_to_user_id=assigned_to.id if assigned_to else None,
            category=t["category"],
            subject=t["subject"],
            description=t["description"],
            status=t["status"],
        )
        db.session.add(ticket)
        db.session.flush()

        # Add an initial audit entry when each ticket is created
        db.session.add(TicketUpdate(
            ticket_id=ticket.id,
            updated_by_user_id=created_by.id,
            note="Ticket created."
        ))

        ticket_list.append(ticket)

    db.session.commit()
    print(f"  {len(ticket_list)} tickets created.")

    # --- Ticket Updates ---
    print("Seeding ticket updates...")
    for u in UPDATES:
        ticket = ticket_list[u["ticket_ref_index"]]
        updated_by = user_map[u["updated_by"]]
        db.session.add(TicketUpdate(
            ticket_id=ticket.id,
            updated_by_user_id=updated_by.id,
            note=u["note"]
        ))
    db.session.commit()
    print(f"  {len(UPDATES)} updates created.")

    print("\nSeed complete.")
    print(f"  All accounts use password: {DEFAULT_PASSWORD}")
    print("  Admin accounts: gandalf@portal.com, aragorn@portal.com, arwen@portal.com")
    print("  Regular accounts: frodo@portal.com, sam@portal.com, legolas@portal.com ...")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():
        seed()
