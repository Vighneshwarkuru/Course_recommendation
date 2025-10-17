import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predictor import GradePredictor

def interactive_predictor():
    """Interactive command-line interface for grade prediction"""
    print("🎓 Student Grade Prediction System")
    print("=" * 50)
    
    # Initialize predictor
    try:
        predictor = GradePredictor()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Show model info
    model_info = predictor.get_model_info()
    print(f"📊 Model Performance: R² = {model_info['test_r2']:.4f}")
    print(f"🎯 Average Error: {model_info['test_rmse']:.2f} grade points")
    print()
    
    while True:
        print("\n" + "="*50)
        print("Enter Student Details:")
        print("="*50)
        
        try:
            student_data = {
                'cgpa': float(input("CGPA (5.0-10.0): ")),
                'attendance': float(input("Attendance % (0-100): ")),
                'previous_avg': float(input("Previous Semester Average (5.0-10.0): ")),
                'branch_code': input("Branch (CE/CSE/ECE/ME/EE): ").upper()
            }
            
            # Validate branch
            if student_data['branch_code'] not in ['CE', 'CSE', 'ECE', 'ME', 'EE']:
                print("❌ Invalid branch! Using CSE as default.")
                student_data['branch_code'] = 'CSE'
            
            print("\n" + "="*50)
            print("Enter Course Details:")
            print("="*50)
            
            course_data = {
                'difficulty_level': int(input("Difficulty Level (1-5): ")),
                'credits': int(input("Credits (2/3/4): ")),
                'theory_weight': float(input("Theory Weight (0.0-1.0): ")),
                'domain_tags': input("Course Domain (AI/Web/DBMS/ML/Networks/Security/Data_Science/Cloud): ").title()
            }
            
            # Validate domain
            valid_domains = ['AI', 'Web', 'DBMS', 'ML', 'Networks', 'Security', 'Data_Science', 'Cloud']
            if course_data['domain_tags'] not in valid_domains:
                print("❌ Invalid domain! Using 'AI' as default.")
                course_data['domain_tags'] = 'AI'
            
            print("\n" + "="*50)
            print("Enter Student Interests:")
            print("="*50)
            print("Available domains: AI, Web, DBMS, ML, Networks, Security, Data_Science, Cloud")
            interests_input = input("Enter interests (comma-separated): ").title()
            interests_data = [interest.strip() for interest in interests_input.split(',') if interest.strip()]
            
            # Predict grade
            predicted_grade = predictor.predict_grade(student_data, course_data, interests_data)
            
            print("\n" + "🎯" * 25)
            print("PREDICTION RESULT:")
            print("🎯" * 25)
            print(f"📊 Predicted Grade: {predicted_grade:.2f}/10.0")
            
            # Interpretation
            if predicted_grade >= 9.0:
                print("💎 Performance: Excellent! Student should excel in this course.")
            elif predicted_grade >= 8.0:
                print("✅ Performance: Very Good! Strong performance expected.")
            elif predicted_grade >= 7.0:
                print("📈 Performance: Good! Solid performance expected.")
            elif predicted_grade >= 6.0:
                print("⚠️  Performance: Average. May need consistent effort.")
            else:
                print("🚨 Performance: Needs improvement. Consider additional support.")
            
            print("🎯" * 25)
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            print("Please try again with valid numbers.")
            continue
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
        
        # Continue?
        continue_pred = input("\nMake another prediction? (y/n): ").lower()
        if continue_pred != 'y':
            print("\nThank you for using the Grade Prediction System! 👋")
            break

if __name__ == "__main__":
    interactive_predictor()