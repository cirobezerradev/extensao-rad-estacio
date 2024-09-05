from tkinter import *
from tkinter import ttk
from connect_db import ConnectDB
from cadastrar_retorno import CadastrarRetorno

class SelectRemessa():
    def __init__(self) -> None:
        self.app2 = Toplevel()
        self.app2.title('ESCOLHA REMESSA')
        self.app2.geometry('700x400+500+100')
        self.app2.resizable(width=False, height=False)
        self.style_app()
        self.frames_app()
        self.widgets_app()
        self.treeview_app()
        self.position_grid()
        self.select_remessas()
        self.remessa = 0

    def style_app(self):
        ttk.Style().configure('TLabel', font=('calibri', 15, 'bold'),
                              foreground='#4C5C57')

    def frames_app(self):
        self.frm1 = ttk.Frame(self.app2, borderwidth=1, relief='solid')
        self.frm2 = ttk.Frame(self.app2)
    
    def widgets_app(self):
        self.label_title = ttk.Label(self.frm1,
                                     text="Clique na Remessa referente ao retorno que deseja cadastrar.",
                                     style='TLabel')

    def treeview_app(self):
        self.tv2 = ttk.Treeview(self.frm2,
                                columns=('nfe', 'cliente',
                                'data_emissao', 'data_limite'),
                                show='headings', height=13)

        self.tv2.column('nfe', minwidth=10, width=100)
        self.tv2.column('cliente', minwidth=10, width=377)
        self.tv2.column('data_emissao', minwidth=10, width=100)
        self.tv2.column('data_limite', minwidth=10, width=100)
        self.tv2.heading('nfe', text='NFe')
        self.tv2.heading('cliente', text='Cliente')
        self.tv2.heading('data_emissao', text='Data Emissão')
        self.tv2.heading('data_limite', text='Data Limite')

        self.tv2.bind('<ButtonRelease-1>', self.seleciona_item)

    def seleciona_item(self, a):
        selecao = self.tv2.item(self.tv2.selection())
        self.ref_remessa = selecao['values'][0]
        CadastrarRetorno(self.ref_remessa)
        self.app2.destroy()

    def position_grid(self):
        # FRAME 1
        self.frm1.place(x=10, y=40, width=680, height=50)
        self.label_title.grid(row=1, column=1, padx=(70,0), pady=(10,0))
        # FRAME 2 TREEVIEW
        self.frm2.place(x=10, y=100, width=680, height=290)
        self.tv2.grid(row=0, column=0)
        self.tv2.grid_anchor(anchor=CENTER)
    
    # BUSCA NO BANCO DE DADOS OS DADOS PARA PREENCHER A TREEVIEW
    def select_remessas(self):
        db = ConnectDB()

        sql_select = '''SELECT nfe_remessa, cliente,
                            data_emissao,
                            (data_emissao + 180) as data_limite
                        FROM remessa
                        WHERE status=%s;'''
        status = ('PENDENTE',)
        
        self.lista = db.select_db(sql_select, status)
        
        for (a, b, c, d) in self.lista:
            self.tv2.insert('', END,
                            values=(a, b,
                                    c.strftime('%d/%m/%Y'),
                                    d.strftime('%d/%m/%Y')))
        
        db.close_db()
        