from flet import *
import asyncio
import websockets
import json
import cv2
import numpy as np
import threading
import base64

from gui.resources.resources_path import (ImagePaths, FontsPath)


class Drowsiness:
    def __init__(self, page):
        self.page = page

        self.running = False
        self.video_thread = None
        self.sketch_image_control = None
        self.original_image_control = None

        self.stop_button = None
        self.start_button = None

        self.images = ImagePaths()
        self.fonts = FontsPath()

    def main(self):

        self.original_image_control = Image(
            width=290,
            height=340,
            fit=ImageFit.COVER,
            src_base64=self.get_placeholder_image()
        )

        self.start_button = ElevatedButton(
            text="Start",
            on_click=self.start_detection,
            bgcolor='#613bbb',
            color='#FFFFFF',
        )
        self.stop_button = ElevatedButton(
            text="Stop",
            on_click=self.stop_detection,
            bgcolor='#3f64c1',
            color='#FFFFFF',
        )

        self.camera_status_dot = Container(
            width=20,
            height=20,
            bgcolor="red",  # Color rojo
            border_radius=10,
            visible=False  # Inicialmente no visible
            
        )

        # Crear un contenedor de fila para el punto en la parte superior
        top_row = Row(
            controls=[self.camera_status_dot],  # Solo el punto rojo
            alignment="center",  # Centrado horizontalmente
            expand=True
        )

        left_column = Column(
            controls=[   
                top_row,  # Aquí añadimos la fila con el punto rojo
                Container(height=30),
                self.original_image_control,
            ],
            alignment='center',
            horizontal_alignment='center',
            expand=True
        )

        elements = Container(
            content=Row(
                controls=[
                    left_column,
                    self.start_button,
                    self.stop_button,
                ],
                alignment='spaceEvenly',
                vertical_alignment='center',
            ),
            bgcolor="#000000",
            padding=0,
            expand=True
        )
        return elements

    def start_detection(self, e):
        if not self.running:
            self.running = True
            self.video_thread = threading.Thread(target=self.run_detection, daemon=True)
            self.video_thread.start()
            self.camera_status_dot.visible = True
            self.page.update()

    def stop_detection(self, e):
        self.running = False
        self.original_image_control.src_base64 = self.get_placeholder_image()
        self.camera_status_dot.visible = False
        self.page.update()

    def run_detection(self):
        uri = "ws://localhost:8000/ws"
        cap = cv2.VideoCapture(0)
        try:
            asyncio.run(self.process_video(uri, cap))
        finally:
            cap.release()

    def get_placeholder_image(self):
        drowsiness_image = cv2.imread(self.images.image_5)
        _, buffer = cv2.imencode('.jpg', drowsiness_image)
        blank_base64 = base64.b64encode(buffer).decode('utf-8')
        return blank_base64

    def cv2_to_base64(self, image):
        _, img_buffer = cv2.imencode(".jpg", image)
        return base64.b64encode(img_buffer).decode('utf-8')

    async def process_video(self, uri, cap):
        async with websockets.connect(uri) as websocket:
            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # encode the frame
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                # send frame
                await websocket.send(frame_base64)

                # receive response
                response = await websocket.recv()
                response_data = json.loads(response)

                # image original
                original_base64 = response_data.get("original_image")
                original_data = base64.b64decode(original_base64)
                nparr_original = np.frombuffer(original_data, np.uint8)
                original_image = cv2.imdecode(nparr_original, cv2.IMREAD_COLOR)

                # update image in Flet
                self.original_image_control.src_base64 = self.cv2_to_base64(original_image)

                # update UI
                self.page.update()
                await asyncio.sleep(0.01)
