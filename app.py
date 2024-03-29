import os
from dotenv import load_dotenv
import openai
from flask import escape, Flask, redirect, render_template, request, url_for, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
# logging
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Load environment variables from the .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OPENAI_API_KEY is not set.")
    api_key_error = "API key is missing. Please provide the OpenAI API key under the advanced settings in the AdaLab App Deployment menu."
else:
    api_key_error = None
    openai.api_key = openai_api_key

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if api_key_error:
        return render_template("index.html", error=api_key_error)

    if request.method == "POST":
        question = request.form["question"]
        long_answer = request.form.get("long_answer")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=generate_prompt(question, long_answer),
            temperature=0.6,
            max_tokens=250,
        )
        generated_text = response.choices[0].text

        logging.info("Q: %s | A: %s", generate_prompt(question, long_answer), generated_text)

        return jsonify(result=escape(generated_text))

    result = request.args.get("result")
    return render_template("index.html", result=result, error=None)


def generate_prompt(question, long_answer):
    prompt_type = "short" if long_answer != "on" else "long"
    return f"""Answer the following question with a {prompt_type} answer:
question: {question.capitalize()}
Answer:"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
