## 📁 Project Structure

```
liver/
├── index.html          # Frontend HTML interface
├── style.css           # CSS styling
├── script.js           # JavaScript functionality
├── app.py              # Flask backend server
├── cirrhosis.csv       # Dataset
├── liver.ipynb         # Jupyter notebook with ML model
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Features

- **Interactive Web Interface**: User-friendly form for entering patient data
- **Real-time Predictions**: Instant cirrhosis status predictions
- **Risk Analysis**: Identifies and displays risk factors
- **Dataset Statistics**: Visual representation of dataset metrics
- **Responsive Design**: Works on desktop and mobile devices
- **XGBoost Model**: Advanced machine learning with 200 estimators
- **SMOTE**: Handles class imbalance in training data



## 📊 Model Information

- **Algorithm**: XGBoost Classifier
- **Features**: 17 clinical and laboratory parameters
  - N_Days, Drug, Age, Sex, Ascites, Hepatomegaly, Spiders, Edema
  - Bilirubin, Cholesterol, Albumin, Copper, Alk_Phos
  - SGOT, Triglycerides, Platelets, Prothrombin, Stage

- **Target Classes**:
  - C: Censored (Alive)
  - CL: Censored due to liver transplant
  - D: Death

- **Preprocessing**:
  - SMOTE for handling class imbalance
  - Label encoding for categorical variables
  - Missing value imputation using mode

- **Model Parameters**:
  - n_estimators: 200
  - learning_rate: 0.05
  - max_depth: 4
  - subsample: 0.8
  - colsample_bytree: 0.8

## 🔌 API Endpoints

### POST /predict
Predict cirrhosis status for a patient

**Request Body:**
```json
{
  "age": 50,
  "sex": "F",
  "drug": "D-penicillamine",
  "ascites": "N",
  "hepatomegaly": "Y",
  "spiders": "Y",
  "edema": "N",
  "bilirubin": 1.1,
  "cholesterol": 302,
  "albumin": 4.14,
  "copper": 54,
  "alk_phos": 7394.8,
  "sgot": 113.52,
  "tryglicerides": 88,
  "platelets": 221,
  "prothrombin": 10.6,
  "stage": "3"
}
```

**Response:**
```json
{
  "status": "C",
  "confidence": 85.42,
  "probabilities": {
    "C": 85.42,
    "CL": 10.23,
    "D": 4.35
  },
  "risk_factors": [...]
}
```

### GET /dataset-stats
Get dataset statistics

**Response:**
```json
{
  "total_records": 418,
  "male_count": 44,
  "female_count": 374,
  "avg_age": 50.5,
  "status_distribution": {...}
}
```

### POST /train
Retrain the model with updated data

## 🎨 Frontend Features

1. **Input Form**
   - 17 input fields for patient data
   - Validation and error handling
   - Sample data loader for testing

2. **Results Display**
   - Predicted status with visual indicators
   - Confidence score with progress bar
   - Risk factor analysis
   - Color-coded severity levels

3. **Statistics Dashboard**
   - Total records in dataset
   - Patient demographics
   - Animated counters

4. **Responsive Design**
   - Mobile-friendly interface
   - Gradient backgrounds
   - Smooth animations

## 📝 Usage Example

1. Click "Load Sample Data" to populate the form
2. Review or modify the values
3. Click "Predict Status"
4. View the results:
   - Predicted status (C/CL/D)
   - Confidence percentage
   - Identified risk factors
   - Recommendations



## 📚 Technologies Used

### Frontend
- HTML5
- CSS3 (with gradients and animations)
- Vanilla JavaScript (ES6+)

### Backend
- Flask (Python web framework)
- XGBoost,SVM,RF (Machine Learning)
- scikit-learn (Data preprocessing)
- pandas (Data manipulation)
- imbalanced-learn (SMOTE)

## 📄 License

This project is created for educational purposes.



## 🔮 Future Enhancements

- [ ] Add data visualization charts
- [ ] Export predictions to PDF
- [ ] Multiple model comparison
- [ ] Historical prediction tracking
- [ ] Advanced feature engineering
- [ ] SHAP value visualization
- [ ] User authentication
- [ ] Database integration

---

**Note**: This system is for educational and research purposes only. Always consult healthcare professionals for medical decisions.
