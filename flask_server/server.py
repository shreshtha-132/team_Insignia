from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import pandas as pd
import os

app = Flask(__name__)

# Function to convert image to text using OCR
def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='eng')
    return text

# Function to split text by commas
def split_text_by_comma(text):
    return [segment.strip() for segment in text.split(',')]

# Function to load CSV and extract the 'Ingredients' column
def load_csv_to_dataframe(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

# Function to extract the 'Ingredient' and 'Health Concerns' columns
def extract_columns(df):
    if 'Ingredient' in df.columns and 'Health Concerns' in df.columns:
        return df[['Ingredient', 'Health Concerns']]
    else:
        return None

# Function to check for presence of ingredients in text segments
def check_ingredients_and_extract_health_concerns(text_segments, ingredient_df):
    found_ingredients_health = {}
    for _, row in ingredient_df.iterrows():
        ingredient = row['Ingredient']
        for segment in text_segments:
            if pd.notna(ingredient) and ingredient.lower() in segment.lower():
                found_ingredients_health[ingredient] = row['Health Concerns']
                break
    return found_ingredients_health

# Endpoint for image processing
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_path = os.path.join('temp', image_file.filename)
    image_file.save(image_path)
    
    # Extract text from image
    extracted_text = image_to_text(image_path)
    text_segments = split_text_by_comma(extracted_text)
    
    # Load the CSV file
    csv_file_path = 'expanded_harmful_ingredients_dataset.csv'
    dataframe = load_csv_to_dataframe(csv_file_path)
    if dataframe is not None:
        ingredient_df = extract_columns(dataframe)
        if ingredient_df is not None:
            # Check ingredients
            matching_ingredients_health = check_ingredients_and_extract_health_concerns(text_segments, ingredient_df)
            return jsonify(matching_ingredients_health)
    
    return jsonify({"error": "Failed to process image"}), 500

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True)
