"""
Analytics and progress tracking for student performance.
"""

from typing import List, Dict
from collections import Counter
import streamlit as st


def calculate_performance_stats(results: List[Dict]) -> Dict:
    """
    Calculate performance statistics from quiz results.
    
    Args:
        results: List of result dictionaries with question data and correctness
    
    Returns:
        Dictionary with performance metrics
    """
    if not results:
        return {
            "total_questions": 0,
            "correct": 0,
            "percentage": 0,
            "weak_areas": [],
            "strong_areas": []
        }
    
    total = len(results)
    correct = sum(1 for r in results if r.get('is_correct', False))
    percentage = (correct / total) * 100
    
    # Track topics (based on question content - simple heuristic)
    # In a real implementation, you'd track this more systematically
    topic_performance = {}
    
    for result in results:
        question_text = result.get('question', '')
        # Simple topic extraction (you can improve this)
        if 'chain-of-thought' in question_text.lower() or 'cot' in question_text.lower():
            topic = 'Chain-of-Thought Prompting'
        elif 'compress' in question_text.lower():
            topic = 'COMPRESS Strategy'
        elif 'write' in question_text.lower():
            topic = 'WRITE Strategy'
        elif 'select' in question_text.lower():
            topic = 'SELECT Strategy'
        else:
            topic = 'General Concepts'
        
        if topic not in topic_performance:
            topic_performance[topic] = {'correct': 0, 'total': 0}
        
        topic_performance[topic]['total'] += 1
        if result.get('is_correct', False):
            topic_performance[topic]['correct'] += 1
    
    # Identify weak and strong areas
    weak_areas = []
    strong_areas = []
    
    for topic, stats in topic_performance.items():
        accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        if accuracy < 0.6:  # Less than 60% correct
            weak_areas.append({
                'topic': topic,
                'accuracy': accuracy,
                'correct': stats['correct'],
                'total': stats['total']
            })
        elif accuracy >= 0.8:  # 80% or more correct
            strong_areas.append({
                'topic': topic,
                'accuracy': accuracy,
                'correct': stats['correct'],
                'total': stats['total']
            })
    
    return {
        "total_questions": total,
        "correct": correct,
        "percentage": percentage,
        "weak_areas": weak_areas,
        "strong_areas": strong_areas
    }


def display_performance_summary(results: List[Dict]):
    """
    Display a student-friendly performance summary.
    
    Args:
        results: List of result dictionaries
    """
    stats = calculate_performance_stats(results)
    
    st.markdown("---")
    st.subheader("📊 Your Performance")
    
    # Overall score with color coding
    percentage = stats['percentage']
    if percentage >= 80:
        score_color = "🟢"
        message = "Excellent work! You're well-prepared! 🎉"
    elif percentage >= 60:
        score_color = "🟡"
        message = "Good progress! Keep practicing. 💪"
    else:
        score_color = "🔴"
        message = "Keep studying - you'll get there! 📚"
    
    # Display score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions", stats['total_questions'])
    with col2:
        st.metric("Correct", stats['correct'])
    with col3:
        st.metric("Score", f"{percentage:.0f}%")
    
    st.info(f"{score_color} {message}")
    
    # Weak areas (areas needing review)
    if stats['weak_areas']:
        st.markdown("### 🎯 Focus Areas (Need Review)")
        st.warning("These topics need more practice:")
        for area in stats['weak_areas']:
            accuracy_pct = area['accuracy'] * 100
            st.write(f"- **{area['topic']}**: {area['correct']}/{area['total']} correct ({accuracy_pct:.0f}%) ⚠️")
    
    # Strong areas
    if stats['strong_areas']:
        st.markdown("### ✅ Strong Areas")
        st.success("You've mastered these topics:")
        for area in stats['strong_areas']:
            accuracy_pct = area['accuracy'] * 100
            st.write(f"- **{area['topic']}**: {area['correct']}/{area['total']} correct ({accuracy_pct:.0f}%) 🌟")
    
    # Call to action
    if stats['weak_areas']:
        st.markdown("---")
        st.info("💡 **Tip**: Generate more questions focusing on your weak areas to improve your understanding!")


def get_study_recommendation(percentage: float) -> str:
    """
    Get a personalized study recommendation based on performance.
    
    Args:
        percentage: Performance percentage (0-100)
    
    Returns:
        Recommendation text
    """
    if percentage >= 90:
        return "You're exam-ready! Consider helping classmates or exploring advanced topics."
    elif percentage >= 80:
        return "Almost there! Review your weak areas and you'll be fully prepared."
    elif percentage >= 70:
        return "Good foundation. Focus on practicing weak areas and reviewing source material."
    elif percentage >= 60:
        return "Keep going! Create more practice questions and review the course material thoroughly."
    else:
        return "Don't worry! Break down topics into smaller chunks and practice consistently."