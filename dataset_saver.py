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
# Load the trained models
rf_model_path = 'models/random_forest_model.pkl'
xgb_model_path = 'models/xgboost_model.pkl'


#from cam_opener import process_video


# Load the Haar cascade for face detection
face_cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Load ResNet50 model for feature extraction
resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')



import cv2
import os
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

def capture_and_save_features(class_name):
    output_folder="dataset4"
    num_images=50
    # Initialize ResNet50 Model (without top layer)
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    
    # Load the Haar cascade for face detection
    face_cascade_path = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    # Create the "new" folder in the output dataset if it doesn't exist
    output_class_path = os.path.join(output_folder, class_name)
    if not os.path.exists(output_class_path):
        os.makedirs(output_class_path)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    captured_count = 0
    
    print("Press 'c' to capture an image with a detected face. Press 'q' to quit.")
    
    while captured_count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image from webcam.")
            break
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            # Draw rectangle around detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Show the frame
        cv2.imshow("Webcam - Press 'c' to capture", frame)
        
        # Wait for user input
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):  # 'c' to capture
            for (x, y, w, h) in faces:
                # Crop and resize the face to 224x224 (ResNet50 input size)
                face = frame[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (224, 224))
                
                # Preprocess the image for ResNet50
                face_array = image.img_to_array(face_resized)
                face_array = np.expand_dims(face_array, axis=0)
                face_array = preprocess_input(face_array)
                
                # Extract features using ResNet50
                features = model.predict(face_array)
                
                # Save the features to a file in "new" folder
                feature_file = os.path.join(output_class_path, f"image_{captured_count + 1}.npy")
                np.save(feature_file, features)
                
                captured_count += 1
                print(f"Captured and saved feature {captured_count}/{num_images}")
                
                if captured_count >= num_images:
                    break
        elif key & 0xFF == ord('q'):  # 'q' to quit
            print("Quitting without completing the capture.")
            break
    
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    
    print("Feature extraction and saving completed!")

# Run the function

