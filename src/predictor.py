import pickle
import json
import pandas as pd
import numpy as np
import os

class GradePredictor:
    def __init__(self, models_dir="models"):
        """Initialize the predictor with saved model, scaler, and feature list"""
        self.models_dir = models_dir
        self.load_models()
        
        # Domain list (should match training)
        self.domains = ['AI', 'Web', 'DBMS', 'ML', 'Networks', 'Security', 'Data_Science', 'Cloud']
        self.branches = ['CE', 'CSE', 'ECE', 'ME', 'EE']
    
    def load_models(self):
        """Load all required model files"""
        try:
            model_path = os.path.join(self.models_dir, "improved_feature_model.pkl")
            scaler_path = os.path.join(self.models_dir, "feature_scaler.pkl")
            features_path = os.path.join(self.models_dir, "selected_features.json")
            metadata_path = os.path.join(self.models_dir, "improved_model_metadata.json")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            with open(features_path, 'r') as f:
                self.selected_features = json.load(f)
            
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            print("✅ Models loaded successfully!")
            print(f"📊 Model Type: {self.metadata['model_type']}")
            print(f"🎯 Test R²: {self.metadata['test_r2']:.4f}")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def predict_grade(self, student_data, course_data, interests_data):
        """
        Predict grade for a student-course combination
        
        Parameters:
        student_data: dict with keys ['cgpa', 'attendance', 'previous_avg', 'branch_code']
        course_data: dict with keys ['difficulty_level', 'credits', 'theory_weight', 'domain_tags']
        interests_data: list of domains the student is interested in
        
        Returns:
        predicted_grade: float between 5.0 and 10.0
        """
        try:
            # Calculate domain match
            domain_match = 1.0 if course_data['domain_tags'] in interests_data else 0.0
            
            # Build feature vector
            features = {}
            
            # Base features
            features['cgpa'] = student_data['cgpa']
            features['attendance'] = student_data['attendance']
            features['previous_avg'] = student_data['previous_avg']
            features['difficulty_level'] = course_data['difficulty_level']
            features['credits'] = course_data['credits']
            features['theory_weight'] = course_data['theory_weight']
            features['domain_match'] = domain_match
            
            # Default values for computed features
            features['grade_consistency'] = 0.5
            features['course_avg_grade'] = 7.5
            
            # Interaction features
            features['cgpa_difficulty_interaction'] = student_data['cgpa'] * (6 - course_data['difficulty_level'])
            features['attendance_difficulty_interaction'] = student_data['attendance'] * (6 - course_data['difficulty_level'])
            features['cgpa_attendance_interaction'] = student_data['cgpa'] * student_data['attendance'] / 100
            
            # Branch encoding
            for branch in self.branches:
                features[f'branch_{branch}'] = 1 if student_data['branch_code'] == branch else 0
            
            # Domain encoding
            for domain in self.domains:
                features[f'domain_{domain}'] = 1 if course_data['domain_tags'] == domain else 0
            
            # Interest encoding
            for domain in self.domains:
                features[f'interest_{domain}'] = 1 if domain in interests_data else 0
            
            # Create feature vector with only selected features
            feature_vector = {}
            for feature in self.selected_features:
                if feature in features:
                    feature_vector[feature] = features[feature]
                else:
                    feature_vector[feature] = 0
            
            # Convert to DataFrame
            feature_df = pd.DataFrame([feature_vector])[self.selected_features]
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_df)
            
            # Predict
            predicted_grade = self.model.predict(feature_vector_scaled)[0]
            
            # Clip to valid range
            final_grade = max(5.0, min(10.0, round(predicted_grade, 2)))
            
            return final_grade
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            # Fallback prediction based on CGPA
            return max(5.0, min(10.0, round(student_data['cgpa'] + np.random.normal(0, 0.3), 2)))
    
    def get_model_info(self):
        """Get information about the loaded model"""
        return self.metadata

if __name__ == "__main__":
    # Test the predictor
    predictor = GradePredictor()
    
    # Test prediction
    test_student = {
        'cgpa': 8.5,
        'attendance': 85.0,
        'previous_avg': 8.2,
        'branch_code': 'CSE'
    }
    
    test_course = {
        'difficulty_level': 3,
        'credits': 3,
        'theory_weight': 0.6,
        'domain_tags': 'ML'
    }
    
    test_interests = ['ML', 'AI', 'Data_Science']
    
    grade = predictor.predict_grade(test_student, test_course, test_interests)
    print(f"Test Prediction: {grade}")