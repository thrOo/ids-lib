import math
from ids_lib.metrics.metrics import AnomalyDetectionMetrics


class CacheableMetric:
    metric_functions = set()

    @staticmethod
    def cacheable_metric(f):
        CacheableMetric.metric_functions.add(f)
        return f


class CacheData:
    def __init__(self, data):
        if isinstance(data, AnomalyDetectionMetrics):
            self.data = data
        else:
            raise TypeError

    @CacheableMetric.cacheable_metric
    def dp_total_count(self):
        self.dp_total_count = len(self.data.anomalous_data_points) + len(self.data.normal_data_points)

    @CacheableMetric.cacheable_metric
    def dp_total_count_unique(self):
        self.dp_total_count_unique = len(set([x[0] for x in self.data.anomalous_data_points + self.data.normal_data_points]))

    @CacheableMetric.cacheable_metric
    def dp_total_count_normal(self):
        self.dp_total_count_normal = len(self.data.normal_data_points)

    @CacheableMetric.cacheable_metric
    def dp_total_count_anomalous(self):
        self.dp_total_count_anomalous = len(self.data.anomalous_data_points)

    @CacheableMetric.cacheable_metric
    def dp_total_count_normal_unique(self):
        self.dp_total_count_normal_unique = len(set([x[0] for x in self.data.normal_data_points]))

    @CacheableMetric.cacheable_metric
    def dp_total_count_anomalous_unique(self):
        self.dp_total_count_anomalous_unique = len(set([x[0] for x in self.data.anomalous_data_points]))

    @CacheableMetric.cacheable_metric
    def unique_dp(self):
        self.unique_dp = [
            ",".join(x)
            for x in
            set([x[0] for x in self.data.anomalous_data_points + self.data.normal_data_points])
        ]

    @CacheableMetric.cacheable_metric
    def false_alarms_total_count(self):
        self.false_alarms_total_count = len([x for x in self.data.normal_data_points if not x[1]])

    @CacheableMetric.cacheable_metric
    def anomaly_detected(self):
        self.anomaly_detected = self.data.map_anomalous_input_to_detected()

    @CacheableMetric.cacheable_metric
    def false_alarm_rate(self):
        self.false_alarms_rate = len([x for x in self.data.normal_data_points if not x[1]]) / len(self.data.normal_data_points)

    @CacheableMetric.cacheable_metric
    def detection_rate(self):
        self.detection_rate = len([x for x in self.data.anomalous_data_points if not x[1]]) / len(self.data.anomalous_data_points)

    def calculate_metrics(self):
        for f in CacheableMetric.metric_functions:
            f(self)
        del self.data

    def __repr__(self):
        return 'such data object'
