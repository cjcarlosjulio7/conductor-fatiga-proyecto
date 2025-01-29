import numpy as np
from typing import Tuple
import logging as log
from drowsiness_processor.extract_points.face_mesh.face_mesh_processor import FaceMeshProcessor

log.basicConfig(level=log.INFO)
logger = log.getLogger(__name__)


class PointsExtractor:
    def __init__(self):
        self.face_mesh = FaceMeshProcessor()

    def process(self, face_image: np.ndarray) -> Tuple[dict, bool, np.ndarray]:
        face_points, mesh_success, draw_sketch = self.face_mesh.process(face_image, draw=True)
        if mesh_success:
            return face_points, True, draw_sketch
        else:
            return face_points, False, draw_sketch

