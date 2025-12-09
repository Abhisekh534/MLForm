import requests
import random
import time
from datetime import datetime

# -------------------- SEED --------------------
random.seed(time.time() + random.randint(0, 1000))

# -------------------- CONFIG --------------------
url = "https://docs.google.com/forms/d/e/1FAIpQLSfeLPNWwoaPjqLIImZ-te6dP8b4zOlslGrJsd4bicmw49klkQ/formResponse"

def weighted_choice(options, weights):
    return random.choices(options, weights=weights)[0]

# -------------------- HUMAN-LIKE RESPONSE --------------------
outlier = random.random() < 0.04  # 4% chance for unusual behavior

sleep_hours = random.randint(0,12) if outlier else weighted_choice([1,2,3,4,5,6,7,8], [5,10,15,20,25,15,7,3])
sleep_hours += random.choice([-1,0,1])
sleep_hours = max(0, min(12, sleep_hours))

if sleep_hours <= 2:
    sleep_quality = 5 if outlier else random.randint(1,3)
elif sleep_hours <= 4:
    sleep_quality = random.randint(2,4)
elif sleep_hours <= 6:
    sleep_quality = random.randint(3,5)
else:
    sleep_quality = random.randint(4,5)

screen_hours = random.randint(0,10) if outlier else weighted_choice([1,2,3,4,5,6], [10,15,25,20,20,10])
screen_hours += random.choice([-1,0,1])
screen_hours = max(0, min(10, screen_hours))

if outlier:
    productive_hours = random.randint(1,5)
else:
    if screen_hours <= 2:
        productive_hours = random.randint(3,5)
    elif screen_hours <= 4:
        productive_hours = random.randint(2,4)
    else:
        productive_hours = random.randint(1,3)

exercise = random.randint(1,5) if outlier else weighted_choice([1,2,3,4,5], [5,10,20,35,30])
study_hours = random.randint(0,10) if outlier else weighted_choice([1,2,3,4,5,6], [10,20,30,25,10,5])
study_hours += random.choice([-1,0,1])
study_hours = max(0, study_hours)

social_activity = weighted_choice(["Sometimes","Always","Never"], [45,35,20])
time_for_self = weighted_choice(["5-10 minutes","10-20 minutes","20-30 minutes"], [35,40,25])
schedule_change = weighted_choice(["No, Same schedule","Yes, Changed schedule"], [75,25])
stress_level = weighted_choice([1,2,3,4,5], [15,20,30,25,10])
meals = weighted_choice([1,2,3,4,5], [15,25,30,20,10])
relaxation_hours = weighted_choice([1,2,3,4,5], [20,25,30,15,10])
screen_quality = weighted_choice(["1-2 hours","3-4 hours","More than 4 hours"], [30,40,30])
days_unproductive = weighted_choice(["1-2 days","3-5 days","5+ days"], [35,40,25])

# -------------------- FORM DATA --------------------
data = {
    "entry.130782805": f"{study_hours} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
    "entry.1315476675": screen_hours,
    "entry.882704943": sleep_hours,
    "entry.1934504077": sleep_quality,
    "entry.206918368": weighted_choice(["8 PM - 10 PM","10 PM - 12 AM","12 AM - 2 AM"], [35,40,25]),
    "entry.744326918": weighted_choice(["Yes","No"], [65,35]),
    "entry.1784191715": social_activity,
    "entry.1192970950": weighted_choice(["Often","Sometimes","Rarely"], [50,35,15]),
    "entry.927479717": screen_quality,
    "entry.2035929357": days_unproductive,
    "entry.38757470": social_activity,
    "entry.1406815052": time_for_self,
    "entry.1403062670": schedule_change,
    "entry.881978082": exercise,
    "entry.1026336142": productive_hours,
    "entry.491147406": meals
}

# -------------------- SUBMIT --------------------
response = requests.post(url, data=data)
print(f"Form submitted! Status: {response.status_code} | Outlier: {outlier}")
