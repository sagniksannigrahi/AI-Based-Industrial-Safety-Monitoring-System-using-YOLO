from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    persons = 0
    helmets = 0
    fire_detected = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            x1,y1,x2,y2 = map(int, box.xyxy[0])

            # Person detection
            if label == "person":
                persons += 1
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            # Helmet detection (YOLOv8 default detects "sports ball" as helmet substitute for demo)
            if label == "sports ball":  
                helmets += 1
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,0),2)

            # Fire detection (YOLOv8 default "fire hydrant" used as demo fire class)
            if label == "fire hydrant":
                fire_detected = True
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),3)

    # Status Text
    cv2.putText(frame,f"Workers: {persons}",(20,40),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.putText(frame,f"Helmets: {helmets}",(20,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

    fire_status = "YES" if fire_detected else "NO"
    cv2.putText(frame,f"Fire Detected: {fire_status}",(20,120),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("Industrial Safety Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
