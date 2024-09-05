from tkinter import *
from tkinter import ttk
from connect_db import ConnectDB
from ver_retorno import VerRetorno

class EstoqueRemessa():

    def __init__(self, nfe_remessa) -> None:
        self.nfe_remessa = nfe_remessa
        self.app3 = Toplevel()
        self.nfe = IntVar()
        self.cliente = StringVar()
        self.dt_emissao = StringVar()
        self.dt_limite = StringVar()
        self.volumes = IntVar()
        self.peso = DoubleVar()
        self.status = StringVar()
        self.vol_est = IntVar()
        self.peso_est = DoubleVar()
        self.app3.geometry("800x700+500+10")
        self.app3.resizable(width=False, height=False)
        self.app3.title('Estoque de Remessa')
        self.style_app()
        self.frame_app()
        self.widgets_app()
        self.treeview_remessa()
        self.treeview_estoque()
        self.treeview_retornos()
        self.position_grid()
        self.open_remessa()
        self.listar_retornos()
        self.carregar_estoque()
        self.app3.mainloop() # excluir
    
    def style_app(self):
        ttk.Style().configure('T.TLabel',
                              font=('calibri', 15, 'bold'),
                              foreground='#4C5C57')
        ttk.Style().configure('Click.TLabel',
                              font=('calibri', 12, 'bold'),
                              foreground='#4C5C57')
        ttk.Style().configure('L.TLabel',
                              font=('calibri', 12))
    
    def frame_app(self):
        self.frm1 = ttk.Frame(self.app3, borderwidth=1, relief='solid')
        self.frm2 = ttk.Frame(self.app3)
        self.frm3 = ttk.Frame(self.app3, borderwidth=1, relief='solid')
        self.frm4 = ttk.Frame(self.app3)
        self.frm5 = ttk.Frame(self.app3, borderwidth=1, relief='solid')
        self.frm6 = ttk.Frame(self.app3)
    
    def widgets_app(self):
        self.label_nfe = ttk.Label(self.frm1, text='NFe Remessa: ', style='L.TLabel')
        self.text_nfe = ttk.Label(self.frm1, textvariable=self.nfe, style='Click.TLabel')
        self.label_cliente = ttk.Label(self.frm1, text='Cliente: ', style='L.TLabel')
        self.text_cliente = ttk.Label(self.frm1, textvariable=self.cliente, style='Click.TLabel')
        self.label_dt_emissao = ttk.Label(self.frm1, text='Data Emissão: ', style='L.TLabel')
        self.text_dt_emissao = ttk.Label(self.frm1, textvariable=self.dt_emissao, style='Click.TLabel')
        self.label_dt_limite = ttk.Label(self.frm1, text='Data Limite: ', style='L.TLabel')
        self.text_dt_limite = ttk.Label(self.frm1, textvariable=self.dt_limite, style='Click.TLabel')
        self.label_volumes = ttk.Label(self.frm1, text='Volumes: ', style='L.TLabel')
        self.text_volumes = ttk.Label(self.frm1, textvariable=self.volumes, style='Click.TLabel')
        self.label_peso = ttk.Label(self.frm1, text='Peso: ', style='L.TLabel')
        self.text_peso = ttk.Label(self.frm1, textvariable=self.peso, style='Click.TLabel')
        self.label_status = ttk.Label(self.frm1, text='Status: ', style='L.TLabel')
        self.text_status = ttk.Label(self.frm1, textvariable=self.status, style='Click.TLabel')

        # FRAME 3
        self.label_estoque = ttk.Label(self.frm3, text='ESTOQUE:', style='T.TLabel')
        self.label_vol_est = ttk.Label(self.frm3, text='Volumes:', style='L.TLabel')
        self.txt_vol_est = ttk.Label(self.frm3, textvariable=self.vol_est, style='Click.TLabel')
        self.label_peso_est = ttk.Label(self.frm3, text='Peso:', style='L.TLabel')
        self.txt_peso_est = ttk.Label(self.frm3, textvariable=self.peso_est, style='Click.TLabel')

        # FRAME 5
        self.label_retornos = ttk.Label(self.frm5, text='RETORNOS EMITIDOS:', style='T.TLabel')
        self.label_click = ttk.Label(self.frm6,
                                     text='<< Clique para obter mais detalhes.',
                                     style='Click.TLabel')
    
    def treeview_remessa(self):
        self.tv_remessa = ttk.Treeview(self.frm2,
                                       columns=('item',
                                                'cod_produto',
                                                'descricao','un',
                                                'qtd', 'vl_unit'),
                                                show='headings',
                                                height=6)
        self.tv_remessa.column('item', minwidth=10, width=50, anchor=CENTER)
        self.tv_remessa.column('cod_produto', minwidth=10, width=100, anchor=CENTER)
        self.tv_remessa.column('descricao', minwidth=10, width=350)
        self.tv_remessa.column('un', minwidth=10, width=68, anchor=CENTER)
        self.tv_remessa.column('qtd', minwidth=10, width=110, anchor=CENTER)
        self.tv_remessa.column('vl_unit', minwidth=10, width=100, anchor=CENTER)
        self.tv_remessa.heading('item', text='Item')
        self.tv_remessa.heading('cod_produto', text='Código')
        self.tv_remessa.heading('descricao', text='Descrição')
        self.tv_remessa.heading('un', text='UN')
        self.tv_remessa.heading('qtd', text='Quantidade')
        self.tv_remessa.heading('vl_unit', text='Valor Unit.')

    def treeview_estoque(self):
        self.tv_estoque = ttk.Treeview(self.frm4,
                                       columns=('item',
                                                'cod_produto',
                                                'descricao','un',
                                                'qtd', 'vl_unit'),
                                                show='headings',
                                                height=6)
        self.tv_estoque.column('item', minwidth=10, width=50, anchor=CENTER)
        self.tv_estoque.column('cod_produto', minwidth=10, width=100, anchor=CENTER)
        self.tv_estoque.column('descricao', minwidth=10, width=350)
        self.tv_estoque.column('un', minwidth=10, width=68, anchor=CENTER)
        self.tv_estoque.column('qtd', minwidth=10, width=110, anchor=CENTER)
        self.tv_estoque.column('vl_unit', minwidth=10, width=100, anchor=CENTER)
        self.tv_estoque.heading('item', text='Item')
        self.tv_estoque.heading('cod_produto', text='Código')
        self.tv_estoque.heading('descricao', text='Descrição')
        self.tv_estoque.heading('un', text='UN')
        self.tv_estoque.heading('qtd', text='Quantidade')
        self.tv_estoque.heading('vl_unit', text='Valor Unit.')
    
    def treeview_retornos(self):
        self.tv_retornos = ttk.Treeview(self.frm6,
                                       columns=('nfe_retorno',
                                                'data_emissao'),
                                                show='headings',
                                                height=6)
        self.tv_retornos.column('nfe_retorno', minwidth=10, width=100, anchor=CENTER)
        self.tv_retornos.column('data_emissao', minwidth=10, width=100, anchor=CENTER)
        self.tv_retornos.heading('nfe_retorno', text='NFe Retornos')
        self.tv_retornos.heading('data_emissao', text='Data Emissão')
        self.tv_retornos.bind('<ButtonRelease-1>', self.select_retorno)
    
    def select_retorno(self, a):
        selecao = self.tv_retornos.item(self.tv_retornos.selection())
        nfe_retorno = selecao['values'][0]
        VerRetorno(nfe_retorno)
        

    def position_grid(self):
        # FRAME 1
        self.frm1.place(x=10, y=10, width=780, height=140)
        self.label_nfe.grid(row=0, column=0, padx=(20,0), pady=(20,0), sticky=W)
        self.text_nfe.grid(row=0, column=1, pady=(20,0), sticky=W)
        self.label_status.grid(row=0, column=2, padx=(100,0), pady=(20,0), sticky=W)
        self.text_status.grid(row=0, column=3, pady=(20,0), sticky=W)
        self.label_cliente.grid(row=1, column=0, padx=(20,0), sticky=W)
        self.text_cliente.grid(row=1, column=1, sticky=W)
        self.label_dt_emissao.grid(row=2, column=0, padx=(20,0), sticky=W)
        self.text_dt_emissao.grid(row=2, column=1, sticky=W)
        self.label_dt_limite.grid(row=2, column=2, padx=(100,0), sticky=W)
        self.text_dt_limite.grid(row=2, column=3, sticky=W)
        self.label_volumes.grid(row=3, column=0, padx=(20,0), sticky=W)
        self.text_volumes.grid(row=3, column=1, sticky=W)
        self.label_peso.grid(row=3, column=2, padx=(100,0), sticky=W)
        self.text_peso.grid(row=3, column=3, sticky=W)
        # FRAME 2
        self.frm2.place(x=10, y=140, width=780, height=148)
        self.tv_remessa.grid(row=0, column=0)

        # FRAME 3
        self.frm3.place(x=10, y=290, width=780, height=70)
        self.label_estoque.grid(row=0, column=0, padx=(20,0))
        self.label_vol_est.grid(row=1, column=0, padx=(20,0), pady=(10,0), sticky=W)
        self.txt_vol_est.grid(row=1, column=1, pady=(10,0), sticky=W)
        self.label_peso_est.grid(row=1, column=2, padx=(100,0), pady=(10,0))
        self.txt_peso_est.grid(row=1, column=3, pady=(10,0), sticky=W)

        # FRAME 4
        self.frm4.place(x=10, y=350, width=780, height=148)
        self.tv_estoque.grid(row=0, column=0)

        # FRAME 5
        self.frm5.place(x=10, y=500, width=202, height=25)
        self.label_retornos.grid(row=0, column=0, padx=(5,0))
        
        # FRAME 6 TV_RETORNOS
        self.frm6.place(x=10, y=524, width=780, height=150)
        self.tv_retornos.grid(row=0, column=0)
        self.label_click.grid(row=0, column=1, padx=(20,0))
    
    def open_remessa(self):
        try:
            db = ConnectDB()

            sql = '''
            SELECT nfe_remessa,
            cliente, data_emissao,
            volumes, peso,
            (data_emissao + 180) as data_limite,
            status
            FROM remessa
            WHERE nfe_remessa = %s'''

            tp_dados = (self.nfe_remessa,)
            dados = db.select_db(sql, tp_dados)
            
            self.nfe.set(dados[0][0])
            self.cliente.set(dados[0][1])
            self.dt_emissao.set(dados[0][2].strftime('%d/%m/%Y'))
            self.volumes.set(dados[0][3])
            self.peso.set(dados[0][4])
            self.dt_limite.set(dados[0][5].strftime('%d/%m/%Y'))
            self.status.set(dados[0][6])

            sql_itens = '''
            SELECT cod_produto,
            descricao, un,
            quantidade, valor_unitario
            FROM itemremessa
            WHERE nfe_remessa = %s'''

            itens = db.select_db(sql_itens, tp_dados)
            count = 1
            for (a, b, c, d, e) in itens:
                self.tv_remessa.insert('', END,
                    values=(count, a, b, c, d, e))
                count += 1
            
            db.close_db()

        except Exception as err:
            print(err)

    def carregar_estoque(self):
        try:
            db = ConnectDB()

            sql_volpeso = '''
            SELECT
	        (rm.volumes - COALESCE(SUM(rt.volumes), 0)) as total_volumes,
	        (rm.peso - COALESCE(SUM(rt.peso), 0)) as total_peso
            FROM remessa rm LEFT JOIN retorno rt USING(nfe_remessa)
            WHERE COALESCE(rt.nfe_remessa=%s, rm.nfe_remessa=%s)
            GROUP BY rm.volumes, rm.peso'''

            tp_volpeso = (self.nfe_remessa, self.nfe_remessa,)

            vol_peso = db.select_db(sql_volpeso, tp_volpeso)
            self.vol_est.set(vol_peso[0][0])
            self.peso_est.set(vol_peso[0][1])
                     
            sql_itens = '''
            SELECT cod_produto,
            descricao, un,
            quantidade, valor_unitario
            FROM estoqueremessa
            WHERE nfe_remessa = %s'''

            tp_dados = (self.nfe_remessa,)

            itens = db.select_db(sql_itens, tp_dados)
            count = 1
            for (a, b, c, d, e) in itens:
                self.tv_estoque.insert('', END,
                    values=(count, a, b, c, d, e))
                count += 1
            
            db.close_db()

        except Exception as err:
            print(err)  

    def listar_retornos(self):
        try:
            db = ConnectDB()

            sql = '''
            SELECT nfe_retorno,
            data_emissao
            FROM retorno
            WHERE nfe_remessa = %s'''

            tp_dados = (self.nfe_remessa,)

            dados = db.select_db(sql, tp_dados)
            
            for(a, b) in dados:
                self.tv_retornos.insert('', END,
                                values=(a,
                                        b.strftime('%d/%m/%Y')))
            
            db.close_db()

        except Exception as err:
            print(err)
