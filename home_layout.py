import json
from tkinter import *
from tkinter import messagebox
import client as client


def event_callback(e):
    """
    É chamado pelo client sempre que se recebe uma resposta do servidor. Tem a responsabilidade de tidentificar o tipo
    de resposta e tratar conforme necessário.
    :param e: evento de resposta (Em geral é uma string representando a resposta do servidor já decodificada.
    """
    log(e)
    try:
        msg = json.loads(e)
        if 'clients' in msg:
            global last_users
            last_users = msg
            set_users_list()
        elif 'event' in msg:
            search_user()
        elif 'error' in msg:
            messagebox.showerror("Error", msg['error'])

    except:
        log("Erro ao processar resposta do servidor")


def search_user():
    """
    Chamando ao clicar no botão de busca.
    Checa se existe algo no form field (Entry) de busca e chama os métodos do client de acordo com o dado recebido.
    """
    if len(find_user.get()) == 0:
        client.get_all_users()
    else:
        client.search_user(find_user.get())


def close_conn():
    """
    Chamando ao clicar no botão de sair.
    Solicita fechamento de conexão.
    """
    client.close_conn()
    exit(0)


def immediately(e):
    """
    Callback de eventos do listBox.
    Chamado automaticamente quando um usuário da lista é selecionado.
    """
    index = lb_users.curselection()[0]
    global call_view_title
    global call_view_desc

    # Limpa valores antigos antes de atualizar
    try:
        if call_view_title and call_view_desc:
            call_view_title.destroy()
            call_view_desc.destroy()
    except:
        log("Adicionando dados a view")

    call_view_title = Label(window, text=last_users['clients'][index]['user'], background='white', fg='black',
                            font=("Arial", 20, "bold"))
    call_view_title.place(x=555, y=350)
    call_view_desc = Label(window, text='IP: ' + last_users['clients'][index]['ip'] + 'Porta: ' +
                                        last_users['clients'][index]['port'], background='white', fg='black',
                           font=("Arial", 16))
    call_view_desc.place(x=520, y=380)


def set_users_list():
    """
    Atualiza lista de usuários
    """
    global lb_users
    lb_users = Listbox(window, width=40, height=21, background='#ffffff', foreground='black')
    if last_users:
        for user in last_users['clients']:
            lb_users.insert(END, user['user'])

    lb_users.place(x=40, y=200)
    lb_users.bind("<<ListboxSelect>>", immediately)


def log(message):
    """
    Adiciona mensagem de log ao logcat
    :param message: Messagem a ser adicionada
    """
    global lb_logcat
    lb_logcat.insert(END, message)


def set_logcat():
    """
    Definindo logcat na interface
    """
    global lb_logcat
    lb_logcat = Listbox(window, width=77, height=5, background='black', foreground='white')
    lb_logcat.insert(END, "Log:")
    lb_logcat.place(x=40, y=600)


def set_home(username=""):
    """
    Entry Point da home.
    Responsável por implementar toda a estrutura da interface gráfica
    :param username: Nome do usuário conectado
    """
    global window
    window = Toplevel()
    window.geometry("800x740")
    window.configure(background='#EFEFEF')
    window.title("Calls UFF")

    desc = Label(window, text="Olá, " + username.split(" ")[0].strip() + '.', background='#EFEFEF', fg='black',
                 font=("Arial", 24, "bold"))
    desc.place(x=40, y=40)
    desc = Label(window, text="Com quem vamos falar hoje?", background='#EFEFEF', fg='black', font=("Arial", 20))
    desc.place(x=40, y=70)

    desc = Label(window, text="Nome do usuário: ", background='#EFEFEF', fg='black', font=("Arial", 16))
    desc.place(x=40, y=115)
    global find_user
    find_user = Entry(window, width=30, bg="white", fg="black", bd=1)
    find_user.place(x=40, y=140)

    button = Button(window, text="Buscar", command=search_user, background='#EFEFEF', activeforeground='#EFEFEF',
                    bd=0,
                    bg='#EFEFEF', highlightcolor='#EFEFEF')
    button.place(x=330, y=140)

    call_img = PhotoImage(file="assets/images/background_calls.png")
    call_background = Label(window, image=call_img, background='#EFEFEF')
    call_background.place(x=420, y=180)

    button = Button(window, text="Sair", command=close_conn,
                    bd=0,
                    bg='red', highlightcolor='#EFEFEF')
    button.place(x=700, y=10)

    set_logcat()
    search_user()
    client.start_listener(event_callback)
    window.mainloop()
