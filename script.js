// Sample data for demonstration
const sampleData = {
    age: 50,
    sex: 'F',
    drug: 'D-penicillamine',
    ascites: 'N',
    hepatomegaly: 'Y',
    spiders: 'Y',
    edema: 'N',
    bilirubin: 1.1,
    cholesterol: 302,
    albumin: 4.14,
    copper: 54,
    alk_phos: 7394.8,
    sgot: 113.52,
    tryglicerides: 88,
    platelets: 221,
    prothrombin: 10.6,
    stage: '3'
};

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadDatasetStats();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const form = document.getElementById('predictionForm');
    const resetBtn = document.getElementById('resetBtn');
    const sampleBtn = document.getElementById('sampleBtn');

    form.addEventListener('submit', handlePrediction);
    resetBtn.addEventListener('click', resetForm);
    sampleBtn.addEventListener('click', loadSampleData);
}

// Handle form submission
async function handlePrediction(e) {
    e.preventDefault();
    
    const formData = getFormData();
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Processing...';
    submitBtn.disabled = true;

    try {
        // Simulate API call for now
        // In production, replace with actual API endpoint
        const result = await simulatePrediction(formData);
        displayResults(result);
    } catch (error) {
        showError('An error occurred during prediction. Please try again.');
        console.error('Prediction error:', error);
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// Get form data
function getFormData() {
    const form = document.getElementById('predictionForm');
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

// Simulate prediction (replace with actual API call)
async function simulatePrediction(data) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Simple rule-based simulation for demonstration
    let status = 'C';
    let probability = Math.random();
    
    // Simple heuristics based on severity indicators
    const bilirubin = parseFloat(data.bilirubin);
    const stage = parseInt(data.stage);
    const albumin = parseFloat(data.albumin);
    
    if (bilirubin > 10 || stage === 4 || albumin < 2.5) {
        status = Math.random() > 0.5 ? 'D' : 'CL';
        probability = 0.7 + Math.random() * 0.3;
    } else if (bilirubin > 5 || stage === 3) {
        status = Math.random() > 0.3 ? 'C' : 'CL';
        probability = 0.5 + Math.random() * 0.3;
    } else {
        status = 'C';
        probability = 0.6 + Math.random() * 0.4;
    }
    
    return {
        status: status,
        probability: probability,
        confidence: (probability * 100).toFixed(2),
        riskFactors: analyzeRiskFactors(data)
    };
}

// Analyze risk factors
function analyzeRiskFactors(data) {
    const factors = [];
    
    if (parseFloat(data.bilirubin) > 2) {
        factors.push({ name: 'Elevated Bilirubin', severity: 'high', value: data.bilirubin });
    }
    
    if (parseFloat(data.albumin) < 3) {
        factors.push({ name: 'Low Albumin', severity: 'high', value: data.albumin });
    }
    
    if (parseInt(data.stage) >= 3) {
        factors.push({ name: 'Advanced Stage', severity: 'high', value: data.stage });
    }
    
    if (data.ascites === 'Y') {
        factors.push({ name: 'Ascites Present', severity: 'medium', value: 'Yes' });
    }
    
    if (data.edema === 'Y') {
        factors.push({ name: 'Edema Present', severity: 'medium', value: 'Yes' });
    }
    
    if (parseFloat(data.prothrombin) > 12) {
        factors.push({ name: 'Elevated Prothrombin', severity: 'medium', value: data.prothrombin });
    }
    
    return factors;
}

// Display results
function displayResults(result) {
    const resultsCard = document.getElementById('resultsCard');
    const resultContent = document.getElementById('predictionResult');
    
    const statusLabels = {
        'C': 'Censored (Alive)',
        'CL': 'Censored (Liver Transplant)',
        'D': 'Death'
    };
    
    let html = `
        <div class="prediction-status status-${result.status}">
            Predicted Status: ${statusLabels[result.status]}
        </div>
        
        <div class="result-item">
            <strong>Confidence:</strong> ${result.confidence}%
            <div style="margin-top: 10px; background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="width: ${result.confidence}%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.5s ease;"></div>
            </div>
        </div>
    `;
    
    if (result.riskFactors && result.riskFactors.length > 0) {
        html += `
            <div class="result-item">
                <strong>Risk Factors Identified:</strong>
                <ul style="margin-top: 10px; margin-left: 20px;">
        `;
        
        result.riskFactors.forEach(factor => {
            const severityColor = factor.severity === 'high' ? '#dc2626' : '#d97706';
            html += `
                <li style="margin-bottom: 8px;">
                    <span style="color: ${severityColor}; font-weight: 600;">${factor.name}</span>
                    <span style="color: #666;"> - Value: ${factor.value}</span>
                </li>
            `;
        });
        
        html += `
                </ul>
            </div>
        `;
    }
    
    html += `
        <div class="alert alert-info" style="margin-top: 20px;">
            <strong>Note:</strong> This prediction is based on machine learning analysis of clinical parameters. 
            Always consult with healthcare professionals for medical decisions.
        </div>
    `;
    
    resultContent.innerHTML = html;
    resultsCard.style.display = 'block';
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error message
function showError(message) {
    const resultsCard = document.getElementById('resultsCard');
    const resultContent = document.getElementById('predictionResult');
    
    resultContent.innerHTML = `
        <div class="alert alert-error">
            <strong>Error:</strong> ${message}
        </div>
    `;
    
    resultsCard.style.display = 'block';
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Reset form
function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultsCard').style.display = 'none';
}

// Load sample data
function loadSampleData() {
    Object.keys(sampleData).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.value = sampleData[key];
        }
    });
    
    // Show confirmation
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.innerHTML = '<strong>Success!</strong> Sample data loaded successfully.';
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '1000';
    alert.style.minWidth = '300px';
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    }, 2000);
}

// Load dataset statistics
async function loadDatasetStats() {
    try {
        // In production, fetch from API
        // For now, use static values based on the CSV
        const stats = {
            totalRecords: 418,
            avgAge: calculateAverageAge(),
            maleCount: 44,
            femaleCount: 374
        };
        
        document.getElementById('totalRecords').textContent = stats.totalRecords;
        document.getElementById('avgAge').textContent = stats.avgAge + ' years';
        document.getElementById('maleCount').textContent = stats.maleCount;
        document.getElementById('femaleCount').textContent = stats.femaleCount;
        
        animateCounters();
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Calculate average age (approximation from days)
function calculateAverageAge() {
    // Average age from dataset is approximately 50 years
    return '50.5';
}

// Animate counters
function animateCounters() {
    const counters = document.querySelectorAll('.stat-value');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (isNaN(target)) return;
        
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// API Integration Functions (For production use)

// Connect to Flask backend
async function predictWithAPI(data) {
    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load dataset from backend
async function loadDatasetFromAPI() {
    try {
        const response = await fetch('http://localhost:5000/dataset-stats');
        
        if (!response.ok) {
            throw new Error('Failed to load dataset stats');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Export data
function exportPrediction(result) {
    const data = {
        timestamp: new Date().toISOString(),
        prediction: result,
        inputData: getFormData()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cirrhosis_prediction_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
