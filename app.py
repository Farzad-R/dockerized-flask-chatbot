from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/DialoGPT-medium", padding_side='left')
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
conversations = []


def filter_response(prompt, response):
    sentences = response.split(".")
    filtered_sentences = [s.strip()
                          for s in sentences if prompt.lower() in s.lower()]
    filtered_sentences = sorted(filtered_sentences, key=len, reverse=True)
    if len(filtered_sentences) == 0:
        return response
    return filtered_sentences[0]


def generate_response(prompt, max_length=100, temperature=0.7, top_k=50, num_return_sequences=3):
    input_ids = tokenizer.encode(
        prompt + tokenizer.eos_token, return_tensors="pt")
    output = model.generate(
        input_ids=input_ids,
        max_length=max_length + len(input_ids[0]),
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        repetition_penalty=1.5,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=num_return_sequences
    )
    responses = [tokenizer.decode(o, skip_special_tokens=True) for o in output]
    filtered_responses = [filter_response(prompt, r) for r in responses]
    # Remove the prompt from the filtered responses
    filtered_responses = [r.replace(prompt, "").strip()
                          for r in filtered_responses]
    return filtered_responses


@app.route("/")
def index():
    return render_template("index.html", conversations=conversations)


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    response = generate_response(user_input)[0]

    # Store the prompt and response in the conversations list
    conversations.append((user_input, response))

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run()
