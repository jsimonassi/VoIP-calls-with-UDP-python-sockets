import socket
import threading
import pyaudio
from state_manager import CallState


class CallManager:
    """
    CallManager é responsável por gerenciar todas as chamadas realizadas pelo cliente atual.
    """

    def __init__(self, origin, dest_server, call_window, ring_sound, state_manager, callback):
        print(" Destino: " + str(dest_server))
        HOST = dest_server['ip']
        PORT = 6004
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ring_sound_obj = ring_sound
        self.call_window_obj = call_window
        self.state_manager = state_manager
        self.callback = callback
        dest = (HOST, PORT)
        thread = threading.Thread(target=self.listen, args=(self.udp,))
        thread.start()
        self.send_message(("convite/" + origin), dest)

    def send_message(self, msg, dest):
        """
        Envia uma mensagem udp
        :param msg: Payload da mensagem
        :param dest: Endereço de envio da mensagem
        """
        print("Enviando mensagem: " + msg)
        self.udp.sendto(msg.encode(), dest)

    def listen(self, udp):
        """
        Recebe dados do outro usuário. Isto é, quem responde a chamada.
        :param udp: Objeto da conexão atual.
        """

        py_audio = pyaudio.PyAudio()
        buffer = 4096
        output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=1,
                                      frames_per_buffer=buffer)
        while True:
            try:
                msg, addrress = udp.recvfrom(buffer)
                print("Recebi essa mensagem: " + str(msg) + " Veio desse endereço: " + str(addrress))
                if "aceito" in str(msg):
                    print("Iniciando chamada")
                    self.callback('{"convite": "' + str(msg) + '"}')
                    self.state_manager.set_current_state(CallState.IN_CALL)
                    self.ring_sound_obj.stop_all_sounds()
                    thread = threading.Thread(target=self.send_audio, args=(addrress,))
                    thread.start()

                if "rejeitado" in str(msg):
                    self.callback('{"rejeitado": "' + str(msg) + '"}')
                    self.ring_sound_obj.stop_all_sounds()
                    self.call_window_obj.destroy()

                elif "encerrar_ligacao" in str(msg):
                    self.callback('{"encerra_ligacao": "' + str(msg) + '"}')
                    self.call_window_obj.destroy()
                    self.state_manager.set_current_state(CallState.IDLE)

                if self.state_manager.call_state == CallState.IN_CALL:
                    output_stream.write(msg)

            except Exception as e:
                print("Error: " + str(e))

    def send_audio(self, dest):
        """
        Envia audio para o outro usuário
        :param dest: Destino do outro usuário
        """
        try:
            py_audio = pyaudio.PyAudio()
            buffer = 1024

            input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=1,
                                         frames_per_buffer=buffer)

            while self.state_manager.call_state == CallState.IN_CALL:
                print("Enviando audio!")
                data = input_stream.read(buffer, exception_on_overflow=False)
                self.udp.sendto(data, dest)

            print("Hora de finalizar a chamada!")
            self.udp.sendto("encerra_ligacao".encode(), dest)
            self.call_window_obj.destroy()

        except Exception as e:
            print(str(e))

    def end_call(self):
        """
        Finaliza chamada atual
        """
        self.call_window_obj.destroy()
        self.ring_sound_obj.stop_all_sounds()
        self.state_manager.set_current_state(CallState.IDLE)

# TODO: Alguém precisa fechar esse tanto de thread aberta. Está gerendo travaentos ao encerrar o app.