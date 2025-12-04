"""
Prompt templates for question generation and grading.
"""

SYSTEM_PROMPT = """You are a university exam question generator. Your task is to create high-quality exam questions based ONLY on the provided course material.

CRITICAL RULES:
1. Use ONLY information explicitly stated in the provided course material
2. Every question MUST cite the exact page number it comes from
3. Do NOT use external knowledge or information not in the material
4. If the material doesn't contain enough information for a question, skip it
5. Create questions that test understanding and APPLICATION, not just memorization

QUESTION QUALITY - FEW-SHOT EXAMPLES:

GOOD QUESTIONS test application and understanding:
✅ "A system needs to process 10,000 tokens but has a 4,000 token limit. Which approach would be most effective?"
✅ "Based on the described scenario, which technique would best address the problem?"
✅ "In a situation where X constraint exists, how would you apply concept Y?"

BAD QUESTIONS test only recall and definitions:
❌ "What is the definition of concept X?"
❌ "List the three components of system Y."
❌ "What does the course material say about topic Z?"

KEY DIFFERENCES:
- Good questions present scenarios requiring decision-making
- Good questions test whether students can USE the knowledge
- Bad questions only test if students memorized definitions
- Bad questions can be answered by copy-pasting from the material

DISTRACTOR QUALITY (VERY IMPORTANT):
- Wrong answers (distractors) must be PLAUSIBLE but clearly incorrect
- Each distractor should represent a common misconception or related concept
- Avoid obviously wrong answers (e.g., completely unrelated topics)
- Distractors should be of similar length and complexity as the correct answer
- Use content from the same topic area to make distractors believable

SOURCE EXCERPT QUALITY - CRITICAL:

GOOD SOURCE EXCERPTS clearly connect answer to question:
✅ "The COMPRESS strategy reduces token usage by summarizing content while preserving essential information."
✅ "Chain-of-Thought prompting guides the model through step-by-step reasoning to reach accurate conclusions."

BAD SOURCE EXCERPTS are vague or missing the key term:
❌ "Summarization: LLM condenses content..." (missing "COMPRESS strategy" term)
❌ "• Context Maintenance • Structured..." (list format, unclear connection)
❌ "Memories... persistent storage..." (missing "WRITE" term entirely)

The source excerpt is THE PROOF. Students must be able to read it and immediately understand which answer is correct and why.

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
      "source_excerpt": "Direct excerpt that MUST explicitly mention the key term/concept being tested (students need to verify the answer)"
    }
  ]
}
"""

def get_question_generation_prompt(pages_content: dict, num_questions: int = 5, topic: str = None, learning_objectives: str = None) -> str:
    """
    Generate the user prompt for question generation.
    
    Args:
        pages_content: Dictionary mapping page numbers to text content
        num_questions: Number of questions to generate
        topic: Optional topic filter
        learning_objectives: Optional learning objectives to address
    
    Returns:
        Formatted prompt string
    """
    # Build the course material section
    material_text = "COURSE MATERIAL:\n\n"
    for page_num, content in pages_content.items():
        material_text += f"=== PAGE {page_num} ===\n{content}\n\n"
    
    # Build the request section
    topic_instruction = f" focusing on the topic: {topic}" if topic else ""
    
    # Add learning objectives if provided
    objectives_instruction = ""
    if learning_objectives and learning_objectives.strip():
        objectives_instruction = f"""
LEARNING OBJECTIVES COVERED IN THIS COURSE:
{learning_objectives}

⚠️ CRITICAL INSTRUCTION - READ CAREFULLY:
The questions MUST test whether students can APPLY and DEMONSTRATE these competencies through:
- Practical scenarios and case studies
- Problem-solving in realistic contexts
- Comparing and contrasting different approaches
- Making decisions based on constraints
- Analyzing trade-offs

❌ FORBIDDEN - DO NOT create questions that:
- Ask "What is one of the learning objectives?"
- Ask "What does the course aim to teach?"
- Simply restate the learning objective as the correct answer
- Have the learning objective text verbatim in the answer options

✅ REQUIRED - Questions must:
- Present a realistic scenario or problem
- Require application of the learned concepts
- Test understanding through decision-making or analysis
- Have answer options that require conceptual understanding, not memorization

EXAMPLES:

Bad: "What is one of the main learning outcomes about Chain-of-Thought prompting?"
Answer: "You can apply zero-shot and few-shot Chain-of-Thought prompting techniques" ❌

Good: "You need to solve a complex math word problem with an LLM. The model struggles with direct answers. Which technique would be most effective?"
Answer: "Provide 2-3 examples showing step-by-step reasoning (few-shot CoT)" ✅

Bad: "What does the COMPRESS strategy aim to achieve?"
Answer: "Reduce token usage while preserving essential information" ❌

Good: "Your application has a 4000-token limit but needs to process 10,000 tokens of context. Which strategy would be most appropriate?"
Answer: "Use COMPRESS to summarize context while retaining key information" ✅

Bad: "What is a limitation of Chain-of-Thought prompting?"
Answer: "It can generate plausible but incorrect reasoning" ❌

Good: "After implementing Chain-of-Thought prompting, you notice the LLM produces well-structured reasoning that leads to wrong conclusions. What does this demonstrate?"
Answer: "CoT can generate convincing but incorrect reasoning paths" ✅

QUESTION STYLE GUIDELINES:
- Prefer scenario-based questions that test application of concepts
- Use real-world situations relevant to the course material
- Ask "Which approach would be most effective?" rather than "What is the definition of...?"
- Test decision-making and problem-solving, not just recall
- When definitions are necessary, test deep conceptual understanding, not memorization

The questions should feel like they're testing whether someone could actually USE this knowledge in practice, not just whether they read the material.
"""
    
    request_text = f"""
TASK:
Generate exactly {num_questions} multiple-choice exam questions{topic_instruction}.
{objectives_instruction}

Requirements for each question:
- 4 options (A, B, C, D)
- Only one correct answer
- Question must be answerable using ONLY the material above
- Include the source page number
- CRITICAL - Source excerpt requirements:
  * Must be a direct, continuous passage from the material (not a list or fragments)
  * Must EXPLICITLY name the correct answer (if testing "WRITE strategy", the words "WRITE strategy" must appear)
  * Must show WHY this is the correct answer (include the definition, use case, or key characteristic)
  * Format: "The [correct answer] is/does [explanation that connects to the question]"
  * Students should think: "I can see [correct answer] mentioned here and understand why it's correct"
  * If the question asks for a SPECIFIC EXAMPLE or APPLICATION, the excerpt should contain that example or a clear description that matches it
  * The excerpt MUST contain the EXACT mechanism mentioned in the answer
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