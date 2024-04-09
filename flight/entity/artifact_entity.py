from collections import namedtuple


DataTransformationArtifact = namedtuple(
    'DataTransformationArtifact',
    [
        'transformed_train_path',
        'transformed_test_path',
        'preprocessor_object_file_path',
        'is_transformed',
        'message'
    ]
)
