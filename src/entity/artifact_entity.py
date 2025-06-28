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
    transformed_object_file_path: str
    tranformed_train_data_file_path: str
    tranformed_test_data_file_path: str

@dataclass
class ClassificationArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass 
class ModelTrainigArtifact:
    train_model_file_path: str
    metric_artifact: ClassificationArtifact


    