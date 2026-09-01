import sys
import os
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from src.retrieval.retrieval import query_vector_db
from src.generation.generator import generate_study_material
import gradio as gr  # pyright: ignore[reportMissingImports]

current_quiz_data = {"questions": [], "answers": [], "explanations": []}

def handle_pipeline(student_query, action_type):
    """
    Processes search and LLM generation based on app interaction parameters."
    """
    blank_quiz_padding = [gr.update(visible=False) for _ in range(9)]

    if not student_query.strip():
        return "Please enter a valid textbook topic or query.". gr.update(visible=False), gr.update(visible=False), *blank_quiz_padding

    retrieved_chunks = query_vector_db(query=student_query, k=4)
    if not retrieved_chunks:
        return "No text fragments matching your request were found in the database store.", gr.update(visible=False), gr.update(visible=False), *blank_quiz_padding

    result = generate_study_material(chunks=retrieved_chunks, action_type=action_type)

    if action_type == "summary":
        if hasattr(result, "content"):
            result = result.content
        return result, gr.update(visible=False), gr.update(visible=False), *blank_quiz_padding

    elif action_type == "quiz":
        global current_quiz_data
        current_quiz_data["questions"] = result.questions


    question_updates = []
    for i in range(3):
        if i < len(result.questions):
            q = result.questions[i]
            question_updates.extend([
                gr.update(value=f"### Q{i+1}: {q.question}", visible=True),
                gr.update(choices=q.options, value=None, visible=True),
                gr.update(value="", visible=False)
            ])

    return "", gr.update(visible=True), gr.update(visible=True), *question_updates

def check_quiz_answers(*selected_options):
    """
    Evaluates user choices against stored correct strings and returns feedback.
    """
    outputs = []
    for i, choice in enumerate(selected_options):
        if i >= len(current_quiz_data["questions"]):
            break
        q = current_quiz_data["questions"][i]

        if choice == q.correct_answer:
            msg = f"✅ **Correct!** {q.explanation}"
        elif choice is None:
            msg = "⚠️ *Please select an answer choice for this question.*"
        else:
            msg = f"❌ **Incorrect.** The correct answer was: *{q.correct_answer}*.\n\n{q.explanation}"

        outputs.append(gr.update(value=msg, visible=True))
    return outputs



# --- GRADIO INTERFACE LAYOUT DEFINITION ---
with gr.Blocks(title="Textbook Study Buddy") as demo:
    gr.Markdown("# 🧑‍🎓 Personalized Textbook Study Buddy")
    gr.Markdown("Search across your indexed textbook vectors to generate customized study aids immediately.")
    
    with gr.Row():
        with gr.Column(scale=2):
            student_input = gr.Textbox(
                label="What section or topic are you reviewing today?",
                placeholder="e.g., Variable assignment, local variable scopes, list comprehensions...",
                lines=2
            )
            action_choice = gr.Radio(
                choices=["summary", "quiz"],
                value="summary",
                label="Select Output Format Pipeline Action"
            )
            submit_btn = gr.Button("Execute Pipeline Transformation", variant="primary")
            
        with gr.Column(scale=3):
            # Summary Output Display Element
            summary_output = gr.Markdown(label="Generated Chapter Summary Context")
            
            # Interactive Quiz Container Box
            with gr.Column(visible=False) as quiz_container:
                gr.Markdown("## 📝 Concept Check Evaluation")
                
                # Question UI Rows (Supports up to 3 questions max for this configuration)
                q1_text = gr.Markdown(visible=False)
                q1_choices = gr.Radio(show_label=False, visible=False)
                q1_feedback = gr.Markdown(visible=False)
                
                q2_text = gr.Markdown(visible=False)
                q2_choices = gr.Radio(show_label=False, visible=False)
                q2_feedback = gr.Markdown(visible=False)
                
                q3_text = gr.Markdown(visible=False)
                q3_choices = gr.Radio(show_label=False, visible=False)
                q3_feedback = gr.Markdown(visible=False)
                
                check_btn = gr.Button("Grade My Answers", variant="secondary", visible=False)

    # Wire up pipeline engine trigger
    quiz_components = [q1_text, q1_choices, q1_feedback, q2_text, q2_choices, q2_feedback, q3_text, q3_choices, q3_feedback]
    submit_btn.click(
        fn=handle_pipeline,
        inputs=[student_input, action_choice],
        outputs=[summary_output, quiz_container, check_btn] + quiz_components
    )
    
    # Wire up quiz submission grading block
    check_btn.click(
        fn=check_quiz_answers,
        inputs=[q1_choices, q2_choices, q3_choices],
        outputs=[q1_feedback, q2_feedback, q3_feedback]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)




