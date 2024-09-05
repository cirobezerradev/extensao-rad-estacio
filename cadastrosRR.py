from tkinter import *
from tkinter import ttk
from connect_db import ConnectDB


class CadastrosRR:
    def __init__(self) -> None:
        # VARIÁVEIS DE CONTROLE
        self.nfe = IntVar()
        self.data_emissao = StringVar()
        self.data_limite = StringVar()
        self.cliente = StringVar()
        self.volumes = IntVar()
        self.peso = DoubleVar()
        self.cfop = BooleanVar()
        self.cod_produto = 0
        self.descricao = ''
        self.un = ''
        self.quantidade = 0.0
        self.valor_unitario = 0.0

        # CARREGAMENTO DA JANELA APP1
        self.app1 = Toplevel()
        self.app1.geometry('700x600+500+100')
        self.app1.resizable(width=False, height=False)
        self.w_styles()
        self.frames_app()
        self.widgets_app()
        self.treeview_app()

    # ESTILOS DOS WIDGETS
    def w_styles(self):
        ttk.Style().configure('CRR.TButton', padding=5, font=('roboto', 12, 'bold'),
                              foreground='#4C5C57', relief='raised', width=10)
        ttk.Style().configure('C.TLabel', font=('calibri', 12, 'bold'))
        ttk.Style().configure('Red.TLabel', font=('calibri', 12, 'bold'), foreground='#FF0004')

    def frames_app(self):
        # FRAME ABRIR XML
        self.frm1 = ttk.Frame(self.app1, borderwidth=1, relief='solid')
        # FRAME DADOS DA NFE
        self.frm2 = ttk.Frame(self.app1, borderwidth=1, relief='solid')
        # FRAME TREEVIEW - ITENS DA NFE
        self.frm3 = ttk.Frame(self.app1, borderwidth=1, relief='solid')
        # FRAME BOTÕES SALVAR, LIMPAR E SAIR
        self.frm4 = ttk.Frame(self.app1, borderwidth=1, relief='solid')
    
    def widgets_app(self):
        # Botão Abrir XML
        self.btn1 = ttk.Button(self.frm1, text='Abrir XML',
                               style='CRR.TButton', command=self.abrir_xml)
        self.label_b1 = ttk.Label(self.frm1,
                                  text=' < Clique para carregar o XML da NFe',
                                  style='C.TLabel')

        # Dados que serão carregados da XML
        self.label_nfe = ttk.Label(self.frm2, text='NFe: ')
        self.etr_nfe = ttk.Entry(self.frm2, state=DISABLED,
                                 textvariable=self.nfe)
        self.label_dt_emissao = ttk.Label(self.frm2, text='Data de Emissão: ')
        self.etr_dt_emissao = ttk.Entry(self.frm2, state=DISABLED,
                                        textvariable=self.data_emissao)
        self.label_cliente = ttk.Label(self.frm2, text='Cliente: ')
        self.etr_cliente = ttk.Entry(self.frm2, width=60, state=DISABLED,
                                     textvariable=self.cliente)
        self.label_volumes = ttk.Label(self.frm2, text='Volumes: ')
        self.etr_volumes = ttk.Entry(self.frm2, state=DISABLED,
                                     textvariable=self.volumes)
        self.label_peso = ttk.Label(self.frm2, text='Peso: ')
        self.etr_peso = ttk.Entry(self.frm2, state=DISABLED,
                                  textvariable=self.peso)
        
        # FRAME 4 - BOTÕES SALVAR, LIMPAR E SAIR
        self.btn_salvar = ttk.Button(self.frm4, text='SALVAR 💾', style='CRR.TButton', command=self.salvar)
        self.btn_limpar = ttk.Button(self.frm4, text='LIMPAR 🧹', style='CRR.TButton', command=self.limpar)
        self.btn_sair = ttk.Button(self.frm4, text='SAIR 🚪', style='CRR.TButton', command=self.sair)

    # WIDGET TREEVIEW - LISTA DE ITENS DA NFE
    def treeview_app(self):
        self.tv = ttk.Treeview(self.frm3,
                               columns=('item', 'cod_produto', 'descricao',
                                        'un', 'qtd', 'vl_unit'),
                               show='headings')
        self.tv.column('item', minwidth=10, width=50)
        self.tv.column('cod_produto', minwidth=10, width=100)
        self.tv.column('descricao', minwidth=10, width=280)
        self.tv.column('un', minwidth=10, width=50)
        self.tv.column('qtd', minwidth=10, width=100)
        self.tv.column('vl_unit', minwidth=10, width=100)
        self.tv.heading('item', text='Item')
        self.tv.heading('cod_produto', text='Código')
        self.tv.heading('descricao', text='Descrição')
        self.tv.heading('un', text='UN')
        self.tv.heading('qtd', text='Quantidade')
        self.tv.heading('vl_unit', text='Valor Unit.')
    
    # POSICIONAMENTO DOS WIDGETS NA GRID
    def position_grid(self):
        # FRAME 1 - BOTÃO DE ABRIR XML
        self.frm1.place(x=10, y=10, width=680, height=100)
        self.btn1.grid(row=0, column=0, padx=(30, 0), pady=(30,0))
        self.label_b1.grid(row=0, column=1, pady=(30,0))
        # FRAME 2 - DADOS DA NFE
        self.frm2.place(x=10, y=120, width=680, height=180)
        self.label_nfe.grid(row=0, column=0, padx=(10, 0),
                            pady=(10, 0), sticky=W)
        self.etr_nfe.grid(row=0, column=1, pady=(10, 0), sticky=W)
        self.label_dt_emissao.grid(row=1, column=0, padx=(10, 0), sticky=W)
        self.etr_dt_emissao.grid(row=1, column=1, sticky=W)
        self.label_cliente.grid(row=2, column=0, padx=(10, 0), sticky=W)
        self.etr_cliente.grid(row=2, column=1, sticky=W, columnspan=100)
        self.label_volumes.grid(row=3, column=0, padx=(10, 0), sticky=W)
        self.etr_volumes.grid(row=3, column=1, sticky=W)
        self.label_peso.grid(row=4, column=0, padx=(10, 0), sticky=W)
        self.etr_peso.grid(row=4, column=1, sticky=W)
        
        # FRAME 3 - TREEVIEW
        self.frm3.place(x=10, y=310, width=680, height=210)
        self.tv.grid()

        # FRAME 4 - BOTÕES SALVAR, LIMPAR E SAIR
        self.frm4.place(x=10, y=530, width=680, height=60)
        self.btn_salvar.grid(row=0, column=0, padx=(30,30), pady=(10,0))
        self.btn_limpar.grid(row=0, column=1, padx=(0,240), pady=(10,0))
        self.btn_sair.grid(row=0, column=2, pady=(10,0))
    
    def salvar(self):
        pass

    def limpar(self):
        self.nfe.set(0)
        self.data_emissao.set('')
        self.cliente.set('')
        self.volumes.set(0)
        self.peso.set(0.0)

    def sair(self):
        self.app1.destroy()
    