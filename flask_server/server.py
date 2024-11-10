from PIL import Image
import pytesseract
import pandas as pd
from io import BytesIO
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to convert image to text using OCR
def image_to_text(image_data):
    img = Image.open(BytesIO(image_data))  # Open image from the raw bytes
    text = pytesseract.image_to_string(img, lang='eng')
    return text

# Function to split text by commas
def split_text_by_comma(text):
    return [segment.strip() for segment in text.split(',')]

# Function to load CSV and extract the 'Ingredients' column
def load_csv_to_dataframe(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

# Function to extract the 'Ingredient' and 'Health Concerns' columns
def extract_columns(df):
    if 'Ingredient' in df.columns and 'Health Concerns' in df.columns:
        return df[['Ingredient', 'Health Concerns']]
    else:
        print("Columns 'Ingredient' and 'Health Concerns' not found in the DataFrame.")
        return None

# Function to check for presence of ingredients in text segments and retrieve corresponding health concerns
def check_ingredients_and_extract_health_concerns(text_segments, ingredient_df):
    found_ingredients_health = {}

    for _, row in ingredient_df.iterrows():
        ingredient = row['Ingredient']
        for segment in text_segments:
            if pd.notna(ingredient) and ingredient.lower() in segment.lower():
                found_ingredients_health[ingredient] = row['Health Concerns']
                break  # Stop checking further segments for this ingredient

    return found_ingredients_health

@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if the request contains an image
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    # Process the image
    image_data = image_file.read()  # Read the raw image data
    extracted_text = image_to_text(image_data)  # Pass the raw image data to the OCR function
    text_segments = split_text_by_comma(extracted_text)
    # Load CSV and extract ingredients and health concerns columns
    csv_file_path = 'expanded_harmful_ingredients_dataset.csv'
    dataframe = load_csv_to_dataframe(csv_file_path)
    
    if dataframe is not None:
        ingredient_df = extract_columns(dataframe)

        if ingredient_df is not None:
            matching_ingredients_health = check_ingredients_and_extract_health_concerns(text_segments, ingredient_df)

            # Calculate the comparison factor
            num_text_segments = len(text_segments)
            num_matched_ingredients = len(matching_ingredients_health)
            if num_text_segments > 0:
                comparison_factor = (num_matched_ingredients / num_text_segments) * 100
            else:
                comparison_factor = 0

            return jsonify({
                'matching_ingredients_health': matching_ingredients_health,
                'comparison_factor': comparison_factor
            })

    return jsonify({'error': 'Unable to process image'}), 500

if __name__ == '__main__':
    app.run(debug=True)
