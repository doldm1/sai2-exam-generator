"""
Prompt templates for question generation and grading.
"""

SYSTEM_PROMPT = """You are a university exam question generator. Your task is to create high-quality exam questions based ONLY on the provided course material.

CRITICAL RULES:
1. Use ONLY information explicitly stated in the provided course material
2. Every question MUST cite the exact page number it comes from
3. Do NOT use external knowledge or information not in the material
4. If the material doesn't contain enough information for a question, skip it
5. Create questions that test understanding, not just memorization

DISTRACTOR QUALITY (VERY IMPORTANT):
- Wrong answers (distractors) must be PLAUSIBLE but clearly incorrect
- Each distractor should represent a common misconception or related concept
- Avoid obviously wrong answers (e.g., completely unrelated topics)
- Distractors should be of similar length and complexity as the correct answer
- Use content from the same topic area to make distractors believable

OUTPUT FORMAT:
Return ONLY valid JSON with this exact structure (no markdown, no code blocks):
{
  "questions": [
    {
      "question": "Clear, specific question text",
      "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
      "correct_answer": "A",
      "explanation": "Brief explanation of why this is correct (2-3 sentences)",
      "source_page": 5,
      "source_excerpt": "Exact quote or paraphrase from the source material"
    }
  ]
}
"""

def get_question_generation_prompt(pages_content: dict, num_questions: int = 5, topic: str = None) -> str:
    """
    Generate the user prompt for question generation.
    
    Args:
        pages_content: Dictionary mapping page numbers to text content
        num_questions: Number of questions to generate
        topic: Optional topic filter
    
    Returns:
        Formatted prompt string
    """
    # Build the course material section
    material_text = "COURSE MATERIAL:\n\n"
    for page_num, content in pages_content.items():
        material_text += f"=== PAGE {page_num} ===\n{content}\n\n"
    
    # Build the request section
    topic_instruction = f" focusing on the topic: {topic}" if topic else ""
    request_text = f"""
TASK:
Generate exactly {num_questions} multiple-choice exam questions{topic_instruction}.

Requirements for each question:
- 4 options (A, B, C, D)
- Only one correct answer
- Question must be answerable using ONLY the material above
- Include the source page number
- Include a brief excerpt from the source material that supports the answer
- Ensure distractors (wrong answers) are plausible but clearly incorrect

Return the questions in the JSON format specified in your system instructions.
"""
    
    return material_text + request_text


GRADING_SYSTEM_PROMPT = """You are a fair and accurate exam grader. Your task is to evaluate student answers against the correct answer.

For multiple-choice questions:
- Check if the student's answer matches the correct answer exactly
- Return a simple correctness assessment

Return ONLY valid JSON (no markdown, no code blocks):
{
  "is_correct": true or false,
  "feedback": "Brief explanation"
}
"""

def get_grading_prompt(question: str, correct_answer: str, user_answer: str, explanation: str) -> str:
    """
    Generate the grading prompt.
    
    Args:
        question: The question text
        correct_answer: The correct answer
        user_answer: The student's answer
        explanation: Explanation of the correct answer
    
    Returns:
        Formatted grading prompt
    """
    return f"""
QUESTION: {question}

CORRECT ANSWER: {correct_answer}
EXPLANATION: {explanation}

STUDENT'S ANSWER: {user_answer}

Please evaluate if the student's answer is correct.
"""