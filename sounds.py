import pyaudio
from time import sleep
import threading


class Sound:

    """
    Classe que gerencia os sons do app.
    Som de chamada recebida, discagem e etc.
    """

    def __init__(self):
        self.need_play = False

    def _thread_call_sound(self):
        while self.need_play:
            global stream
            myRates = [4185, 7900, 5275, 7900]
            for v_rate in myRates:
                stream = pyaudio.PyAudio().open(format=pyaudio.paInt8, channels=1, rate=v_rate, output=True)
                for beep_num in range(0, 2):
                    for n in range(0, 50, 1):
                        stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")
                        if not self.need_play:
                            stream.close()
                            pyaudio.PyAudio().terminate()
                            return
            stream.close()
            pyaudio.PyAudio().terminate()

    def play_incoming_call_sound(self):
        self.need_play = True
        thread_incoming_call_sound = threading.Thread(target=self._thread_call_sound)
        thread_incoming_call_sound.start()

    def stop_all_sounds(self):
        self.need_play = False

    def play_ring_call_sound(self):
        self.need_play = True
        thread_incoming_call_sound = threading.Thread(target=self._thread_start_ring)
        thread_incoming_call_sound.start()

    def _thread_start_ring(self):
        ring_output_stream = pyaudio.PyAudio().open(format=pyaudio.paInt8, channels=1, rate=4700, output=True)
        while self.need_play:
            for n in range(400):
                ring_output_stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")
            sleep(2)
        ring_output_stream.close()
        pyaudio.PyAudio().terminate()
