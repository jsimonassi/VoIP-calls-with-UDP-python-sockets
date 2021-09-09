from home_layout import *
from tkinter import *
from tkinter import messagebox


def valid_information():
    """
    Valida as informações que estão nos campos para não permitir conexões com campos vazios.
    :return: Booleano representando se as informações são válidas ou não.
    """
    if len(name.get()) > 0 and len(ip.get()) > 0:
        return True
    return False


def start_connection():
    """
    Solicita ao client a conexão de um novo usuário.
    """
    if not valid_information():
        messagebox.showerror("Error", "Preencha todas as informações solicitadas.")
        return

    resp = client.conn(name.get(), ip.get())
    print(resp)
    if 'Novo registro efetuado' in resp:
        # Enviando também o ip atual para iniciar o servidor de ligação com o ip correto em cada máquina.
        set_home(resp.split("/")[1], name.get())

    elif 'Usuário ja registrado' in resp:
        messagebox.showerror("Atenção", "Usuário já registrado - Conexão encerrada. Tente outro nome.")

    else:
        messagebox.showerror("Error", "Erro ao fazer requisição: " + resp)


"""
Interface gráfica da tela inicial.
Obs: Pode variar de acordo com o SO.
"""
window = Tk()
window.geometry("530x600")
window.configure(background='#EFEFEF')
window.title("Calls UFF")

# Header
header_img = PhotoImage(file="assets/images/header.png")
header = Label(window, image=header_img, background='#EFEFEF')
header.place(x=15, y=15)

# Descrição
desc = Label(window, text="Antes de começar,", background='#EFEFEF', fg='black', font=("Arial", 20, "bold"))
desc.place(x=40, y=290)

desc = Label(window, text="precisamos de algumas informações", background='#EFEFEF', fg='black',
             font=("Arial", 20, "bold"))
desc.place(x=40, y=320)

# Content
view_img = PhotoImage(file="assets/images/view_background.png")
view = Label(window, image=view_img, background='#EFEFEF', )
view.place(x=15, y=360)

desc = Label(window, text="IP do servidor: ", background='#ffffff', fg='black', font=("Arial", 16))
desc.place(x=40, y=380)
ip = Entry(window, width=50, bg="white", fg="black", bd=1)
ip.place(x=40, y=410)

desc = Label(window, text="Nome de usuário: ", background='#ffffff', fg='black', font=("Arial", 16))
desc.place(x=40, y=440)
name = Entry(window, width=50, bg="white", fg="black", bd=1)
name.place(x=40, y=470)

# Todo: Botão com uma borda. Preciso descobrir de onde isso vem e remover.
button = Button(window, text="Conectar", command=start_connection, background='#EFEFEF', activeforeground='#EFEFEF', bd=0,
                bg='#EFEFEF', highlightcolor='#EFEFEF')
button.place(x=220, y=550)

window.mainloop()
