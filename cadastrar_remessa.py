from cadastrosRR import CadastrosRR
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from DomRemessa import DomRemessa
from connect_db import ConnectDB
import psycopg2
from psycopg2 import errors

class CadastrarRemessa(CadastrosRR):

    def __init__(self) -> None:
        self.status = 'PENDENTE'
        super().__init__()
        self.app1.title('Cadastro de Remessa')
        self.position_grid()

    def widgets_app(self):
        super().widgets_app()
        self.label_dt_limite = ttk.Label(self.frm2, text='Data Limite: ',
                                         style='Red.TLabel')
        self.etr_dt_limite = ttk.Entry(self.frm2,
                                       textvariable=self.data_limite,
                                       width=25,
                                       state=DISABLED)

    def position_grid(self):
        super().position_grid()
        # FRAME 1
        # FRAME 2
        self.label_dt_limite.grid(row=1, column=2, sticky=W, padx=(10, 0))
        self.etr_dt_limite.grid(row=1, column=3, sticky=W)
        # FRAME 3

    def abrir_xml(self):
        url_xml = filedialog.askopenfilename(parent=self.app1)
        self.remessa = DomRemessa(url_xml)
        self.nfe.set(self.remessa.num_nfe)
        self.data_emissao.set(self.remessa.data_emissao)
        self.data_limite.set(self.remessa.data_limite)
        self.cliente.set(self.remessa.cliente)
        self.volumes.set(self.remessa.volumes)
        self.peso.set(self.remessa.peso)
        self.cfop.set(self.remessa.status_cfop())
        # VERIFICAÇÃO DE CFOP 6901
        if not self.cfop.get():
            messagebox.showinfo(title='ATENÇÃO',
                                message='Por favor insira uma XML de Remessa.',
                                parent=self.app1)
            self.limpar()
            return None
        # Inserção dos Itens na Treeview
        count = 1
        for (a, b, c, d, e) in self.remessa.itens:
            self.cod_produto = a
            self.descricao = b
            self.un = c
            self.quantidade = d
            self.valor_unitario = e
            self.tv.insert('', 'end', values=(count, a, b, c, d, e))
            count += 1

        self.app1.update()
        self.app1.update_idletasks()

    def salvar(self):
        super().salvar()

        try:
            db = ConnectDB()

            # SCRIPT SQL INSERIR DADOS NA TABELA REMESSA
            sql_remessa = '''INSERT INTO remessa(nfe_remessa,
                        data_emissao, cliente, volumes, peso, status)
                        VALUES (%s, %s, %s, %s, %s, %s);'''
            # TUPLA DE VALORES P/ INSERÇÃO
            tp_remessa = (self.nfe.get(), self.data_emissao.get(),
                            self.cliente.get(), self.volumes.get(),
                            self.peso.get(), self.status)
            
            db.insert_db(sql_remessa, tp_remessa)

            # SCRIPT SQL INSERIR DADOS NA TABELA ITEMREMESSA
            sql_itemremessa = '''INSERT INTO itemremessa(cod_produto,
                            descricao, un, quantidade, valor_unitario,
                            nfe_remessa)
                            VALUES (%s, %s, %s, %s, %s, %s);'''
            sql_estoqueremessa = '''INSERT INTO estoqueremessa(cod_produto,
                            descricao, un, quantidade, valor_unitario,
                            nfe_remessa)
                            VALUES (%s, %s, %s, %s, %s, %s);'''
            
            # ITERAÇÃO P TUPLA DE VALORES PARA INSERÇÃO
            for (a, b, c, d, e) in self.remessa.itens:
                tp_itens = (a, b, c, d, e, self.nfe.get())
                # INSERSÃO NA TABELA ITEMREMESSA
                db.insert_db(sql_itemremessa, tp_itens)
                db.insert_db(sql_estoqueremessa, tp_itens)
            
            db.conn.commit()

            db.close_db()

        except psycopg2.errors.UniqueViolation:
            msg = f'Essa remessa {self.nfe.get()} já foi cadastrada!'
            messagebox.showinfo(
                title="ATENÇÃO", message=msg, parent=self.app1)
            self.limpar()
            return None

        messagebox.showinfo(title='INFORMAÇÃO',
            message=f'REMESSA {self.nfe.get()} CADASTRADA COM SUCESSO.',
            parent=self.app1)
        return self.limpar()

    def limpar(self):
        super().limpar()
        self.data_limite.set('')
        self.tv.delete(*self.tv.get_children())
