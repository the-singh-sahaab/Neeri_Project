import spacy
from sentence_transformers import SentenceTransformer, util
import json

# Load spaCy model and SentenceTransformer model
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load expertise data from the JSON file
with open('expertise.json', 'r') as json_file:
    expertise_data = json.load(json_file)


def find_similar_expertise(input_expertise, json_file = expertise_data, threshold=0.5):
    # Create a list to store similar expertise in the same category
    similar_expertise_in_category = []

    # Process input expertise with spaCy
    input_doc = nlp(input_expertise)

    # Iterate through expertise categories in the JSON data
    for category in expertise_data.get("expertise", []):
        category_name = category.get("name", "")
        expertise_list = category.get("subOptions", [])

        # Calculate similarity between input expertise and each expertise in the category
        similarities = util.pytorch_cos_sim(
            model.encode([input_expertise], convert_to_tensor=True),
            model.encode(expertise_list, convert_to_tensor=True)
        )[0]

        # Filter results below the threshold
        filtered_results = [(expertise_list[i], similarities[i].item()) for i in range(len(expertise_list)) if similarities[i].item() > threshold]

        # Add the filtered results to the list
        similar_expertise_in_category.extend([{
            'Category': category_name,
            'Expertise': expertise,
            'Similarity': similarity
        } for expertise, similarity in filtered_results])

    # Sort the list by similarity (higher similarity first)
    similar_expertise_in_category.sort(key=lambda x: x['Similarity'], reverse=True)

    return similar_expertise_in_category
