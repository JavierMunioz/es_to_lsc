import sounddevice as sd
import queue

class AudioStreamService:
    def __init__(self, device_id, samplerate=16000):
        self.queue = queue.Queue()
        self.stream = sd.InputStream(
            device=device_id,
            channels=1,
            samplerate=samplerate,
            callback=self.callback
        )

    def callback(self, indata, frames, time, status):
        self.queue.put(indata.copy())

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
