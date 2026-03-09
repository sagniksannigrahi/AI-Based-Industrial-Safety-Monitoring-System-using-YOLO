from ultralytics import YOLO
import cv2
import sqlite3
from datetime import datetime
import smtplib
from email.message import EmailMessage
import requests
import os
import time
import logging

# =========================
# CONFIGURATION
# =========================

EMAIL_SENDER = "srmextrause@gmail.com"
EMAIL_PASSWORD = "qojo weld zuho vetr"   # 🔴 Put NEW app password (no spaces)
EMAIL_RECEIVER = "sagniksannigrahi@gmail.com"

VIOLATION_FOLDER = "violations"
LOG_FOLDER = "logs"

os.makedirs(VIOLATION_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# =========================
# LOGGING SETUP
# =========================

logging.basicConfig(
    filename=f"{LOG_FOLDER}/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# GPS LOCATION FUNCTION
# =========================

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()

        location = data.get("loc", "Unknown")
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")

        maps_link = f"https://www.google.com/maps?q={location}"

        return location, f"{city}, {region}, {country}", maps_link

    except Exception as e:
        logging.error(f"GPS Error: {e}")
        return "Unknown", "Unknown Location", "N/A"

# =========================
# EMAIL ALERT FUNCTION
# =========================

def send_email_alert(workers, helmets, image_path):

    try:
        location_coords, location_text, maps_link = get_location()

        msg = EmailMessage()
        msg["Subject"] = "⚠ Helmet Violation Detected!"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        msg.set_content("Helmet violation detected.")

        msg.add_alternative(f"""
        <html>
            <body>
                <h2 style="color:red;">⚠ Helmet Violation Detected</h2>
                <p><b>Workers:</b> {workers}</p>
                <p><b>Helmets:</b> {helmets}</p>
                <p><b>Location:</b> {location_text}</p>
                <p><b>GPS:</b> {location_coords}</p>
                <p><a href="{maps_link}">View on Google Maps</a></p>
                <hr>
                <p>AI-Based Industrial Safety Monitoring System</p>
            </body>
        </html>
        """, subtype="html")

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="image",
                    subtype="jpeg",
                    filename=os.path.basename(image_path)
                )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        logging.info("Email alert sent successfully.")
        print("✅ Email Sent")

    except Exception as e:
        logging.error(f"Email Error: {e}")
        print("❌ Email Error:", e)

# =========================
# DATABASE FUNCTION
# =========================

def save_log(workers, helmets, fire_status, violation):
    conn = sqlite3.connect("safety.db")
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO safety_logs(date, workers, helmets, fire_status, violation) VALUES (?,?,?,?,?)",
        (date, workers, helmets, fire_status, violation)
    )

    conn.commit()
    conn.close()

    logging.info("Log saved in database.")

# =========================
# YOLO + CAMERA SETUP
# =========================

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

last_email_time = 0

# =========================
# MAIN LOOP
# =========================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    workers = 0
    helmets = 0
    fire_detected = False
    violation = "SAFE"

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                workers += 1

            if label == "sports ball":   # replace with real helmet class if trained
                helmets += 1

            if label == "fire hydrant":
                fire_detected = True

    fire_status = "YES" if fire_detected else "NO"

    # =========================
    # HELMET VIOLATION
    # =========================

    if helmets < workers and workers > 0:

        violation = "HELMET VIOLATION"

        if time.time() - last_email_time > 20:

            face_saved_path = None

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]

                    if label == "person":
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        person_crop = frame[y1:y2, x1:x2]

                        gray = cv2.cvtColor(person_crop, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                        for (fx, fy, fw, fh) in faces:
                            face_img = person_crop[fy:fy+fh, fx:fx+fw]

                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            face_saved_path = f"{VIOLATION_FOLDER}/violation_{timestamp}.jpg"

                            cv2.imwrite(face_saved_path, face_img)
                            logging.info("Face captured and saved.")
                            break

                        break

            send_email_alert(workers, helmets, face_saved_path)
            save_log(workers, helmets, fire_status, violation)

            last_email_time = time.time()

    # =========================
    # FIRE DETECTION
    # =========================

    if fire_status == "YES":
        violation = "FIRE EMERGENCY"
        send_email_alert(workers, helmets, None)
        save_log(workers, helmets, fire_status, violation)

    # =========================
    # DISPLAY
    # =========================

    cv2.putText(frame, f"Workers: {workers}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"Helmets: {helmets}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    cv2.putText(frame, f"Fire: {fire_status}", (20,120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Industrial Safety Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()