from flask import Flask, render_template, request
import os
import google.generativeai as genai
import re

# Set your Gemini API key directly or use an environment variable
genai.configure(api_key="AIzaSyAXBCmmMROUFCP-UeZi_hjo7O_mtEqQHeA")

# Initialize Flask app
app = Flask(__name__)

# Example usage with chat completion
model = genai.GenerativeModel('gemini-pro')

# Define the startup viability assessment function
def assess_startup_viability(business_idea, sector, target_market, competition, uniqueness, revenue_model):
    # Construct the prompt for the Gemini model
    prompt = f"""
    Assess the viability of the following startup based on the provided inputs:

    Business Idea: {business_idea}
    Sector: {sector}
    Target Market: {target_market}
    Competition: {competition}
    Product Uniqueness: {uniqueness}
    Revenue Model: {revenue_model}

    Provide a viability score and analysis.
    """

    try:
        # Use Gemini API to generate the analysis
        response = model.generate_content(prompt)

        # Extract the response text
        result = response.text.strip()

         # Extract the viability score from the response (e.g., "3/5" or "3 out of 5")
        match = re.search(r"(\d+)\s*(?:\/|out of)\s*(\d+)", result)  # Matches '3/5' or '3 out of 5'
        if match:
            viability_score = int(match.group(1))  # The score value (numerator)
            max_score = int(match.group(2))  # The max score value (denominator)
        else:
            viability_score = 0  # Default if no score found
            max_score = 1  # To prevent division by zero

        # Calculate the percentage
        viability_percentage = (viability_score / max_score) * 100

        return result, viability_score, round(viability_percentage, 2)

    except Exception as e:
        return f"Error: {e}", 0, 0

# Define the route to display the form and process the input
@app.route('/', methods=['GET', 'POST'])
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        business_idea = request.form.get("business_idea")
        sector = request.form.get("sector")
        target_market = request.form.get("target_market")
        competition = request.form.get("competition")
        uniqueness = request.form.get("uniqueness")
        revenue_model = request.form.get("revenue_model")

        # Call the function with the user's inputs
        result_analysis, viability_score, viability_percentage = assess_startup_viability(
            business_idea, sector, target_market, competition, uniqueness, revenue_model
        )

        return render_template("index2.html", result=result_analysis, 
                               viability_score=viability_score, 
                               viability_percentage=viability_percentage)
    
    return render_template("index2.html", result=None, viability_score=None, viability_percentage=None)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
