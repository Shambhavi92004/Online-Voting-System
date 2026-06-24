import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle
import cv2
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
def train_save_model():
                # Paths
                dataset_path = 'dataset4'
                models_path = 'models'
                if not os.path.exists(models_path):
                    os.makedirs(models_path)

                # Load the dataset
                X = []  # Features
                y = []  # Labels

                class_labels = {class_name: idx for idx, class_name in enumerate(os.listdir(dataset_path))}
                inverse_labels = {idx: class_name for class_name, idx in class_labels.items()}
                # Save the dictionary as a pickle file
                with open('inverse_labels.pkl', 'wb') as file:
                    pickle.dump(inverse_labels, file)

                print("Dictionary saved as 'inverse_labels.pkl'")
                for class_name, label in class_labels.items():
                    class_folder = os.path.join(dataset_path, class_name)
                    if not os.path.isdir(class_folder):
                        continue
                    
                    for file_name in os.listdir(class_folder):
                        file_path = os.path.join(class_folder, file_name)
                        if file_path.endswith('.npy'):
                            features = np.load(file_path)
                            X.append(features.flatten())
                            y.append(label)

                X = np.array(X)
                y = np.array(y)

                # Split the data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Train Random Forest Classifier
                rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
                rf_model.fit(X_train, y_train)
                rf_preds = rf_model.predict(X_test)
                rf_acc = accuracy_score(y_test, rf_preds)
                print(f"Random Forest Accuracy: {rf_acc * 100:.2f}%")

                # Save Random Forest model
                rf_model_path = os.path.join(models_path, 'random_forest_model.pkl')
                with open(rf_model_path, 'wb') as f:
                    pickle.dump(rf_model, f)

                # Train XGBoost Classifier
                xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
                print(y_train)




                # Encode labels
                label_encoder = LabelEncoder()
                y_train_encoded = label_encoder.fit_transform(y_train)
                y_test_encoded = label_encoder.transform(y_test)  # Ensure y_test is also encoded

                # Train XGBoost
                xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
                xgb_model.fit(X_train, y_train_encoded)

                # Predict
                xgb_preds = xgb_model.predict(X_test)

                # Decode predictions back to original labels (optional)
                xgb_preds_decoded = label_encoder.inverse_transform(xgb_preds)

                # Calculate accuracy
                xgb_acc = accuracy_score(y_test_encoded, xgb_preds)
                print(f"XGBoost Accuracy: {xgb_acc * 100:.2f}%")


                # Save XGBoost model
                xgb_model_path = os.path.join(models_path, 'xgboost_model.pkl')
                with open(xgb_model_path, 'wb') as f:
                    pickle.dump(xgb_model, f)

