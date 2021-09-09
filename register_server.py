import socket
import json
import threading

HOST = '25.90.35.163'  # Endereco IP do Servidor
PORT = 5005  # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)

clientes = {}

print("Servidor Iniciado")


def sendall(origin, msg):
    """
    Envia uma mensagem de evento para todos os clientes, exceto, o cliente de origem.
    :param origin: Cliente que originou o evento
    :param msg: Texto da mensagem
    """
    try:
        for cl in clientes:
            if cl != origin:
                clientes.get(cl)[2].send(('{"event": "' + origin + msg + '"}').encode())
    except Exception as e:
        print("SendAll error: " + str(e))


def in_communication(client, con):
    """
    Executado após uma conexão ser estabelecida. Responsável por gerenciar as requições no servidor.
    :param client: Ip e Porta do current client
    :param con: Objeto de socket da conexão atual
    """
    try:
        ip_cliente = client[0]
        port_cliente = client[1]

        while True:
            msg = con.recv(1024).decode()

            if "{" in msg:
                msg = json.loads(msg)

                if "Registro" in msg.keys():
                    name = msg.get("Registro")
                    if name not in clientes:
                        clientes[name] = [ip_cliente, port_cliente, con]
                        con.send(("Novo registro efetuado/" + ip_cliente).encode())
                        print(clientes)
                        sendall(name, " está online!")
                    else:
                        con.send(("Usuário ja registrado").encode())
                        con.close()
                        print('Usuário já registrado: ' + name + ' - A conexão foi finalizada.')
                        return

                elif "Consulta" in msg.keys():
                    name = msg.get("Consulta")
                    # se buscou com vazio, deve retornar todos os usuários
                    # Todo: Melhorar a montagem desse json
                    if len(name) == 0:
                        i = 0
                        response = '{"clients": ['
                        for obj in clientes:
                            response += '{"user":"' + obj + '", "ip":"' + clientes.get(obj)[0] + '", "port": "' \
                                        + str(clientes.get(obj)[1])
                            if i == len(clientes) - 1:
                                response += '"}'
                            else:
                                response += '"},'
                            i += 1

                        response += ']}'
                        con.send(response.encode())

                    # Caso contrário, retorna só a primeira ocorrência
                    elif name in clientes:
                        con.send(('{"clients": [{"user":"' + name + '", "ip":"' + str(ip_cliente) + '", "port": "'
                                  + str(port_cliente) + '"}]}').encode())
                    else:
                        con.send('{"error": "Usuário não esta registrado"}'.encode())
                elif "Encerrar" in msg.keys():
                    break
            if not msg:
                break

        for key, value in clientes.items():
            if (value == [ip_cliente, port_cliente, con]):
                print('Finalizando conexao do cliente', key)
                clientes.pop(key)
                sendall(key, " saiu!")
                con.close()
                break

    except Exception as e:
        print("Error: " + str(e))


try:
    """
    Main loop do servidor. Fica aguardando novas conexões e abre uma nova thread para cada client conectado
    """
    while True:
        con, client = tcp.accept()
        thread = threading.Thread(target=in_communication, args=(client, con,))
        thread.start()
except KeyboardInterrupt as e:
    print("Servidor finalizado pelo teclado")
except Exception as e:
    print("Error: " + str(e))