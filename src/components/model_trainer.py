import sys
from typing import Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging

from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainingConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainigArtifact, ClassificationArtifact
from src.entity.estimator import MyModel


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainingConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train:np.array, test:np.array) -> Tuple[object, object]:

        try:
            logging.info("Training RandomForestClassifier with specified parameters")

            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            logging.info("Train-Test splitting done")

            model = RandomForestClassifier(
                n_estimators = self.model_trainer_config._n_estimators,
                min_samples_split = self.model_trainer_config._min_samples_split,
                min_samples_leaf = self.model_trainer_config._min_samples_leaf,
                max_depth = self.model_trainer_config._max_depth,
                criterion = self.model_trainer_config._criterion,
                random_state = self.model_trainer_config._random_state
            )

            # Model fitting
            logging.info("Model Training statrted")
            model.fit(x_train, y_train)
            logging.info("Model training done")

            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            metric_artifact = ClassificationArtifact(f1_score=f1, precision_score=precision, recall_score=recall)

            save_object(self.model_trainer_config.train_model_performance_path, metric_artifact)
            save_object(self.model_trainer_config.train_model_file_path, model)

            return metric_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def initiate_model_triaining(self) -> ModelTrainigArtifact:
            
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.tranformed_train_data_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.tranformed_test_data_file_path)
            logging.info("train-test data loaded")

            metric_artifact = self.get_model_object_and_report(train_arr, test_arr)
            logging.info("Model object and artifact loaded")

            model_trainer_artifact = ModelTrainigArtifact(
                train_model_file_path=self.model_trainer_config.train_model_file_path,
                metric_artifact=metric_artifact
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys) from e
