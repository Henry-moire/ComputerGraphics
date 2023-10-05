import json
import pandas as pd
import glob
import logging


"""Create a file for logging"""
logging.basicConfig(filename = "logfile.log", format = '%(asctime)s %(message)s', filemode = 'w')

""" Create logger object"""
logger = logging.getLogger()

""" Setting the threshold of logger to DEBUG"""
logger.setLevel(logging.DEBUG)


"""
Function to import the dataset
"""
def import_dataset():

    """
    File path containing the directory all the JSONL files
    """
    jsonl_files = glob.glob('amazon-massive-dataset/data/*.jsonl')

    logging.info("Successfully imported the dataset")
    return jsonl_files

"""
Function to generate a spreadsheet grouped by language
"""
def group_language(data_files):
    """
    Args:
        data_files: The variable containing the jsonl files.
    """
    """
    Initializing an empty list to store data from data folder
    """
    data = []


    """ This function takes a list of JSONL file paths as input and loads them into a dataframe a dataframe"""
    for jsonl_file in data_files:
        with open(jsonl_file, 'r', encoding='utf-8') as file:
            for line in file:
                record = json.loads(line)
                data.append(record)
    
    df = pd.DataFrame(data)
    """
    Create an Excel writer object to save the data to an Excel file
   """
    excel_writer = pd.ExcelWriter('en-xx.xlsx', engine='openpyxl')
    """
    Group the data by 'locale' and iterate over each language
    """
    for lang, lang_df in df.groupby('locale'):
        
        """ Save the data to the Excel sheet named with the language code """
        
        lang_df[['id', 'utt', 'annot_utt']].to_excel(excel_writer, sheet_name=lang, index=False)
    
    excel_writer._save()
    logging.info("Excel file generated successfully.")

"""
Function to filter a JSONL file by a specific value in a column and write the filtered data to a new JSONL file
"""
def filter_jsonl_by_column(input_file, output_file, filter_column, filter_value):
    """
    Args:
        input_file: The path to the input JSONL file.
        output_file: The path to the output JSONL file.
        filter_column: The name of the column to filter by.
        filter_value: The value to filter for in the specified column.
    """
    filtered_data = []

    with open(input_file, "r") as infile:
        for line in infile:
            try:
                json_obj = json.loads(line)
                if filter_column in json_obj and json_obj[filter_column] == filter_value:
                    filtered_data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON: {e}")

    with open(output_file, "w") as outfile:
        for data in filtered_data:
            outfile.write(json.dumps(data) + "\n")
    
    logging.info("Successfully created filtered json file.")

"""
Function to generate one large json file showing all the translations from en to xx with id 
and utt for all the train sets
"""
def train_set(dataset):
    """
    Args:
        dataset: The variable containing the jsonl files.
    """
    filtered_data = []
    for jsonl_file in dataset:
            with open(jsonl_file, 'r', encoding='utf-8') as file:
                for line in file:
                    record = json.loads(line)
                    if 'partition' in record and record['partition'] == 'train':
                        filtered_data.append(record)
    with open('train-set.jsonl', "w") as outfile:
            for data in filtered_data:
                outfile.write(json.dumps(data) + "\n")
    logging.info("Train set saved to jsonl file.")

    # Define the columns you want to extract
    columns_to_extract = ['id', 'utt']

    # Open the input and output files
    with open('train-set.jsonl', 'r') as input_file, open('filtered-train-set.jsonl', 'w') as output_file:
        # Iterate through each line in the input file
        for line in input_file:
            try:
                # Parse the line as JSON
                data = json.loads(line)

                # Create a new dictionary with only the specified columns
                extracted_data = {key: data[key] for key in columns_to_extract}

                # Convert the extracted data back to JSON and write to the output file
                output_file.write(json.dumps(extracted_data) + '\n')
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")
    logging.info("Train set successfully filtered.")

    # Open the input JSONL file for reading and the output JSONL file for writing
    with open('filtered-train-set.jsonl', 'r') as input_file, open('pretty-train-set.jsonl', 'w') as output_file:
        for line in input_file:
            try:
                # Parse each line as a JSON object
                data = json.loads(line)

                # Pretty-print the JSON data with an indentation of 4 spaces
                pretty_json = json.dumps(data, indent=4)

                # Write the pretty-printed JSON to the output file with a newline character
                output_file.write(pretty_json + '\n')
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")

    logging.info("Pretty-printed JSONL data saved to: pretty-train-set.jsonl.")
