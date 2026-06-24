import os
import cv2
import numpy as np
import pickle
import dlib
from scipy.spatial import distance
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from collections import Counter

# Load the Haar cascade for face detection
face_cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Load ResNet50 model for feature extraction
resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Load dlib's face detector and landmark predictor for liveness detection
detector = dlib.get_frontal_face_detector()
predictor_path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Eye Aspect Ratio (EAR) calculation for blink detection
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Process video with liveness detection (only using eye blink)
def process_video():
    # Load the trained models
    with open('models/random_forest_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)

    with open('models/xgboost_model.pkl', 'rb') as f:
        xgb_model = pickle.load(f)

    with open('inverse_labels.pkl', 'rb') as file:
        inverse_labels = pickle.load(file)

    video = cv2.VideoCapture(0)  # 0 for default webcam

    frame_count = 0
    valid_detections = 0
    rf_predictions = []
    xgb_predictions = []
    blink_count = 0  # Track blinks

    try:
        while valid_detections < 50:
            ret, frame = video.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            if len(faces) > 0:
                valid_detections += 1  # Increment only if faces are detected

                for face in faces:
                    # Detect facial landmarks
                    landmarks = predictor(gray, face)
                    
                    # Extract eye coordinates
                    left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                    right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]

                    # Compute EAR (Eye Aspect Ratio)
                    left_EAR = eye_aspect_ratio(left_eye)
                    right_EAR = eye_aspect_ratio(right_eye)
                    avg_EAR = (left_EAR + right_EAR) / 2.0

                    # Blink Detection (Threshold)
                    if avg_EAR < 0.23:  # Threshold for eye closing
                        blink_count += 1

                    # Extract and preprocess the face
                    (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())

                    # Ensure face coordinates are within bounds
                    img_h, img_w, _ = frame.shape
                    x = max(0, x)
                    y = max(0, y)
                    w = min(w, img_w - x)
                    h = min(h, img_h - y)

                    if w > 0 and h > 0:  # Ensure valid crop size
                        face_crop = frame[y:y+h, x:x+w]
                        
                        if face_crop.size > 0:  # Ensure face_crop is not empty
                            face_resized = cv2.resize(face_crop, (224, 224))
                            face_array = image.img_to_array(face_resized)
                            face_array = np.expand_dims(face_array, axis=0)
                            face_array = preprocess_input(face_array)

                            # Feature extraction using ResNet50
                            features = resnet_model.predict(face_array).flatten()

                            # Predict using models
                            rf_prediction = rf_model.predict([features])[0]
                            xgb_prediction = xgb_model.predict([features])[0]

                            rf_predictions.append(rf_prediction)
                            xgb_predictions.append(xgb_prediction)

                            # Display predictions on the frame
                            label = f"RF: {inverse_labels[rf_prediction]} | XGB: {inverse_labels[xgb_prediction]}"
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Display the video feed
            cv2.imshow("Real-Time Face Recognition & Liveness Detection (Blink Only)", frame)
            frame_count += 1

            # If 50 detections are made, stop the loop
            if valid_detections >= 50:
                break

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        video.release()
        cv2.destroyAllWindows()

    # Get most common predictions
    if valid_detections >= 50:
        rf_most_common = Counter(rf_predictions).most_common(1)[0][0]
        xgb_most_common = Counter(xgb_predictions).most_common(1)[0][0]
        final_prediction = inverse_labels.get(rf_most_common)

        # **Liveness determination (Only using blinks)**
        is_live = blink_count >= 2  # At least 2 blinks to be considered live
        liveness_status = "Live User" if is_live else "Fake Input (Photo or Video)"

        print(f"Final Prediction: {final_prediction} | Liveness: {liveness_status}")
        return final_prediction, liveness_status
    else:
        print("Not enough valid detections.")
        return None, "No Detection"

process_video()
