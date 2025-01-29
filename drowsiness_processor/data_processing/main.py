from drowsiness_processor.data_processing.processors.face_processor import FaceProcessor
from drowsiness_processor.data_processing.eyes.eyes_processor import EyesProcessor
from drowsiness_processor.data_processing.head.head_processor import HeadProcessor
from drowsiness_processor.data_processing.mouth.mouth_processor import MouthProcessor


class PointsProcessing:
    def __init__(self):
        self.face_processors: dict[str, FaceProcessor] = {
            'eyes': EyesProcessor(),
            'head': HeadProcessor(),
            'mouth': MouthProcessor()
        }
        self.hands_processors: dict = {}
        self.processed_points: dict = {}

    def main(self, points: dict):
        self.processed_points = {}
        self.processed_points['eyes'] = self.face_processors['eyes'].process(points.get('eyes', {}))
        self.processed_points['head'] = self.face_processors['head'].process(points.get('head', {}))
        self.processed_points['mouth'] = self.face_processors['mouth'].process(points.get('mouth', {}))

        return self.processed_points
