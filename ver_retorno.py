from tkinter import *
from tkinter import ttk
from connect_db import ConnectDB

class VerRetorno:
    def __init__(self, retorno) -> None:
        self.retorno = retorno
        self.app4 = Toplevel()
        self.nfe_retorno = IntVar()
        self.cliente = StringVar()
        self.data_emissao = StringVar()
        self.volumes = IntVar()
        self.peso = DoubleVar()
        self.app4.geometry('800x315+500+10')
        self.app4.resizable(width=False, height=False)
        self.app4.title('Retorno')
        self.style_app()
        self.frame_app()
        self.widgets_app()
        self.treeview_itens()
        self.position_grid()
        self.carregar_retorno()
        self.app4.mainloop()
    
    def style_app(self):
        ttk.Style().configure('Click.TLabel',
                              font=('calibri', 12, 'bold'),
                              foreground='#4C5C57')
        ttk.Style().configure('L.TLabel',
                              font=('calibri', 12))
    
    def frame_app(self):
        self.frm7 = ttk.Frame(self.app4, borderwidth=1, relief='solid')
        self.frm8 = ttk.Frame(self.app4)
    
    def widgets_app(self):
        self.label_nfe = ttk.Label(self.frm7, text='NFe Retorno:', style='L.TLabel')
        self.txt_nfe = ttk.Label(self.frm7, textvariable=self.nfe_retorno,
                                 style='Click.TLabel')
        self.label_cliente = ttk.Label(self.frm7, text='Cliente:', style='L.TLabel')
        self.txt_cliente = ttk.Label(self.frm7, textvariable=self.cliente,
                                     style='Click.TLabel')
        self.label_dt_emissao = ttk.Label(self.frm7, text='Data Emissão: ', style='L.TLabel')
        self.txt_dt_emissao = ttk.Label(self.frm7, textvariable=self.data_emissao,
                                        style='Click.TLabel')
        self.label_volumes = ttk.Label(self.frm7, text='Volumes: ', style='L.TLabel')
        self.txt_volumes = ttk.Label(self.frm7, textvariable=self.volumes,
                                     style='Click.TLabel')
        self.label_peso = ttk.Label(self.frm7, text='Peso: ', style='L.TLabel')
        self.txt_peso = ttk.Label(self.frm7, textvariable=self.peso,
                                  style='Click.TLabel')

    def treeview_itens(self):
        self.tv_itens = ttk.Treeview(self.frm8,
                                     columns=('item',
                                              'cod_produto',
                                              'descricao',
                                              'un',
                                              'qtd',
                                              'vl_unit'),
                                     show='headings',
                                     height=8)
        
        self.tv_itens.column('item', minwidth=10, width=50, anchor=CENTER)
        self.tv_itens.column('cod_produto', minwidth=10, width=100, anchor=CENTER)
        self.tv_itens.column('descricao', minwidth=10, width=350)
        self.tv_itens.column('un', minwidth=10, width=68, anchor=CENTER)
        self.tv_itens.column('qtd', minwidth=10, width=110, anchor=CENTER)
        self.tv_itens.column('vl_unit', minwidth=10, width=100, anchor=CENTER)
        self.tv_itens.heading('item', text='Item')
        self.tv_itens.heading('cod_produto', text='Código')
        self.tv_itens.heading('descricao', text='Descrição')
        self.tv_itens.heading('un', text='UN')
        self.tv_itens.heading('qtd', text='Quantidade')
        self.tv_itens.heading('vl_unit', text='Valor Unit.')

    def position_grid(self):
        # FRAME 1
        self.frm7.place(x=10, y=10, width=780, height=120)
        self.label_nfe.grid(row=0, column=0, padx=(20,0), pady=(10,0), sticky=W)
        self.txt_nfe.grid(row=0, column=1, padx=(10,0), pady=(10,0), sticky=W)
        self.label_cliente.grid(row=1, column=0, padx=(20,0), sticky=W)
        self.txt_cliente.grid(row=1, column=1, padx=(10,0), sticky=W)
        self.label_dt_emissao.grid(row=2, column=0, padx=(20,0), sticky=W)
        self.txt_dt_emissao.grid(row=2, column=1, padx=(10,0), sticky=W)
        self.label_volumes.grid(row=3, column=0, padx=(20,0), sticky=W)
        self.txt_volumes.grid(row=3, column=1, padx=(10,0), sticky=W)
        self.label_peso.grid(row=3, column=2, padx=(20,0), sticky=W)
        self.txt_peso.grid(row=3, column=3, padx=(10,0), sticky=W)
        # FRAME 2
        self.frm8.place(x=10, y=120, width=780, height=190)
        self.tv_itens.grid(row=0, column=0)
    
    def carregar_retorno(self):
        try:
            db = ConnectDB()

            sql_retorno = '''
            SELECT nfe_retorno,
            cliente, data_emissao,
            volumes, peso
            FROM retorno
            where nfe_retorno = %s'''

            tp_retorno = (self.retorno,)

            dados_retorno = db.select_db(sql_retorno, tp_retorno)

            self.nfe_retorno.set(dados_retorno[0][0])
            self.cliente.set(dados_retorno[0][1])
            self.data_emissao.set(dados_retorno[0][2].strftime('%d/%m/%Y'))
            self.volumes.set(dados_retorno[0][3])
            self.peso.set(dados_retorno[0][4])

            sql_itens = '''
            SELECT *
            FROM itemretorno
            WHERE nfe_retorno = %s'''

            lista_itens = db.select_db(sql_itens, tp_retorno)
            count = 1
            for (a, b, c, d, e, f) in lista_itens:
                self.tv_itens.insert('', END,
                                     values=(count, a,
                                             b, c, d, e))
                count += 1
            
            db.close_db()

        except Exception as err:
            print(err)
   

