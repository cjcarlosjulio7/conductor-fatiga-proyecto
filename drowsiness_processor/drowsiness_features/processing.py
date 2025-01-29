from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor
from drowsiness_processor.drowsiness_features.flicker_and_microsleep.processing import FlickerEstimator
from drowsiness_processor.drowsiness_features.pitch.processing import PitchEstimator
from drowsiness_processor.drowsiness_features.yawn.processing import YawnEstimator


class FeaturesDrowsinessProcessing:
    def __init__(self):
        self.features_drowsiness: dict[str, DrowsinessProcessor] = {
            'flicker_and_micro_sleep': FlickerEstimator(),
            'pitch': PitchEstimator(),
            'yawn': YawnEstimator(),
        }
        self.processed_feature: dict = {
            'flicker_and_micro_sleep': None,
            'pitch': None,
            'yawn': None
        }

    def main(self, distances: dict):
        self.processed_feature['flicker_and_micro_sleep'] = (self.features_drowsiness['flicker_and_micro_sleep'].process
                                                             (distances.get('eyes', {})))
        self.processed_feature['pitch'] = self.features_drowsiness['pitch'].process(distances.get('head', {}))
        self.processed_feature['yawn'] = self.features_drowsiness['yawn'].process(distances.get('mouth', {}))
        return self.processed_feature
