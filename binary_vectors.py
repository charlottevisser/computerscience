import re
import numpy as np


def get_model_words_titles(title):
    model_words_title = []
    pattern = r'([a-zA-Z0-9]*(([0-9]+[^0-9, ]+)|([^0-9, ]+[0-9]+))[a-zA-Z0-9]*)'
    regex = re.compile(pattern)
    
    matches = regex.findall(title)
    
    for match in matches:
        model_words_title.append(match[0])

    return model_words_title

def get_unique_model_words(titles_list):
    all_model_words_title = []
    for title in titles_list:
        model_words = get_model_words_titles(title)
        all_model_words_title.extend(model_words)
    return list(set(all_model_words_title))




def get_model_words_values(value):
    model_words_keyvalue = []
    pattern = r'(^\d+(\.\d+)?[a-zA-Z]*$|^\d+(\.\d+)?$)'

    regex = re.compile(pattern)
    matches = regex.findall(value)
    
    for match in matches:
        numeric_part = re.match(r'^\d+(\.\d+)?', match[0])
        if numeric_part:
            model_words_keyvalue.append(numeric_part.group())

    return model_words_keyvalue

def get_unique_model_words_features(features_list):
    all_model_words_feature = []
    for feature in features_list:
        model_words = get_model_words_values(feature)
        all_model_words_feature.extend(model_words)
    return list(set(all_model_words_feature))


import numpy as np

def obtain_binary_matrix(products_subset):
    titles_list = [product['title'] for product in products_subset]
    unique_model_words_title = set(get_unique_model_words(titles_list))

    features_values = [value for product in products_subset for value in product.get('featuresMap', {}).values()]
    unique_model_words_features = set(get_unique_model_words_features(features_values))

    all_mw = set(unique_model_words_title.union(unique_model_words_features))
    
    binary_matrix = np.zeros((len(all_mw), len(products_subset)), dtype=int)

    for product_index, product in enumerate(products_subset):
        title = product['title']
        features_values = product.get('featuresMap', {}).values()

        for mw_index, mw in enumerate(all_mw):
            if (mw in (unique_model_words_title or unique_model_words_features) and mw in features_values) or \
                (mw in (unique_model_words_title) and mw in title):
                binary_matrix[mw_index][product_index] = 1
    return binary_matrix

