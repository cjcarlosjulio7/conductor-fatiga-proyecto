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
            width=280,
            height=300,
            fit=ImageFit.COVER,
            src_base64=self.get_placeholder_image()
        )

        #self.sketch_image_control = Image(
        #    width=440,
        #    height=280,
        #    fit=ImageFit.COVER,
        #    src_base64=self.get_placeholder_image()
        #)

        self.start_button = ElevatedButton(
            text="Start",
            on_click=self.start_detection,
            bgcolor='green',
            color='#FFFFFF',
        )
        self.stop_button = ElevatedButton(
            text="Stop",
            on_click=self.stop_detection,
            bgcolor='red',
            color='#FFFFFF',
        )

        self.luz_roja = Container(
            width=20,
            height=20,
            bgcolor="red",  # Color rojo
            border_radius=10,
            visible=False  # Inicialmente no visible  
        )

        left_column = Column(
            controls=[
                self.luz_roja, 
                Container(height=30),
                self.original_image_control,
                self.start_button,
                self.stop_button, #agregado de la otra columna
            ],
            alignment='center',
            horizontal_alignment='center',
            #spacing=20,
            height=520,  # Altura específica
            width=300    # Ancho específico opcional
        )

        #right_column = Column(
        #   controls=[
        #        Container(height=30),
        #        #self.sketch_image_control,
        #        #self.stop_button,
        #    ],
        #    alignment='center',
        #    horizontal_alignment='center',
        #    spacing=20,
        #    expand=True
        #)

        
        left_column_container = Container(
            content=left_column,  # Contenedor original
            bgcolor="#000000",  # Fondo gris claro (puedes cambiarlo a cualquier color)
            border_radius=12,
        )

        elements = Container(
            content=Row(
                controls=[

                    left_column_container,
                    #right_column
                ],
                alignment='spaceEvenly',
                vertical_alignment='center',
            ),
            bgcolor="#1c1c1c",
            padding=0,
            expand=True
        )
        return elements

    def start_detection(self, e):
        if not self.running:
            self.running = True
            self.video_thread = threading.Thread(target=self.run_detection, daemon=True)
            self.video_thread.start()
            self.luz_roja.visible = True
            self.start_button.visible = False
            self.stop_button.visible = True



    def stop_detection(self, e):
        self.running = False
        self.original_image_control.src_base64 = self.get_placeholder_image()
        #self.sketch_image_control.src_base64 = self.get_placeholder_image()
        self.luz_roja.visible = False
        self.start_button.visible = True
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

                # sketch image
                sketch_base64 = response_data.get("sketch_image")
                sketch_data = base64.b64decode(sketch_base64)
                nparr_sketch = np.frombuffer(sketch_data, np.uint8)
                sketch_image = cv2.imdecode(nparr_sketch, cv2.IMREAD_COLOR)

                # image original
                original_base64 = response_data.get("original_image")
                original_data = base64.b64decode(original_base64)
                nparr_original = np.frombuffer(original_data, np.uint8)
                original_image = cv2.imdecode(nparr_original, cv2.IMREAD_COLOR)

                
                # update image in Flet
                alpha = 0.4  # Ajusta la opacidad del sketch
                overlay_image = cv2.addWeighted(original_image, 1 - alpha, sketch_image, alpha, 0)
                self.original_image_control.src_base64 = self.cv2_to_base64(overlay_image)

                #self.original_image_control.src_base64 = self.cv2_to_base64(original_image)
                #self.original_image_control.src_base64 = self.cv2_to_base64(sketch_image)

                # update UI
                self.page.update()
                await asyncio.sleep(0.01)
