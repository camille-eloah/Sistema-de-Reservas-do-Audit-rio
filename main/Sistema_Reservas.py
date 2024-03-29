from tkinter import *
from tkinter import ttk, messagebox 
from tkcalendar import Calendar
from tkinter import ttk

import time
import random
import threading
import pickle
import sqlite3


class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("880x640")

        # Criando os containers
        self.container_principal = Frame(master=self.root, width=880, height=640, bg="#0d1b2a")
        self.container_principal.pack()

        self.navbar = Frame(master=self.container_principal, width=880, height=100, bg="#0d1b2a")
        self.navbar.pack()

        self.corpo = Frame(master=self.container_principal, width=880, height=400, bg="#415a77")
        self.corpo.pack()

        self.area_bott = Frame(master=self.corpo, width=880, height=140, bg="#1b263b")
        self.area_bott.pack()
        
        self.area_exibicao = Frame(master=self.container_principal, width=880, height=260, bg="#0d1b2a")
        self.area_exibicao.pack()

        self.area_calendario = Frame(master=self.corpo, width=880, height=300, bg="green")
        self.area_calendario.pack()

        # Criando calendário
        self.calendario = Calendar(self.area_calendario, selectmode="day", year=2023, month=12, day=27,
                                   background="black", disabledbackground="black", bordercolor="black",
                                   headersbackground="black", normalbackground="black", foreground='white',
                                   normalforeground='white', headersforeground='white')
        self.calendario.config(background="black")
        self.calendario.pack()

        # Logo
        img = PhotoImage(file="./logo_oficial.png")

        self.label_imagem = Label(self.container_principal, image=img)
        self.label_imagem.place(x=1, y=1, width=50, height=50)


        # Campo para o nome da reserva
        self.label_nome = Label(self.area_bott, text="Responsável:", font=("Helvetica", 10, "bold"), bg="#1b263b", fg="white")
        self.label_nome.place(x=10, y=20)
        self.entry_nome = Entry(self.area_bott, width=110)
        self.entry_nome.place(x=130, y=20)

        # Seletor de horário de início
        self.label_inicio = Label(self.area_bott, text="Horário de Início:", font=("Helvetica", 10, "bold"), bg="#1b263b", fg="white")
        self.label_inicio.place(x=10, y=60)
        self.combobox_inicio = ttk.Combobox(self.area_bott, values=self.get_horarios(), state="readonly")
        self.combobox_inicio.place(x=130, y=60)

        # Seletor de horário de fim
        self.label_fim = Label(self.area_bott, text="Horário de Fim:", font=("Helvetica", 10, "bold"), bg="#1b263b", fg="white")
        self.label_fim.place(x=10, y=90)
        self.combobox_fim = ttk.Combobox(self.area_bott, values=self.get_horarios(), state="readonly")
        self.combobox_fim.place(x=130, y=90)

        # Botão de reservar
        self.botao_reserva = Button(self.area_bott, text="Reservar", bg="#0078d7", fg="white", command=self.reservar)
        self.botao_reserva.place(x=340, y=80, height=30, width=100)
        
        # Botão de exibir
        self.botao_exibir = Button(self.area_bott, text="Exibir", command=self.exibir_reservas)
        self.botao_exibir.place(x=460, y=80, height=30, width=100)
        
        # Botão de deletar
        self.botao_deletar = Button(self.area_bott, text="Deletar", bg="#f03a47", fg="white", command=self.deletar_reserva)
        self.botao_deletar.place(x=580, y=80, height=30, width=100)
        
        # Botão de backup
        self.botao_backup = Button(self.area_bott, text="Fazer Backup", command=self.fazer_backup)
        self.botao_backup.place(x=700, y=80, height=30, width=100)
        
        # Título "Sistema de Reservas de Auditório" no Frame navbar
        self.label_titulo = Label(self.navbar, text="Sistema de Reservas de Auditório", font=("Helvetica", 16, "bold"), bg="#0d1b2a", fg="white")
        self.label_titulo.pack(pady=12) 

        # Título "Reservas do dia"
        self.label_exibicao = Label(self.area_exibicao, text="Reservas do dia", font=("Helvetica", 12, "bold"), bg="#0d1b2a", fg="white")
        self.label_exibicao.place(x=10, y=10)
        
        # Widget de texto para exibir as reservas
        self.texto_exibicao = Text(self.area_exibicao, wrap="word", height=8, width=70)
        self.texto_exibicao.place(x=10, y=50)
        
        # Campos das frases motivacionais na interface
        self.titulo_frase_motivar = Label(self.area_exibicao, text="Frase Motivacional", font=("Helvetica", 12, "bold"), bg="#0d1b2a", fg="white") 
        self.titulo_frase_motivar.place(x=10, y=200)
        
        self.label_frase_motivar = Label(self.area_exibicao, text="Frase", font=("Helvetica", 10), bg="#778da9") 
        self.label_frase_motivar.place(x=10, y=230)
        
        # Lista de frases motivacionais
        self.frases_motivacionais = [
            "O sucesso está em quantas vezes você é capaz de voltar pro foco, mesmo você falhando.",
            "Cultive amor pelas pessoas!",
            "A felicidade vem de se importar com algo muito maior que você.",
            "Que adianta ao homem ganhar o mundo inteiro e perder a sua alma?",
            "Até os jovens se cansam e ficam exaustos, aqueles que esperam no Senhor renovam as suas forças.",
            "Cuide do seu jardim, para que as borboletas venham até ele. Se no final não vier nenhuma borboleta, você terá um belo jardim.",
            "Onde há um problema... Você pode criar uma solução!",
            "Quem é fiel no pouco, é fiel no muito, e quem é infiel no pouco, também é infiel no muito.",
            "Se você não é grato pelas coisas hoje, quem dirá que você será grato depois? Seja grato agora.",
            "Saiba o que acende a luz em você, para que da sua própria maneira, você possa iluminar o mundo.",
            "Ei, você não está preso as suas circunstâncias!",
            "Tenha muito cuidado com o que deseja de coração... Porque por certo será seu!",
            "Molduras boas não salvam quadros ruins",
            "Um mais um é sempre mais que dois",
            "Ninguém sabe tanto que não tem o que aprender, ninguém sabe tão pouco que não tenha nada para ensinar.",
            "Um tolo é conhecido por seu discurso e um sábio por seu silêncio.",
            "Que a luz de Deus brilhe dentro de você e reflita à sua volta!",
            "Ao envelhecer, parei de escutar o que as pessoas dizem. Agora só presto atenção ao que elas fazem.",
            "Inveja é burrice. Deus tem um plano só pra você!",
            "Sapere aude! Ouse ser sábio.",
            "O difícil é um punhado de coisas fáceis" 
        ]
        
        # Inicializa a thread para atualizar as frases motivacionais
        self.thread_frases_motivacionais = threading.Thread(target=self.atualizar_frases)
        self.thread_frases_motivacionais.start()
        
        # Conecta ao banco de dados SQLite
        self.conn = sqlite3.connect('reservas.db')
        self.cursor = self.conn.cursor()

        # Cria a tabela
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                data TEXT,
                horario_inicio TEXT,
                horario_fim TEXT,
                responsavel TEXT
            )
        ''')
        
        # Dicionário para armazenar as reservas. As chaves são as datas.
        self.reservas_por_dia = {}
        
        self.carregar_database()
        print(self.reservas_por_dia)

        self.root.mainloop()

    #######################
    # FUNÇÕES DO PROGRAMA #
    #######################
    
    def get_horarios(self):
        # Retorna uma lista de horários
        return [f"{hora:02d}:00" for hora in range(7, 22)]

    def carregar_database(self):
        self.cursor.execute('''
            SELECT data, horario_inicio, horario_fim, responsavel
            FROM reservas
        ''')
        dados = self.cursor.fetchall()

        # Preenche o dicionário com os dados do reservas.db
        for data, horario_inicio, horario_fim, responsavel in dados:
            if data not in self.reservas_por_dia:
                self.reservas_por_dia[data] = []
            
            reserva = [horario_inicio, horario_fim, responsavel]
            self.reservas_por_dia[data].append(reserva)
    
    
    def fazer_backup(self):
        # Realiza backup dos dados em formato serializado usando pickle
        try:
            with open('backup_reservas.pkl', 'wb') as arquivo:
                pickle.dump(self.reservas_por_dia, arquivo)
            messagebox.showinfo("Backup Concluído", "Backup realizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro no Backup", f"Ocorreu um erro durante o backup: {str(e)}")
    
    def reservar(self):
        data_selecionada = self.calendario.get_date()
        horario_inicio = self.combobox_inicio.get()
        horario_fim = self.combobox_fim.get()
        nome_reserva = self.entry_nome.get()

        try:
            if self.verificar_reservado(data_selecionada, horario_inicio, horario_fim):
                raise ValueError("Este período de horário já foi reservado para este dia.")
        except ValueError as error:
            messagebox.showerror("Erro de Reserva", str(error))
            return

        # Adiciona a reserva ao banco de dados
        self.cursor.execute('''
            INSERT INTO reservas (data, horario_inicio, horario_fim, responsavel)
            VALUES (?, ?, ?, ?)
        ''', (data_selecionada, horario_inicio, horario_fim, nome_reserva))
        self.conn.commit()

        # Atualiza o dicionário local
        if data_selecionada not in self.reservas_por_dia:
            self.reservas_por_dia[data_selecionada] = []
        self.reservas_por_dia[data_selecionada].append([horario_inicio, horario_fim, nome_reserva])

        messagebox.showinfo("Concluído", "A reserva foi feita com sucesso!")

        
    def verificar_reservado(self, data, novo_inicio, novo_fim):
        # Verifica se o novo horário já foi reservado
        try:
            if data in self.reservas_por_dia:
                for reserva in self.reservas_por_dia[data]:
                    inicio_reserva, fim_reserva = self.obter_horarios(reserva)

                    if (novo_inicio == inicio_reserva or novo_fim == fim_reserva or
                            (novo_inicio > inicio_reserva and novo_inicio < fim_reserva) or
                            (novo_fim > inicio_reserva and novo_fim < fim_reserva)):
                        raise ValueError("Este período de horário já foi reservado para este dia.")
        except ValueError as error:
            return True
        return False

    def obter_horarios(self, reserva):
        # Obtém os horários de início e fim
        return reserva[0], reserva[1]

    def exibir_reservas(self):
        data_selecionada = self.calendario.get_date()
        
        # Limpa o widget de texto antes de exibir as novas reservas
        self.texto_exibicao.delete(1.0, END)
        
        if data_selecionada in self.reservas_por_dia:
            self.texto_exibicao.insert(END, f"Reservas para {data_selecionada}:\n")
            # Itera sobre as listas das reservas da data selecionada
            for dados in self.reservas_por_dia[data_selecionada]:
                # Cria uma mensagem para cada reserva
                texto = f'Das {dados[0]} às {dados[1]} por {dados[2]}'
                # Exibe a mensagem no widget de texto
                self.texto_exibicao.insert(END, f"{texto}\n")
        else:
            self.texto_exibicao.insert(END, f"Não há reservas para {data_selecionada}.")


    def deletar_reserva(self):
        data_selecionada = self.calendario.get_date()
        horario_inicio = self.combobox_inicio.get()
        horario_fim = self.combobox_fim.get()

        if data_selecionada in self.reservas_por_dia:
            horario_encontrado = False
            novas_reservas = []

            for reserva in self.reservas_por_dia[data_selecionada]:
                if reserva[0] == horario_inicio and reserva[1] == horario_fim:
                    print(f"Reserva removida para {data_selecionada}: {reserva}")
                    messagebox.showinfo("Concluído", "A reserva foi deletada com sucesso!")
                    horario_encontrado = True
                else:
                    novas_reservas.append(reserva)

            self.reservas_por_dia[data_selecionada] = novas_reservas

            # Remove a reserva do banco de dados se o horário foi encontrado
            if horario_encontrado:
                self.cursor.execute('''
                    DELETE FROM reservas
                    WHERE data = ? AND horario_inicio = ? AND horario_fim = ?
                ''', (data_selecionada, horario_inicio, horario_fim))
                self.conn.commit()
            else:
                messagebox.showerror("Erro ao Deletar", "Não há reservas para esse horário nessa data.")
        else:
            messagebox.showerror("Erro ao Deletar", "Não há reservas para essa data.")

    def atualizar_frases(self):
        while True:
            # Atualiza as frases aleatoriamente
            nova_frase = random.choice(self.frases_motivacionais)
            self.label_frase_motivar.config(text=nova_frase)
            time.sleep(5)


def __del__(self):
    self.conn.close()


app = App()

# Camille Eloá & Licurgo Keven
