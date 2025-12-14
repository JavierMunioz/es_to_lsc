from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit
)
from audio.audio_devices import AudioDeviceService
from asr.asr_worker import ASRWorker
from asr.gloss_service import GlossService
from audio.audio_stream import AudioStreamService


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_service = AudioDeviceService()
        self.gloss_service = GlossService()
        self.setup_ui()
        self.load_audio_devices()

    def setup_ui(self):
        self.setWindowTitle("Traductor Voz → LSC")
        self.resize(400, 420)

        self.partial_text = ""

        
        self.audio_label = QLabel("Seleccione dispositivo de audio")
        self.audio_selector = QComboBox()
        self.refresh_button = QPushButton("Refrescar dispositivos")

        self.text_label = QLabel("Texto reconocido")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        self.gloss_label = QLabel("Glosas LSC")
        self.gloss_output = QTextEdit()
        self.gloss_output.setReadOnly(True)

        self.start_button = QPushButton("Iniciar")


        self.start_button.clicked.connect(self.start_asr)

        layout = QVBoxLayout()
        layout.addWidget(self.audio_label)
        layout.addWidget(self.audio_selector)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.start_button)

        layout.addWidget(self.text_label)
        layout.addWidget(self.text_output)

        layout.addWidget(self.gloss_label)
        layout.addWidget(self.gloss_output)

        self.setLayout(layout)

        self.refresh_button.clicked.connect(self.load_audio_devices)
    
    def update_text(self, text):
        self.partial_text += " " + text
        self.text_output.setText(self.partial_text.strip())

        gloss = self.gloss_service.to_gloss(self.partial_text)
        self.gloss_output.setText(gloss)

    def start_asr(self):
        device_id = self.audio_selector.currentData()

        self.audio_stream = AudioStreamService(device_id)
        self.audio_stream.start()

        self.asr_worker = ASRWorker(self.audio_stream.queue)
        self.asr_worker.text_ready.connect(self.update_text)
        self.asr_worker.start()


    def load_audio_devices(self):
        self.audio_selector.clear()

        devices = self.audio_service.get_input_devices()
        for device in devices:
            self.audio_selector.addItem(
                f"{device['id']}: {device['name']}",
                device["id"]
            )
