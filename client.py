import socket
import threading
import call_server


def listen_server(callback):
    """
    Responsável por escutar todas as respostas do servidor (Apenas depois da conexão ser estabelecida).
    :param callback: Função passada como parâmetro pela view. Esta é uma forma de retornar a mensagem a view sem gerar
    dependência circular.
    """
    try:
        while True:
            resp = tcp.recv(1024)
            callback(resp.decode())
    except Exception as e:
        print("Conexão finalizada")


def start_listener(call_server_obj, callback, window, state_manager):
    """
    Inicia thread com método responsável pela escuta das respostas do servidor. É feita em uma thread separada para não
    bloquear o fluxo de execução principal da aplicação
    :param state_manager: Gerenciador de estados de chamadas
    :param call_server_obj: Objeto do servidor de ligação
    :param window: GUI tkinter
    :param callback: Função passada como parâmetro pela view para exibir retornos do servidor.
    """
    thread = threading.Thread(target=listen_server, args=(callback,))
    thread.start()

    """
    Inicia servidor de ligação e fica esperando chamadas
    :param callback: Função passada como parâmetro pela view para exibir retornos do servidor.
    """
    thread = threading.Thread(target=call_server_obj.init_call_server, args=(window,))
    thread.start()


def conn(username, server_ip):
    """
    Solicita ao servidor o início de uma nova conexão.
    :param username: Nome do novo usuário
    :param server_ip: Ip do servidor
    :return Resposta do servidor para solicitação de nova conexão
    """
    global tcp
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = server_ip
    print(HOST)
    PORT = 5005

    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send(('{"Registro":"' + username + '"}').encode())

    resp = tcp.recv(1024)
    msg = resp.decode()
    if 'Usuário ja registrado' in msg:
        tcp.close()

    return msg


def search_user(username):
    """
    Realiza busca no servidor a procura de determinado usuário
    :param username: Nome do usuário que se deseja encontrar (Chave da busca)
    """
    msg = '{"Consulta":"' + username + '"}'
    tcp.send(msg.encode())


def get_all_users():
    """
    Retorna todos os usuários com conexões ativas.
    """
    msg = '{"Consulta":"''"}'
    tcp.send(msg.encode())


def close_conn(username=" "):
    """
    Encerra a conexão de um usuário
    :param username: Nome do usuário que se deseja encerrar a conexão
    """
    try:
        tcp.send(('{"Encerrar":"' + username + '"}').encode())
        tcp.close()
    except:
        print("______")


def get_current_client():
    return tcp
