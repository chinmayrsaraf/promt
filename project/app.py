from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from transformers import pipeline
import re
import os

# Initialize Flask app
app = Flask(__name__)

# Create an uploads directory to save files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize the model for code optimization
print("Loading the model...")
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-Coder-1.5B-Instruct", device=-1)
print("Model loaded successfully!")

def optimize_code(input_code, language="Java", optimization_goal=None):
    """
    Optimizes the provided code based on the specified programming language and optimization goal.
    """
    if not optimization_goal:
        optimization_goal = (
            f"Optimize the following {language} code to reduce time complexity, "
            f"remove unnecessary steps, improve performance, reduce space, and minimize energy consumption. "
            f"Focus on eliminating redundant operations, using more efficient algorithms, and optimizing memory usage."
        )
    
    # Create the optimization prompt
    prompt = f"Optimize the following {language} code to {optimization_goal}. Return only the optimized code without any explanations or comments:\n\n{input_code}\n\nOptimized Code:\n"
    
    # Generate the optimized code
    response = pipe(prompt, max_new_tokens=300)
    generated_text = response[0]["generated_text"]

    # Extract only the optimized code
    match = re.search(r"Optimized Code:\s*(```" + language.lower() + r")?(.*?)(```|\Z|Explanation:|Additionally|This optimized code)", generated_text, re.DOTALL)
    optimized_code = match.group(2).strip() if match else generated_text.strip()

    return optimized_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    language = request.form.get('language', 'Java')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)
    
    # Read the uploaded file
    with open(file_path, 'r') as f:
        input_code = f.read()

    # Optimize the code
    optimized_code = optimize_code(input_code, language=language)

    # Append optimized code to the file
    with open(file_path, 'a') as f:
        f.write("\n\n// === Optimized Code ===\n")
        f.write(optimized_code)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
