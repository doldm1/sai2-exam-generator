"""
Question generation using OpenAI's API.
Handles LLM calls for generating exam questions and grading answers.
"""

import openai
import json
from typing import List, Dict, Optional
from .prompts import (
    SYSTEM_PROMPT, 
    get_question_generation_prompt,
    GRADING_SYSTEM_PROMPT,
    get_grading_prompt
)


def generate_questions(
    pages_content: Dict[int, str],
    api_key: str,
    num_questions: int = 5,
    topic: Optional[str] = None,
    learning_objectives: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.3
) -> List[Dict]:
    """
    Generate exam questions from course material using OpenAI's API.
    
    Args:
        pages_content: Dictionary mapping page numbers to text content
        api_key: OpenAI API key
        num_questions: Number of questions to generate
        topic: Optional topic filter
        learning_objectives: Optional learning objectives to address
        model: OpenAI model to use
        temperature: Temperature for generation (0.0-1.0, lower = more focused)
    
    Returns:
        List of question dictionaries with structure:
        {
            "question": str,
            "options": List[str],
            "correct_answer": str,
            "explanation": str,
            "source_page": int,
            "source_excerpt": str
        }
    
    Raises:
        Exception: If API call fails or response is invalid
    """
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Generate the prompt
    user_prompt = get_question_generation_prompt(pages_content, num_questions, topic, learning_objectives)
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"}  # Ensure JSON response
        )
        
        # Parse the response
        response_text = response.choices[0].message.content
        questions_data = json.loads(response_text)
        
        # Validate the response structure
        if "questions" not in questions_data:
            raise ValueError("Response missing 'questions' field")
        
        questions = questions_data["questions"]
        
        # Validate each question has required fields
        required_fields = ["question", "options", "correct_answer", "explanation", "source_page"]
        for q in questions:
            for field in required_fields:
                if field not in q:
                    raise ValueError(f"Question missing required field: {field}")
        
        return questions
    
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating questions: {str(e)}")


def grade_answer(
    question: str,
    correct_answer: str,
    user_answer: str,
    explanation: str,
    api_key: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Grade a student's answer using OpenAI's API.
    
    Args:
        question: The question text
        correct_answer: The correct answer
        user_answer: The student's answer
        explanation: Explanation of the correct answer
        api_key: OpenAI API key
        model: OpenAI model to use
    
    Returns:
        Dictionary with:
        {
            "is_correct": bool,
            "feedback": str
        }
    """
    # For multiple choice, we can do simple matching
    # Extract just the letter (A, B, C, D) from answers
    correct_letter = correct_answer.strip().upper()[0] if correct_answer else ""
    user_letter = user_answer.strip().upper()[0] if user_answer else ""
    
    is_correct = correct_letter == user_letter
    
    if is_correct:
        feedback = f"Correct! {explanation}"
    else:
        feedback = f"Incorrect. The correct answer is {correct_answer}. {explanation}"
    
    return {
        "is_correct": is_correct,
        "feedback": feedback
    }


def check_api_key(api_key: str) -> bool:
    """
    Verify that the OpenAI API key is valid.
    
    Args:
        api_key: OpenAI API key to check
    
    Returns:
        True if valid, False otherwise
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        # Try a minimal API call
        client.models.list()
        return True
    except Exception:
        return False