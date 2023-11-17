import secrets, csv
from datetime import datetime

secret = secrets.token_urlsafe(16)

try:
    with open("keys.csv", "x", newline="") as file:
        writer = csv.writer(file)
        field = ["api_key", "datetime_created"]

        writer.writerow(field)
        writer.writerow([secret, datetime.now()])
except FileExistsError:
    with open("keys.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([secret, datetime.now()])
