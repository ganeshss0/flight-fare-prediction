# Importing namedtuple
from collections import namedtuple


DataTransformationConfig = namedtuple(
    'DataTransformationConfig',
    [
        'add_bedroom_per_room',
        'transformed_train_dir',
        'transformed_test_dir',
        'preprocessed_object_file_path'
    ]
)

