import tkinter as tk
from datetime import datetime

from project.DB.AppDB import AppDB
from tkinter import ttk, messagebox


class Main:
    def __init__(self, win):
        self.objetoDB = AppDB()

        self.lblCodigo = tk.Label(win, text="ID do Chamado:", bd=2, relief="flat")
        self.lblLocal = tk.Label(win, text="Local:", bd=2, relief="flat")
        self.lblDescricao = tk.Label(win, text="Descrição:", bd=2, relief="flat")

        self.txtCodigo = tk.Entry(bd=2, relief="sunken")
        self.txtLocal = tk.Entry(bd=2, relief="sunken")
        self.txtDescricao = tk.Entry(bd=2, relief="sunken")

        self.btnCadastrar = tk.Button(win, text="Cadastrar", command=self.fCadastrarChamado, cursor="hand2", relief="raised")
        self.btnAtualizar = tk.Button(win, text="Atualizar", command=self.fAtualizarChamado, cursor="hand2", relief="raised")
        self.btnFinalizar = tk.Button(win, text="Finalizar", command=self.fFinalizarChamado, cursor="hand2", relief="raised")
        self.btnLimpar = tk.Button(win, text="Limpar", command=self.fLimparTela, cursor="hand2", relief="raised")
        self.btnDeletar = tk.Button(win, text="Deletar", command=self.fDeletarChamado, cursor="hand2", relief="raised")

        self.dadosColunas = ("CODIGO", "LOCAL", "DESCRICAO", "ABERTURA", "FECHAMENTO")

        self.treeChamados = ttk.Treeview(win,
                                         columns=self.dadosColunas,
                                         selectmode="browse")

        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeChamados.yview)
        self.verscrlbar.pack(side="right", fill="x")

        self.treeChamados.configure(yscrollcommand=self.verscrlbar.set)

        self.treeChamados.heading("CODIGO", text="Código", anchor="w")
        self.treeChamados.heading("LOCAL", text="Local", anchor="w")
        self.treeChamados.heading("DESCRICAO", text="Descrição", anchor="w")
        self.treeChamados.heading("ABERTURA", text="Abertura", anchor="w")
        self.treeChamados.heading("FECHAMENTO", text="Fechamento", anchor="w")

        self.treeChamados.column("CODIGO", minwidth=0, width=80, stretch=tk.NO)
        self.treeChamados.column("LOCAL", minwidth=0, width=150, stretch=tk.YES)
        self.treeChamados.column("DESCRICAO", minwidth=0, width=150, stretch=tk.YES)
        self.treeChamados.column("ABERTURA", minwidth=0, width=150, stretch=tk.YES)
        self.treeChamados.column("FECHAMENTO", minwidth=0, width=150, stretch=tk.YES)

        self.treeChamados.pack(padx=10, pady=10)

        self.treeChamados.bind("<<TreeviewSelect>>",
                               self.fApresentarChamadosSelecionados)

        self.lblCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lblLocal.place(x=100, y=100)
        self.txtLocal.place(x=250, y=100)

        self.lblDescricao.place(x=100, y=150)
        self.txtDescricao.place(x=250, y=150)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnFinalizar.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
        self.btnDeletar.place(x=500, y=200)

        self.treeChamados.place(x=100, y=300)
        self.verscrlbar.place(x=980, y=300, height=225)
        self.fCarregarDadosIniciais()

    def fApresentarChamadosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeChamados.selection():
            item = self.treeChamados.item(selection)
            codigo, local, descricao = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtLocal.insert(0, local)
            self.txtDescricao.insert(0, descricao)

    def fLimparTela(self):
        try:
            print("***** dados disponíveis *****")
            self.txtCodigo.delete(0, tk.END)
            self.txtLocal.delete(0, tk.END)
            self.txtDescricao.delete(0, tk.END)
            print("Campos Limpos!")
        except Exception as e:
            print("Não foi possível limpar os campos.")
            print(f"Erro: {e}")

    def fCarregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            chamados = self.objetoDB.selecionarDados()
            print("***** dados disponíveis no BD *****")
            for item in chamados:
                codigo = item[0]
                local = item[1]
                descricao = item[2]
                abertura = item[3]
                fechamento = item[4]
                print("Código = ", codigo)
                print("Local = ", local)
                print("Descrição = ", descricao)
                print("Abertura = ", abertura)
                print("Fechamento = ", fechamento)

                self.treeChamados.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo, local, descricao, abertura, fechamento))
                self.iid = self.iid + 1
                self.id = self.id + 1
                print("***** Dados da Base *****")
        except Exception as e:
            print("Ainda não existem dados para carregar")
            print(f"Erro: {e}")

    def fLerCampos(self):
        try:
            print("***** dados disponíveis *****")
            codigo = int(self.txtCodigo.get())
            print("codigo", codigo)
            local = self.txtLocal.get()
            print("local", local)
            descricao = self.txtDescricao.get()
            print("descricao", descricao)
        except Exception as e:
            print("Não foi possível ler os dados")
            print(f"Erro: {e}")
        return codigo, local, descricao

    def fCadastrarChamado(self):
        try:
            codigo, local, descricao = self.fLerCampos()
            now = datetime.now().strftime("%Y-%m-%d")
            self.objetoDB.inserirChamado(codigo, local, descricao, now)
            self.treeChamados.insert('', "end",
                                     iid=self.iid,
                                     values=(codigo, local, descricao, now))
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.fLimparTela()
            print("Chamado cadastrado com sucesso!")
        except Exception as e:
            print("Não foi possível fazer o cadastro.")
            print(f"Erro: {e}")

    def fAtualizarChamado(self):
        try:
            codigo, local, descricao = self.fLerCampos()
            self.objetoDB.atualizarChamado(codigo, local, descricao)

            self.treeChamados.delete(*self.treeChamados.get_children())
            self.fCarregarDadosIniciais()
            self.fLimparTela()
            print("Chamado atualizado com sucesso!")
        except Exception as e:
            print("Não foi possível fazer a atualização.")
            print(f"Erro: {e}")

    def fFinalizarChamado(self):
        try:
            codigo, local, descricao = self.fLerCampos()
            self.objetoDB.finalizarChamado(codigo)
            self.treeChamados.delete(*self.treeChamados.get_children())
            self.fCarregarDadosIniciais()
            self.fLimparTela()
            print("Chamado finalizado com sucesso!")
        except Exception as e:
            print("Não foi possível finalizar o chamado.")
            print(f"Erro: {e}")

    def fDeletarChamado(self):
        try:
            resposta = messagebox.askyesno("Confirmação", "Você tem certeza que quer deletar o item?")
            if resposta:
                codigo, local, descricao = self.fLerCampos()
                self.objetoDB.deletarChamado(codigo)
                self.treeChamados.delete(*self.treeChamados.get_children())
                self.fCarregarDadosIniciais()
                self.fLimparTela()
                print("Chamado deletado com sucesso!")
            else:
                messagebox.showinfo("Cancelado", "A ação foi cancelada")
        except Exception as e:
            print(f"Erro: {e}")



janela = tk.Tk()
principal = Main(janela)
janela.title("Controle de Chamados")
janela.geometry("1000x600+10+10")
janela.configure(bg="#87CEFA")

style = ttk.Style()

style.theme_use("default")

style.configure("Treeview",
                background="#ADD8E6",
                fieldbackground="#F0F8FF", )
janela.mainloop()
