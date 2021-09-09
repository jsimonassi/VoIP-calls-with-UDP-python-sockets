import time
import pyaudio
import socket
import threading
from state_manager import CallState


class CallServer:
    """
    Servidor de ligação. Responsável por receber e tratar dados e chamadas.
    """
    def __init__(self, current_ip, sound_obj, state_manager, callback):
        self.current_client = {}
        self.sound_obj = sound_obj
        self.call_window = None
        self.state_manager = state_manager
        self.callback = callback
        HOST = current_ip
        PORT = 6005
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        self.udp.bind(orig)
        print("Socket de ligação criado")

    def init_call_server(self, window):
        """
        Inicia o servidor de ligação.
        :param window: Tela principal da aplicação
        """
        print("Iniciando servidor")
        self.callback('{"info": "Iniciando servidor de ligação"}')
        py_audio = pyaudio.PyAudio()
        buffer = 4096
        output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=1,
                                      frames_per_buffer=buffer)
        while True:
            msg, client = self.udp.recvfrom(buffer)
            print(client, str(msg))
            print("Vou testar com " + str(msg))
            if "convite" in str(msg):
                if self.state_manager.call_state == CallState.IN_CALL:
                    self.callback('{"convite": "' + str(msg) + '"}')
                    self.udp.sendto("rejeitado - Usuário ocupado".encode(), client)
                else:
                    self.current_client = {"username": msg.decode().split("/")[1], "ip": str(client[0]),
                                           "port": int(client[1])}
                    time.sleep(2)
                    print("Gerando event")
                    self.sound_obj.play_incoming_call_sound()
                    thread = threading.Thread(target=window.event_generate, args=("<<newCall>>",))
                    thread.start()
                    print("depois do event")
            elif "encerrar_ligacao" in str(msg):
                self.callback('{"encerrar_ligacao": "' + str(msg) + '"}')
                self.state_manager.set_current_state(CallState.IDLE)
                print("Encerra ligação")

            if self.state_manager.call_state == CallState.IN_CALL:
                print("Recebendo audio!")
                output_stream.write(msg)

    def answer_invitation(self, answer, dest):
        """
        Responde convites de chamadas
        :param answer: Resposta do convite
        :param dest: Destino da resposta
        """
        try:
            print("Resposta: " + answer)
            self.callback('{"resposta": "' + str(answer) + '"}')
            self.udp.sendto(answer.encode(), tuple([dest["ip"], dest["port"]]))

            if 'aceito' in answer:
                self.state_manager.set_current_state(CallState.IN_CALL)
                thread = threading.Thread(target=self.send_audio, args=(self.udp, tuple([dest["ip"], dest["port"]]),))
                thread.start()

        except Exception as e:
            print("Deu erro:" + str(e))

    def send_audio(self, udp, dest):
        """
        Envia audio para outro usuário.
        :param udp: Conexão udp atual
        :param dest: Destino de envio do audio
        """
        try:
            py_audio = pyaudio.PyAudio()
            buffer = 1024

            input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=1,
                                         frames_per_buffer=buffer)
            while self.state_manager.call_state == CallState.IN_CALL:
                print("Enviando audio!")
                data = input_stream.read(buffer, exception_on_overflow = False)
                udp.sendto(data, dest)

            print("A chamada deve ser finalizada aqui!")
            udp.sendto("encerrar_ligacao".encode(), dest) # TODO: Validar

            if self.call_window is not None:
                self.call_window.destroy()

        except Exception as e:
            print(str(e))

    def end_call(self, call_window):
        """
        Finaliza chamada atual
        :param call_window: Popup de chamada atual
        """
        call_window.destroy()
        self.state_manager.set_current_state(CallState.IDLE)

    def set_call_window(self, call_window):
        """
        Altera objeto de popup da chamada atual
        :param call_window: objeto de popup
        """
        self.call_window = call_window
