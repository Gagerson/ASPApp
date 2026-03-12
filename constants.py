"""
constants.py — Defines allowed values for ticket categories, statuses, and robot platforms.
"""

TICKET_CATEGORIES = {"StatusCheck", "StatsRequest", "Incident", "ChangeRequest", "Other"}
TICKET_STATUSES = {"New", "In Progress", "Waiting on Requestor", "Resolved", "Closed"}
ROBOT_PLATFORMS = {"UiPath", "Power Automate"}
