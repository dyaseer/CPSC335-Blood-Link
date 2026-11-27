"""theme.py - BloodLink: a regional blood supply network.
Turns the theme's data into the inputs that core.py expects."""
import json, os

THEME = "BloodLink"
TITLE = "BloodLink"
TAGLINE = "Regional blood-unit sharing planner"
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "units.json")

RECORD = "blood unit"
ID_FIELD = "barcode"
LOOKUP_FIELD, LOOKUP_LABEL = "barcode", "Unit barcode"
COLUMNS = ["barcode", "blood_type", "product", "cooler_slots", "patients_helped", "expires_in_hours", "hospital"]

SORT_LABEL = "Hours until expiry"
SEARCH_PROMPT = "Show units that expire in at least (hours)"
SEARCH_DEFAULT = "48"

HEAP_TITLE = "Shipping queue: unit closest to expiry first"
HEAP_RULE = "Priority = fewest hours until expiry, then O-negative (universal donor) first, then more patients helped."

PLAN_TITLE = "Pack one courier cooler"
CAPACITY_LABEL, CAPACITY_UNIT = "Cooler space", "slots"
CAPACITY_DEFAULT, CAPACITY_MIN, CAPACITY_MAX = 18, 4, 40
POOL_DEFAULT = 15
WEIGHT_LABEL, VALUE_LABEL = "Cooler slots", "Patients helped"

ROOT_LABEL = "Regional Blood Center"
ROAD_LABEL = "courier drive time (minutes)"
NETWORK_TITLE = "Courier link network"
MST_TEXT = "Cheapest set of courier links that connects every hospital to the blood center (cost in $ per day)."
BREAK_TEXT = "A courier link goes down. Which hospitals are cut off?"

TEXT_TITLE = "Recall label scanner"
TEXT_HELP = "Scan unit labels for recalled lot numbers so no recalled unit is shipped."

TOUR_TITLE = "One courier's delivery loop"
TOUR_TEXT = "Start at the blood center, visit every chosen hospital, return. Finding the shortest order is the Traveling Salesman Problem (NP-hard)."


def load(path=DATA_FILE):
    with open(path) as f:
        data = json.load(f)
    names = {n["id"]: n["name"] for n in data["nodes"]}
    for r in data["records"]:
        r["hospital"] = names[r["node"]]
    return data


def to_minutes(text):            # here the sort value is hours, so just an int
    return int(text)


def sort_value(rec):
    return rec["expires_in_hours"]


def priority(rec):
    return (rec["expires_in_hours"], 0 if rec["blood_type"] == "O-" else 1, -rec["patients_helped"])


def priority_reason(rec):
    return f"expires in {rec['expires_in_hours']} h, {rec['blood_type']} {rec['product'].lower()}"


def plan_items(records):
    return [{"id": r[ID_FIELD], "weight": r["cooler_slots"], "value": r["patients_helped"]} for r in records]


def describe(rec):
    return (f"{rec['barcode']} at {rec['hospital']}: {rec['blood_type']} {rec['product'].lower()}, "
            f"{rec['cooler_slots']} slot(s), helps {rec['patients_helped']} patient(s), expires in {rec['expires_in_hours']} h.")
