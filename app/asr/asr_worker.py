from PySide6.QtCore import QThread, Signal
from faster_whisper import WhisperModel
import numpy as np


class ASRWorker(QThread):
    text_ready = Signal(str)

    def __init__(self, audio_queue):
        super().__init__()
        self.audio_queue = audio_queue
        self.running = True

        # Modelo pequeño = menos delay
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        self.buffer = np.array([], dtype=np.float32)

    def run(self):
        while self.running:
            audio_chunk = self.audio_queue.get()

            # audio_chunk: (frames, channels)
            audio_chunk = audio_chunk.flatten()
            self.buffer = np.concatenate((self.buffer, audio_chunk))

            # Procesar cada ~1 segundo de audio
            if len(self.buffer) >= 16000:
                segment_audio = self.buffer[:16000]
                self.buffer = self.buffer[16000:]

                segments, _ = self.model.transcribe(
                    segment_audio,
                    language="es",
                    vad_filter=True
                )

                text = ""
                for segment in segments:
                    text += segment.text + " "

                if text.strip():
                    self.text_ready.emit(text.strip())

    def stop(self):
        self.running = False
