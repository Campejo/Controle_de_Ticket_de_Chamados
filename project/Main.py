import tkinter as tk
from datetime import datetime

from project.DB.AppDB import AppDB
from tkinter import ttk, messagebox


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Chamados")
        self.root.geometry("900x600")
        self.root.configure(bg="#F7F7F7")

        self.db = AppDB()

        # Variáveis para controle de IDs
        self.id = 0
        self.iid = 0

        # Estilo para a Treeview
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white",
                        font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Labels e Entrys
        self.lblCodigo = tk.Label(root, text="ID do Chamado:", bg="#F7F7F7", font=("Arial", 12))
        self.lblCodigo.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.txtCodigo = tk.Entry(root, font=("Arial", 12), bd=2)
        self.txtCodigo.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        self.lblLocal = tk.Label(root, text="Local:", bg="#F7F7F7", font=("Arial", 12))
        self.lblLocal.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.txtLocal = tk.Entry(root, font=("Arial", 12), bd=2)
        self.txtLocal.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        self.lblDescricao = tk.Label(root, text="Descrição:", bg="#F7F7F7", font=("Arial", 12))
        self.lblDescricao.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.txtDescricao = tk.Entry(root, font=("Arial", 12), bd=2)
        self.txtDescricao.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        # Botões
        self.btnCadastrar = tk.Button(root, text="Cadastrar", bg="#4CAF50", fg="white", font=("Arial", 12),
                                      command=self.fCadastrarChamado, cursor="hand2")
        self.btnCadastrar.grid(row=0, column=2, padx=5, pady=5)


        self.btnExcluir = tk.Button(root, text="Excluir", bg="#F44336", fg="white", font=("Arial", 12),
                                    command=self.fDeletarChamado, cursor="hand2")
        self.btnExcluir.grid(row=4, column=2, padx=5, pady=5)


        self.btnLimpar = tk.Button(root, text="Limpar", bg="#FF9800", fg="white", font=("Arial", 12),
                                   command=self.fLimparTela, cursor="hand2")
        self.btnLimpar.grid(row=2, column=2, padx=5, pady=5)


        self.btnAtualizar = tk.Button(root, text="Atualizar", bg="#2196F3", fg="white", font=("Arial", 12),
                                      command=self.fAtualizarChamado, cursor="hand2")
        self.btnAtualizar.grid(row=1, column=2, padx=5, pady=5)


        self.btnFinalizar = tk.Button(root, text="Finalizar", bg="#9C27B0", fg="white", font=("Arial", 12),
                                      command=self.fFinalizarChamado, cursor="hand2")
        self.btnFinalizar.grid(row=3, column=2, padx=5, pady=5)


        # Treeview
        self.dadosColunas = ("CODIGO", "LOCAL", "DESCRICAO", "ABERTURA", "FECHAMENTO")
        self.treeChamados = ttk.Treeview(root, columns=self.dadosColunas, show="headings", height=10)

        # Definindo as colunas
        self.treeChamados.heading("CODIGO", text="Código")
        self.treeChamados.heading("LOCAL", text="Local")
        self.treeChamados.heading("DESCRICAO", text="Descrição")
        self.treeChamados.heading("ABERTURA", text="Abertura")
        self.treeChamados.heading("FECHAMENTO", text="Fechamento")

        self.treeChamados.column("CODIGO", width=80, anchor="center")
        self.treeChamados.column("LOCAL", width=150, anchor="center")
        self.treeChamados.column("DESCRICAO", width=200, anchor="center")
        self.treeChamados.column("ABERTURA", width=100, anchor="center")
        self.treeChamados.column("FECHAMENTO", width=100, anchor="center")

        self.treeChamados.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # Bind para apresentar dados selecionados
        self.treeChamados.bind("<<TreeviewSelect>>", self.fApresentarChamadosSelecionados)

        # Barra de rolagem para a Treeview
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.treeChamados.yview)
        self.treeChamados.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=3, column=1, sticky="nse")

        # Configurando grid para expandir
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(3, weight=1)

        # Carregar dados iniciais
        self.fCarregarDadosIniciais()

    # Funções dos botões
    def fCadastrarChamado(self):
        try:
            codigo, local, descricao = self.fLerCampos()
            now = datetime.now().strftime("%Y-%m-%d")
            self.db.inserirChamado(codigo, local, descricao, now)
            self.treeChamados.insert('', "end",
                                     iid=self.iid,
                                     values=(codigo, local, descricao, now, ''))
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
            self.db.atualizarChamado(codigo, local, descricao)

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
            fechamento = datetime.now().strftime("%Y-%m-%d")
            self.db.finalizarChamado(codigo)
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
                self.db.deletarChamado(codigo)
                self.treeChamados.delete(*self.treeChamados.get_children())
                self.fCarregarDadosIniciais()
                self.fLimparTela()
                print("Chamado deletado com sucesso!")
            else:
                messagebox.showinfo("Cancelado", "A ação foi cancelada")
        except Exception as e:
            print(f"Erro: {e}")

    def fCarregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            chamados = self.db.selecionarDados()
            for item in chamados:
                codigo = item[0]
                local = item[1]
                descricao = item[2]
                abertura = item[3]
                fechamento = item[4]

                self.treeChamados.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo, local, descricao, abertura, fechamento))
                self.iid += 1
                self.id += 1
        except Exception as e:
            print("Ainda não existem dados para carregar")
            print(f"Erro: {e}")

    def fApresentarChamadosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeChamados.selection():
            item = self.treeChamados.item(selection)
            codigo, local, descricao, abertura, fechamento = item["values"][0:5]
            self.txtCodigo.insert(0, codigo)
            self.txtLocal.insert(0, local)
            self.txtDescricao.insert(0, descricao)

    def fLerCampos(self):
        try:
            codigo = int(self.txtCodigo.get())
            local = self.txtLocal.get()
            descricao = self.txtDescricao.get()
        except Exception as e:
            print("Não foi possível ler os dados")
            print(f"Erro: {e}")
        return codigo, local, descricao

    def fLimparTela(self):
        try:
            self.txtCodigo.delete(0, tk.END)
            self.txtLocal.delete(0, tk.END)
            self.txtDescricao.delete(0, tk.END)
        except Exception as e:
            print("Não foi possível limpar os campos.")
            print(f"Erro: {e}")


# Inicialização da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()