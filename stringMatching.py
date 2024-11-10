from PIL import Image
import pytesseract
import pandas as pd

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
    """
    Check for the presence of each ingredient in 'Ingredient' column within each text segment
    and retrieve the corresponding 'Health concerns' for the matched ingredient.

    Parameters:
    text_segments (list of str): List containing text segments extracted from the image.
    ingredient_df (DataFrame): DataFrame containing ingredients and health concerns.

    Returns:
    dict: Dictionary where keys are found ingredients and values are the corresponding health concerns.
    """
    found_ingredients_health = {}

    for _, row in ingredient_df.iterrows():
        ingredient = row['Ingredient']
        for segment in text_segments:
            if pd.notna(ingredient) and ingredient.lower() in segment.lower():
                found_ingredients_health[ingredient] = row['Health Concerns']
                break  # Stop checking further segments for this ingredient

    return found_ingredients_health

# Paths for the image and CSV file
image_path = 'images/pop.jpg'
csv_file_path = 'expanded_harmful_ingredients_dataset.csv'

# Process the image
extracted_text = image_to_text(image_path)
text_segments = split_text_by_comma(extracted_text)
print("Extracted Text Segments:", text_segments)

# Load the CSV and extract ingredients and health concerns columns
dataframe = load_csv_to_dataframe(csv_file_path)
if dataframe is not None:
    ingredient_df = extract_columns(dataframe)
    
    # Check if any ingredients are present in the text segments and get corresponding health concerns
    if ingredient_df is not None:
        matching_ingredients_health = check_ingredients_and_extract_health_concerns(text_segments, ingredient_df)
        print("Matching Ingredients and Corresponding Health Concerns:")
        for ingredient, health_concern in matching_ingredients_health.items():
            print(f"Ingredient: {ingredient}")
            print(f"Health Concern: {health_concern}")
        
        # Calculate the comparison factor
        num_text_segments = len(text_segments)
        num_matched_ingredients = len(matching_ingredients_health)
        if num_text_segments > 0:
            comparison_factor = (num_matched_ingredients / num_text_segments) * 100
            print(f"Comparison Factor: {comparison_factor:.2f}%")
        else:
            print("No text segments found to compare.")
