import json 
import re
import copy
import math

import math
import re

def clean_data(value):
    # Convert to lower case first
    value = value.lower()

    # Normalize variations of "inch"
    inch_pattern = r'["\'”]|inches?|\binch\b|\binches\b'
    value = re.sub(inch_pattern, 'inch', value)

    # Normalize variations of "hertz"
    hertz_pattern = r'\bh[zZ]\b|\bhertz\b'
    value = re.sub(hertz_pattern, 'hz', value)
    
    # Function to remove non-alphanumeric tokens and spaces before units
    def clean_unit(match):
        unit = match.group(0)
        return re.sub(r'^[\s\W]+', '', unit)

    # Apply the cleaning function to each instance of "inch" or "hz"
    value = re.sub(r'[\s\W]*(inch|hz)\b', clean_unit, value)

    return value


def clean_tv_data(file_path, output_file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create a deep copy of the original data
    data_cleaned = copy.deepcopy(data)

    for model_id, list_tvs in data_cleaned.items():
        for tv in list_tvs:
            if 'featuresMap' in tv:
                for feature, v in tv['featuresMap'].items():
                    cleaned_val = clean_data(v)
                    tv['featuresMap'][feature] = cleaned_val
            if 'title' in tv:
                tv['title'] = clean_data(tv['title'])

    # Save the cleaned data to a new JSON file
    with open(output_file_path, 'w') as file:
        json.dump(data_cleaned, file, indent=4)
