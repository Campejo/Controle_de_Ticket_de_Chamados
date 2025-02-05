import tkinter as tk
from datetime import datetime
from model.AppDB import AppDB
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

        # Frame para as labels e entradas de texto
        frame_labels = tk.Frame(root, bg="#F7F7F7")
        frame_labels.pack(pady=10, anchor="center", padx=20)

        # Labels e Entrys
        self.lblCodigo = tk.Label(frame_labels, text="ID do Chamado:", bg="#F7F7F7", font=("Arial", 12))
        self.lblCodigo.pack(anchor="w")
        self.txtCodigo = tk.Entry(frame_labels, font=("Arial", 12), bd=2)
        self.txtCodigo.pack(fill="x", pady=5)

        self.lblLocal = tk.Label(frame_labels, text="Local:", bg="#F7F7F7", font=("Arial", 12))
        self.lblLocal.pack(anchor="w")
        self.txtLocal = tk.Entry(frame_labels, font=("Arial", 12), bd=2)
        self.txtLocal.pack(fill="x", pady=5)

        self.lblDescricao = tk.Label(frame_labels, text="Descrição:", bg="#F7F7F7", font=("Arial", 12))
        self.lblDescricao.pack(anchor="w")
        self.txtDescricao = tk.Entry(frame_labels, font=("Arial", 12), bd=2)
        self.txtDescricao.pack(fill="x", pady=5)

        # Frame para os botões
        frame_botoes = tk.Frame(root, bg="#F7F7F7")
        frame_botoes.pack(pady=10)

        # Botões dispostos horizontalmente
        self.btnCadastrar = tk.Button(frame_botoes, text="Cadastrar", bg="#28a745", fg="white", font=("Arial", 12),
                                      command=self.fCadastrarChamado, cursor="hand2")
        self.btnCadastrar.pack(side=tk.LEFT, padx=10)

        self.btnAtualizar = tk.Button(frame_botoes, text="Atualizar", bg="#007bff", fg="white", font=("Arial", 12),
                                      command=self.fAtualizarChamado, cursor="hand2")
        self.btnAtualizar.pack(side=tk.LEFT, padx=10)

        self.btnLimpar = tk.Button(frame_botoes, text="Limpar Campos", bg="#fd7e14", fg="white", font=("Arial", 12),
                                   command=self.fLimparTela, cursor="hand2")
        self.btnLimpar.pack(side=tk.LEFT, padx=10)

        self.btnFinalizar = tk.Button(frame_botoes, text="Finalizar", bg="#6f42c1", fg="white", font=("Arial", 12),
                                      command=self.fFinalizarChamado, cursor="hand2")
        self.btnFinalizar.pack(side=tk.LEFT, padx=10)

        self.btnExcluir = tk.Button(frame_botoes, text="Excluir", bg="#dc3545", fg="white", font=("Arial", 12),
                                    command=self.fDeletarChamado, cursor="hand2")
        self.btnExcluir.pack(side=tk.LEFT, padx=10)

        # Frame para a Treeview e Scrollbar
        frame_tree = tk.Frame(root)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Treeview
        self.dadosColunas = ("CODIGO", "LOCAL", "DESCRICAO", "ABERTURA", "FECHAMENTO")
        self.treeChamados = ttk.Treeview(frame_tree, columns=self.dadosColunas, show="headings", height=10)

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

        self.treeChamados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem para a Treeview
        self.scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.treeChamados.yview)
        self.treeChamados.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind para apresentar dados selecionados
        self.treeChamados.bind("<<TreeviewSelect>>", self.fApresentarChamadosSelecionados)

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


