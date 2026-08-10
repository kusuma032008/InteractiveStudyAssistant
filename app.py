import os
import gradio as gr
from google import genai

# Get Gemini API key from Render environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def study_assistant(topic, help_type, difficulty):

    if not topic.strip():
        return "Please enter a topic or question."

    prompt = f"""
You are an AI Interactive Study Assistant.

The student needs help with:

Topic / Question:
{topic}

Type of Help:
{help_type}

Difficulty Level:
{difficulty}

Provide a clear, accurate, and student-friendly response.

Instructions:
- Explain the concept in simple language.
- Organize the response using headings and bullet points where appropriate.
- Give examples when useful.
- Highlight important points.
- If the student asks for a concept explanation, explain it step by step.
- If the student asks for exam preparation, include important points to remember.
- Keep the response appropriate for the selected difficulty level.

Provide the study response now.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(title="Interactive Study Assistant") as app:

    gr.Markdown(
        """
        # 📚 Interactive Study Assistant

        ### Your AI-powered study companion

        Enter a topic or question and get personalized study help.
        """
    )

    topic = gr.Textbox(
        label="📖 Enter Topic or Question",
        placeholder="Example: Explain Object Oriented Programming in Python",
        lines=5
    )

    with gr.Row():

        help_type = gr.Dropdown(
            choices=[
                "Explain Concept",
                "Step-by-Step Explanation",
                "Exam Preparation",
                "Important Points",
                "Examples",
                "Quick Revision"
            ],
            value="Explain Concept",
            label="Type of Help"
        )

        difficulty = gr.Dropdown(
            choices=[
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            value="Beginner",
            label="Difficulty Level"
        )

    with gr.Row():

        study_button = gr.Button(
            "📚 Get Study Help",
            variant="primary"
        )

        clear_button = gr.Button(
            "🗑️ Clear"
        )

    output = gr.Markdown(
        label="Study Response"
    )

    study_button.click(
        fn=study_assistant,
        inputs=[
            topic,
            help_type,
            difficulty
        ],
        outputs=output
    )

    clear_button.click(
        fn=lambda: ("", "Explain Concept", "Beginner", ""),
        inputs=[],
        outputs=[
            topic,
            help_type,
            difficulty,
            output
        ]
    )


port = int(os.environ.get("PORT", 10000))

app.launch(
    server_name="0.0.0.0",
    server_port=port
)
