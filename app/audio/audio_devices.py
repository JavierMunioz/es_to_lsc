import sounddevice as sd

class AudioDeviceService:
    def get_input_devices(self):
        devices = []
        for index, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                devices.append({
                    "id": index,
                    "name": device["name"]
                })
        return devices
