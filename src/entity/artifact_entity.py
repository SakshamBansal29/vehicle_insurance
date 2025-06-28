from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    validation_report_file: str

@dataclass
class DataTransformationArtifact:
    tranformed_data_file_path: str
    tranformed_train_data_file_path: str
    tranformed_test_data_file_path: str


    