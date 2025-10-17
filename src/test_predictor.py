import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predictor import GradePredictor

def test_predictor():
    """Test the predictor with various scenarios"""
    print("🧪 Testing Grade Predictor")
    print("=" * 50)
    
    try:
        predictor = GradePredictor()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "name": "High Performer in Interest Area",
            "student": {"cgpa": 9.5, "attendance": 95, "previous_avg": 9.3, "branch_code": "CSE"},
            "course": {"difficulty_level": 2, "credits": 3, "theory_weight": 0.6, "domain_tags": "AI"},
            "interests": ["AI", "ML", "Data_Science"]
        },
        {
            "name": "Average Student in Unrelated Course", 
            "student": {"cgpa": 6.8, "attendance": 65, "previous_avg": 6.5, "branch_code": "ME"},
            "course": {"difficulty_level": 5, "credits": 4, "theory_weight": 0.8, "domain_tags": "Networks"},
            "interests": ["Web"]
        },
        {
            "name": "Good Student with Domain Match",
            "student": {"cgpa": 8.2, "attendance": 88, "previous_avg": 7.9, "branch_code": "ECE"},
            "course": {"difficulty_level": 3, "credits": 3, "theory_weight": 0.7, "domain_tags": "Web"},
            "interests": ["Web", "DBMS", "Cloud"]
        }
    ]
    
    print("\n" + "📊" * 20)
    print("TEST RESULTS:")
    print("📊" * 20)
    
    for i, test_case in enumerate(test_cases, 1):
        grade = predictor.predict_grade(
            test_case["student"],
            test_case["course"], 
            test_case["interests"]
        )
        
        print(f"\nTest {i}: {test_case['name']}")
        print(f"  Student: CGPA {test_case['student']['cgpa']}, Attendance {test_case['student']['attendance']}%")
        print(f"  Course: {test_case['course']['domain_tags']} (Difficulty: {test_case['course']['difficulty_level']})")
        print(f"  Interests: {', '.join(test_case['interests'])}")
        print(f"  🎯 Predicted Grade: {grade:.2f}/10.0")
        
        # Performance interpretation
        if grade >= 9.0:
            performance = "💎 EXCELLENT"
        elif grade >= 8.0:
            performance = "✅ VERY GOOD" 
        elif grade >= 7.0:
            performance = "📈 GOOD"
        elif grade >= 6.0:
            performance = "⚠️  AVERAGE"
        else:
            performance = "🚨 NEEDS IMPROVEMENT"
            
        print(f"  Performance: {performance}")

if __name__ == "__main__":
    test_predictor()