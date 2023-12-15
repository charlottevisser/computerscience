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

    def process_inch_diag(match):
        def normal_round(n):
            if n - math.floor(n) < 0.5:
                return math.floor(n)
            return math.ceil(n)
        
        num = match.group(1)
        
        # Case 1: Two digits - do nothing
        if len(num) == 2 and num.isdigit():
            return num + 'inch '

        # Case 4: Interpret numbers like 49910 as 49+9/10
        elif len(num) == 5 and num.isdigit():
            first_part = int(num[:2])
            second_part = int(num[2:3]) / int(num[3:])
            number = first_part + second_part
            rounded = normal_round(number)
            return str(rounded) + 'inch '

        elif len(num) == 6 and num.isdigit():
            first_part = int(num[:2])
            second_part = int(num[2:4]) / int(num[4:])
            number = first_part + second_part
            rounded = normal_round(number)
            return str(rounded) + 'inch '

        # Case 3: Interpret numbers like 2812, 2912, 3558
        elif len(num) > 2 and num.isdigit():
            first_part = int(num[:-2])
            second_part = int(num[-2:-1]) / int(num[-1:])
            number = first_part + second_part
            rounded = normal_round(number)
            return str(rounded) + 'inch '

        # Case 2: Decimal numbers - round to nearest integer
        else:
            rounded = normal_round(float(num))
            return str(rounded) + 'inch '

    # Apply processing for inch diag values
    value = re.sub(r'(\d+\.?\d*)inch ', process_inch_diag, value)

    return value

def clean_data_title_specific(value):
    # Convert to lower case first
    
    list_brands = ['newegg.com - ', ' - best buy', ' - thenerds.net']
    brands_pattern = r'\b' + r'\b|\b'.join(map(re.escape, list_brands)) + r'\b'

    # Remove the website names
    value = re.sub(brands_pattern, '', value)

    value = re.sub(r'[()]', '', value)
    return value

# 

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
                tv['title'] = clean_data_title_specific(tv['title'])

    # Save the cleaned data to a new JSON file
    with open(output_file_path, 'w') as file:
        json.dump(data_cleaned, file, indent=4)
