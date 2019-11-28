import numpy as np
from abc import abstractmethod


class AnomalyDetectionMetrics:
    @property
    def normal_data_points(self):
        raise NotImplementedError

    @property
    def anomalous_data_points(self):
        raise NotImplementedError

    @abstractmethod
    def map_anomalous_input_to_detected(self):
        pass

    def check_types(self):
        if not isinstance(self.anomalous_data_points, np.ndarray):
            raise TypeError
        if not isinstance(self.normal_data_points, np.ndarray):
            raise TypeError
        if not isinstance(self.anomalous_data_points, np.ndarray):
            raise TypeError

