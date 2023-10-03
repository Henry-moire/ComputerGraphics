import json
import pandas as pd
import glob
import jsonlines
import logging

#Create a file for logging
logging.basicConfig(filename = "logfile.log", format = '%(asctime)s %(message)s', filemode = 'w')

#Create logger object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

"""
Function to import the dataset
"""
def import_dataset():
    json_files = ""
    '''
    File path containing for the directory all the JSONL files
    '''
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
    '''
    Initializing an empty list to store data from data folder
    '''
    data = []
    '''
    Iterate over each JSONL file
    '''
    for jsonl_file in data_files:
        with open(jsonl_file, 'r', encoding='utf-8') as file:
            for line in file:
                record = json.loads(line)
                data.append(record)
    '''
    Create a DataFrame from the data
    '''
    df = pd.DataFrame(data)
    '''
    Create an Excel writer object to save the data to an Excel file
    '''
    excel_writer = pd.ExcelWriter('en-xx.xlsx', engine='openpyxl')
    '''
    Group the data by 'locale' and iterate over each language
    '''
    for lang, lang_df in df.groupby('locale'):
        '''
        Save the data to the Excel sheet named with the language code
        '''
        lang_df[['id', 'utt', 'annot_utt']].to_excel(excel_writer, sheet_name=lang, index=False)
    '''
    Save the Excel file
    '''
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