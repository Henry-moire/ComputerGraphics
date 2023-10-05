import json
import pandas as pd
import glob
import jsonlines

'''
Function to import the dataset
'''
def import_dataset():
    json_files = ""
    '''
    File path containing the directory all the JSONL files
    '''
    jsonl_files = glob.glob('amazon-massive-dataset/data/*.jsonl')
    return jsonl_files

'''
Function to generate a spreadsheet grouped by language
'''
def group_language(data_files):
    '''
    Initializing an empty list to store data from data folder
    '''
    data = []
    '''
    This function takes a list of JSONL file paths as input and loads them into a dataframe a dataframe
    '''
    for jsonl_file in data_files:
        with open(jsonl_file, 'r', encoding='utf-8') as file:
            for line in file:
                record = json.loads(line)
                data.append(record)
    
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
    
    excel_writer._save()
    print('Excel file generated successfully.')

'''
Function to filter a JSONL file by a specific value in a column and write the filtered data to a new JSONL file
'''

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

