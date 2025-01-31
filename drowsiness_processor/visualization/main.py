import numpy as np
import cv2
import time
import threading
import pygame
from typing import Tuple

class ReportVisualizer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.coordinates = {
            'flicker': (10, 180),
            'micro_sleep': (10, 260),
            'pitch': (10, 340),
            'yawn': (10, 420),
        }
        self.visualize_reports = {
            'flicker': {'report': False, 'count': 0, 'processed': False},
            'micro_sleep': {'report': False, 'count': 0, 'processed': False},
            'pitch': {'report': False, 'count': 0, 'processed': False},
            'yawn': {'report': False, 'count': 0, 'processed': False}
        }
        self.sounds = {
            'micro_sleep': pygame.mixer.Sound("resources/sounds/micro_sleep.mp3"),
            'yawn': pygame.mixer.Sound("resources/sounds/yawn.mp3"),
        }

    def play_sound(self, feature: str):
        """Reproduce un sonido usando pygame en un hilo separado."""
        def sound_worker():
            try:
                self.sounds[feature].play()
            except Exception as e:
                print(f"Error reproduciendo sonido para {feature}: {e}")

        threading.Thread(target=sound_worker, daemon=True).start()

    def update_report(self, feature: str, data: dict):
        base_feature = feature.replace('_first_hand', '').replace('_second_hand', '')
        report = data[f'{base_feature}_report']

        if report:
            counter = data[f'{base_feature}_count']
            self.visualize_reports[feature]['report'] = report
            self.visualize_reports[feature]['count'] = counter
        else:
            # Reset processed state if the event is no longer active
            self.visualize_reports[feature]['report'] = False
            self.visualize_reports[feature]['processed'] = False

    def visualize_all_reports(self, sketch: np.ndarray, report_data: dict):
        # flicker
        self.update_report('flicker', report_data['flicker_and_micro_sleep'])

        # micro sleep
        self.update_report('micro_sleep', report_data['flicker_and_micro_sleep'])
        if self.visualize_reports['micro_sleep']['report']:
            if not self.visualize_reports['micro_sleep']['processed']:
                self.play_sound('micro_sleep')
                self.visualize_reports['micro_sleep']['processed'] = True

        # pitch
        self.update_report('pitch', report_data['pitch'])

        # yawn
        self.update_report('yawn', report_data['yawn'])
        if self.visualize_reports['yawn']['report']:
            if not self.visualize_reports['yawn']['processed']:
                self.play_sound('yawn')
                self.visualize_reports['yawn']['processed'] = True

        return sketch  # Devuelve la imagen sin texto.
