from flask import Flask, request, jsonify, render_template_string
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predictor import GradePredictor

app = Flask(__name__)
predictor = None

# HTML template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🎓 Grade Prediction System</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .result { background: #f0f8ff; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .error { background: #ffe6e6; color: #d00; }
    </style>
</head>
<body>
    <h1>🎓 Student Grade Prediction</h1>
    
    <form id="predictionForm">
        <h2>Student Information</h2>
        <div class="form-group">
            <label>CGPA (5.0-10.0):</label>
            <input type="number" name="cgpa" min="5" max="10" step="0.1" required value="8.5">
        </div>
        
        <div class="form-group">
            <label>Attendance %:</label>
            <input type="number" name="attendance" min="0" max="100" required value="85">
        </div>
        
        <div class="form-group">
            <label>Previous Semester Average:</label>
            <input type="number" name="previous_avg" min="5" max="10" step="0.1" required value="8.2">
        </div>
        
        <div class="form-group">
            <label>Branch:</label>
            <select name="branch_code" required>
                <option value="CSE">CSE</option>
                <option value="ECE">ECE</option>
                <option value="ME">ME</option>
                <option value="CE">CE</option>
                <option value="EE">EE</option>
            </select>
        </div>
        
        <h2>Course Information</h2>
        <div class="form-group">
            <label>Difficulty Level (1-5):</label>
            <input type="number" name="difficulty_level" min="1" max="5" required value="3">
        </div>
        
        <div class="form-group">
            <label>Credits:</label>
            <select name="credits" required>
                <option value="2">2</option>
                <option value="3" selected>3</option>
                <option value="4">4</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Theory Weight (0.0-1.0):</label>
            <input type="number" name="theory_weight" min="0" max="1" step="0.1" required value="0.6">
        </div>
        
        <div class="form-group">
            <label>Course Domain:</label>
            <select name="domain_tags" required>
                <option value="AI">AI</option>
                <option value="ML" selected>ML</option>
                <option value="Web">Web</option>
                <option value="DBMS">DBMS</option>
                <option value="Networks">Networks</option>
                <option value="Security">Security</option>
                <option value="Data_Science">Data Science</option>
                <option value="Cloud">Cloud</option>
            </select>
        </div>
        
        <h2>Student Interests</h2>
        <div class="form-group">
            <label>Select interests (hold Ctrl to select multiple):</label>
            <select name="interests" multiple size="5" required style="height: 120px;">
                <option value="AI">AI</option>
                <option value="ML" selected>ML</option>
                <option value="Web">Web</option>
                <option value="DBMS">DBMS</option>
                <option value="Networks">Networks</option>
                <option value="Security">Security</option>
                <option value="Data_Science">Data Science</option>
                <option value="Cloud">Cloud</option>
            </select>
        </div>
        
        <button type="submit">Predict Grade</button>
    </form>
    
    <div id="result"></div>
    
    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const interests = Array.from(formData.getAll('interests'));
            
            const data = {
                student: {
                    cgpa: parseFloat(formData.get('cgpa')),
                    attendance: parseFloat(formData.get('attendance')),
                    previous_avg: parseFloat(formData.get('previous_avg')),
                    branch_code: formData.get('branch_code')
                },
                course: {
                    difficulty_level: parseInt(formData.get('difficulty_level')),
                    credits: parseInt(formData.get('credits')),
                    theory_weight: parseFloat(formData.get('theory_weight')),
                    domain_tags: formData.get('domain_tags')
                },
                interests: interests
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('result');
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result">
                            <h3>🎯 Prediction Result</h3>
                            <p><strong>Predicted Grade:</strong> ${result.predicted_grade}/10.0</p>
                            <p><strong>Message:</strong> ${result.message}</p>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>❌ Error</h3>
                            <p>${result.error}</p>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `
                    <div class="result error">
                        <h3>❌ Connection Error</h3>
                        <p>Failed to connect to server</p>
                    </div>
                `;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict_grade_api():
    """API endpoint for grade prediction"""
    try:
        data = request.json
        
        student_data = data['student']
        course_data = data['course']
        interests_data = data['interests']
        
        predicted_grade = predictor.predict_grade(student_data, course_data, interests_data)
        
        # Performance interpretation
        if predicted_grade >= 9.0:
            message = "Excellent performance expected! 🎉"
        elif predicted_grade >= 8.0:
            message = "Very good performance expected! ✅"
        elif predicted_grade >= 7.0:
            message = "Good performance expected 📈"
        elif predicted_grade >= 6.0:
            message = "Average performance - consistent effort needed ⚠️"
        else:
            message = "Needs improvement - consider additional support 🚨"
        
        return jsonify({
            'success': True,
            'predicted_grade': predicted_grade,
            'message': message
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'model_type': predictor.metadata['model_type'] if predictor else 'None'
    })

def start_api(host='0.0.0.0', port=5000):
    """Start the Flask API server"""
    global predictor
    try:
        predictor = GradePredictor()
        print(f"✅ Model loaded successfully!")
        print(f"🌐 Starting web server at http://{host}:{port}")
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"❌ Failed to start API: {e}")

if __name__ == '__main__':
    start_api()