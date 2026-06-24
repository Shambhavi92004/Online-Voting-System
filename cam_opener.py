import os
import cv2
import numpy as np
import pickle
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, Response, jsonify
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from collections import Counter
import time
import os
import sys


#from cam_opener import process_video


# Load the Haar cascade for face detection
face_cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Load ResNet50 model for feature extraction
resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')



#print("Dictionary loaded successfully:")
#print(loaded_inverse_labels)





def process_video():
# Load the trained models
    rf_model_path = 'models/random_forest_model.pkl'
    xgb_model_path = 'models/xgboost_model.pkl'

    with open(rf_model_path, 'rb') as f:
        rf_model = pickle.load(f)

    with open(xgb_model_path, 'rb') as f:
        xgb_model = pickle.load(f)
# Mapping from label index to class name (use the same as during training)
    with open('inverse_labels.pkl', 'rb') as file:
        loaded_inverse_labels = pickle.load(file)
    inverse_labels = loaded_inverse_labels
    # Initialize video capture
    # Reset and open the camera
    #camera_index = 1  # Use 0 for default webcam, 1 for secondary camera
    #video = reset_camera(camera_index)
   # try: 

    #    video = reset_camera(camera_index)
    #except:

    video = cv2.VideoCapture(0)# 0 for default webcam (1 for secondary camera if available)




    

    frame_count = 0
    rf_predictions = []
    xgb_predictions = []
    valid_detections = 0  # To track how many frames with face detection we have

    try:
        while valid_detections < 50:
            ret, frame = video.read()
            if not ret:
                print("Failed to capture video")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) > 0:  # Only process frames where faces are detected
                valid_detections += 1  # Increment only if faces are detected
                for (x, y, w, h) in faces:
                    # Crop and preprocess the face
                    face = frame[y:y+h, x:x+w]
                    face_resized = cv2.resize(face, (224, 224))
                    face_array = image.img_to_array(face_resized)
                    face_array = np.expand_dims(face_array, axis=0)
                    face_array = preprocess_input(face_array)

                    # Extract features using ResNet50
                    features = resnet_model.predict(face_array).flatten()

                    # Predict using Random Forest
                    rf_prediction = rf_model.predict([features])[0]
                    rf_predictions.append(rf_prediction)

                    # Predict using XGBoost
                    xgb_prediction = xgb_model.predict([features])[0]
                    xgb_predictions.append(xgb_prediction)

                    # Display the predictions on the frame
                    label = f"RF: {inverse_labels[rf_prediction]} | XGB: {inverse_labels[xgb_prediction]}"
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Display the video feed
            cv2.imshow("Real-Time Face Recognition", frame)
            frame_count += 1

            # If 50 detections are made, stop the loop
            if valid_detections >= 50:
                break

            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Ensure the video capture is released and windows are closed properly

        #reset_camera()

        video.release()
        cv2.destroyAllWindows()
        #video = cv2.VideoCapture(1)

    # Only return the most common prediction if there are enough valid detections
    if valid_detections >= 50:
        rf_most_common = Counter(rf_predictions).most_common(1)[0][0]
        xgb_most_common = Counter(xgb_predictions).most_common(1)[0][0]
        print("Most frames detected:", inverse_labels.get(rf_most_common), inverse_labels.get(xgb_most_common))
        return inverse_labels.get(rf_most_common)
    else:
        print("Not enough valid detections.")
        return None, None
