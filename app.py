from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables for model and encoders
model = None
label_encoders = {}
feature_names = []

def train_and_save_model():
    """Train the model using the cirrhosis.csv data"""
    global model, label_encoders, feature_names
    
    try:
        # Load dataset
        df = pd.read_csv('cirrhosis.csv')
        
        # Drop ID column
        df.drop(columns=['ID'], inplace=True, errors='ignore')
        
        # Fill missing values
        df.fillna(df.mode().iloc[0], inplace=True)
        
        # Label encoding for categorical columns
        label_encoders = {}
        for col in df.select_dtypes(include='object').columns:
            if col != 'Status':  # Don't encode target yet
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
        
        # Encode target variable
        status_encoder = LabelEncoder()
        df['Status'] = status_encoder.fit_transform(df['Status'])
        label_encoders['Status'] = status_encoder
        
        # Split features and target
        X = df.drop('Status', axis=1)
        y = df['Status']
        
        feature_names = X.columns.tolist()
        
        # Apply SMOTE
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
        )
        
        # Train XGBoost model
        model = XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='logloss'
        )
        
        model.fit(X_train, y_train)
        
        # Save model and encoders
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        with open('encoders.pkl', 'wb') as f:
            pickle.dump(label_encoders, f)
        
        with open('features.pkl', 'wb') as f:
            pickle.dump(feature_names, f)
        
        print("Model trained and saved successfully!")
        return True
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return False

def load_model():
    """Load the trained model and encoders"""
    global model, label_encoders, feature_names
    
    try:
        if os.path.exists('model.pkl'):
            with open('model.pkl', 'rb') as f:
                model = pickle.load(f)
            
            with open('encoders.pkl', 'rb') as f:
                label_encoders = pickle.load(f)
            
            with open('features.pkl', 'rb') as f:
                feature_names = pickle.load(f)
            
            print("Model loaded successfully!")
        else:
            print("Model not found. Training new model...")
            train_and_save_model()
            
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print("Training new model...")
        train_and_save_model()

def preprocess_input(data):
    """Preprocess input data for prediction"""
    # Convert age from years to days (approximate)
    if 'age' in data:
        data['N_Days'] = int(float(data['age']) * 365.25)
        del data['age']
    
    # Map categorical variables
    categorical_mapping = {
        'Sex': data.get('sex', 'F'),
        'Drug': data.get('drug', 'Placebo'),
        'Ascites': data.get('ascites', 'N'),
        'Hepatomegaly': data.get('hepatomegaly', 'N'),
        'Spiders': data.get('spiders', 'N'),
        'Edema': data.get('edema', 'N')
    }
    
    # Create feature dictionary
    features = {
        'N_Days': data.get('N_Days', 1000),
        'Drug': categorical_mapping['Drug'],
        'Sex': categorical_mapping['Sex'],
        'Ascites': categorical_mapping['Ascites'],
        'Hepatomegaly': categorical_mapping['Hepatomegaly'],
        'Spiders': categorical_mapping['Spiders'],
        'Edema': categorical_mapping['Edema'],
        'Bilirubin': float(data.get('bilirubin', 1.0)),
        'Cholesterol': float(data.get('cholesterol', 250)),
        'Albumin': float(data.get('albumin', 3.5)),
        'Copper': float(data.get('copper', 50)),
        'Alk_Phos': float(data.get('alk_phos', 1000)),
        'SGOT': float(data.get('sgot', 100)),
        'Tryglicerides': float(data.get('tryglicerides', 100)),
        'Platelets': float(data.get('platelets', 250)),
        'Prothrombin': float(data.get('prothrombin', 10.5)),
        'Stage': float(data.get('stage', 2))
    }
    
    # Encode categorical features
    for col, value in features.items():
        if col in label_encoders and col != 'Status':
            try:
                features[col] = label_encoders[col].transform([value])[0]
            except:
                # If value not seen during training, use most common value
                features[col] = 0
    
    # Create DataFrame with correct feature order
    df = pd.DataFrame([features])
    df = df[feature_names]  # Ensure correct column order
    
    return df

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict cirrhosis status"""
    try:
        data = request.get_json()
        
        # Preprocess input
        X = preprocess_input(data)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Decode prediction
        status_labels = label_encoders['Status'].inverse_transform([prediction])[0]
        
        # Get confidence
        confidence = float(probabilities[prediction] * 100)
        
        # Analyze risk factors
        risk_factors = analyze_risk_factors(data)
        
        result = {
            'status': status_labels,
            'confidence': round(confidence, 2),
            'probabilities': {
                label: round(float(prob * 100), 2) 
                for label, prob in zip(label_encoders['Status'].classes_, probabilities)
            },
            'risk_factors': risk_factors
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_risk_factors(data):
    """Analyze risk factors from input data"""
    factors = []
    
    bilirubin = float(data.get('bilirubin', 0))
    albumin = float(data.get('albumin', 0))
    stage = int(data.get('stage', 0))
    prothrombin = float(data.get('prothrombin', 0))
    
    if bilirubin > 2:
        factors.append({
            'name': 'Elevated Bilirubin',
            'severity': 'high' if bilirubin > 5 else 'medium',
            'value': bilirubin
        })
    
    if albumin < 3.5:
        factors.append({
            'name': 'Low Albumin',
            'severity': 'high' if albumin < 2.5 else 'medium',
            'value': albumin
        })
    
    if stage >= 3:
        factors.append({
            'name': 'Advanced Disease Stage',
            'severity': 'high' if stage == 4 else 'medium',
            'value': stage
        })
    
    if data.get('ascites') == 'Y':
        factors.append({
            'name': 'Ascites Present',
            'severity': 'medium',
            'value': 'Yes'
        })
    
    if data.get('edema') == 'Y':
        factors.append({
            'name': 'Edema Present',
            'severity': 'high' if data.get('edema') == 'Y' else 'medium',
            'value': data.get('edema')
        })
    
    if prothrombin > 12:
        factors.append({
            'name': 'Elevated Prothrombin Time',
            'severity': 'medium',
            'value': prothrombin
        })
    
    return factors

@app.route('/dataset-stats', methods=['GET'])
def dataset_stats():
    """Get dataset statistics"""
    try:
        df = pd.read_csv('cirrhosis.csv')
        
        stats = {
            'total_records': len(df),
            'male_count': int(df[df['Sex'] == 'M'].shape[0]),
            'female_count': int(df[df['Sex'] == 'F'].shape[0]),
            'avg_age': round(df['Age'].mean() / 365.25, 1) if 'Age' in df.columns else 50,
            'status_distribution': df['Status'].value_counts().to_dict()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def retrain_model():
    """Retrain the model"""
    try:
        success = train_and_save_model()
        if success:
            load_model()
            return jsonify({'message': 'Model retrained successfully'})
        else:
            return jsonify({'error': 'Failed to train model'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load or train model on startup
    load_model()
    
    # Run the Flask app
    print("Starting Cirrhosis Prediction API...")
    print("Frontend available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
