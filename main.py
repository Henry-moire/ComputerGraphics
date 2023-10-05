from functions import *

dataset = import_dataset()
group_language(dataset)
filter_jsonl_by_column('amazon-massive-dataset/data/en-US.jsonl', 'english-test.jsonl', 'partition', 'test')
train_set(dataset)