from tkinter import *
from tkinter import ttk, messagebox
from connect_db import ConnectDB
from estoque_remessa import EstoqueRemessa

class BuscarRemessa:

    def __init__(self) -> None:
        self.nfe_remessa = StringVar()
        self.app2 = Toplevel()
        self.app2.title('BUSCAR REMESSAS')
        self.app2.geometry('800x435+500+100')
        self.app2.resizable(width=False, height=False)
        self.style_app()
        self.frames_app()
        self.widgets_app()
        self.treeview_app()
        self.position_grid()
        self.listar_remessas()
    
    def style_app(self):
        ttk.Style().configure('B.TLabel',
                              font=('calibri', 15, 'bold'),
                              foreground='#4C5C57')
        ttk.Style().configure('B.TButton',
                              font=('calibri', 15, 'bold'),
                              foreground='#4C5C57', width=10)
        ttk.Style().configure('TScrollbar', height=100)
    
    def frames_app(self):
        self.frm1 = ttk.Frame(self.app2, borderwidth=1, relief=SOLID)
        self.frm2 = ttk.Frame(self.app2)
    
    def widgets_app(self):
        self.label_nfe = ttk.Label(self.frm1, text='NFe Remessa: ', style='B.TLabel')
        self.etr_nfe = ttk.Entry(self.frm1, textvariable=self.nfe_remessa)
        self.btn1 = ttk.Button(self.frm1, text='Buscar', command=self.buscar_remessa,
                               style='B.TButton')
        self.btn2 = ttk.Button(self.frm1, text='Listar Remessas', command=self.listar_remessas,
                               style='B.TButton', width=20)
    
    def treeview_app(self):
        self.tv = ttk.Treeview(self.frm2,
                               columns=('nfe_remessa',
                                        'cliente',
                                        'data_emissao',
                                        'data_limite',
                                        'status'),
                                        show='headings',
                                        height=14)
        self.tv.column('nfe_remessa', minwidth=10, width=100, anchor=CENTER)
        self.tv.column('cliente', minwidth=10, width=313)
        self.tv.column('data_emissao', minwidth=10, width=100, anchor=CENTER)
        self.tv.column('data_limite', minwidth=10, width=100, anchor=CENTER)
        self.tv.column('status', minwidth=10, width=150, anchor=CENTER)
        self.tv.heading('nfe_remessa', text='NFe')
        self.tv.heading('cliente', text='Cliente')
        self.tv.heading('data_emissao', text='Data Emissão')
        self.tv.heading('data_limite', text='Data Limite')
        self.tv.heading('status', text='Status')

        self.scbar = ttk.Scrollbar(self.frm2,
                                   orient='vertical',
                                   command=self.tv.yview,
                                   style='TScrollbar')
        self.scbar.set(0, 0.9)
        self.tv.bind('<ButtonRelease-1>', self.select_remessa,)
    
    def select_remessa(self, a):
        selecao = self.tv.item(self.tv.selection())
        nfe_remessa = selecao['values'][0]
        self.app2.destroy()
        EstoqueRemessa(nfe_remessa)
        
    
    def position_grid(self):
        self.frm1.place(x=10, y=10, width=780, height=100)
        self.label_nfe.grid(row=0, column=0, padx=(30,0), pady=(35,0))
        self.etr_nfe.grid(row=0, column=1, pady=(35,0))
        self.btn1.grid(row=0, column=2, padx=(20,0), pady=(35,0))
        self.btn2.grid(row=0, column=3, padx=(20,0), pady=(35,0))
        self.frm2.place(x=10, y=120, width=780, height=320)
        self.tv.yview("moveto", 0.82)
        self.tv.grid(row=0, column=0)
        self.scbar.place(x=765, height=310)
    
    def buscar_remessa(self):
        self.tv.delete(*self.tv.get_children())
        try:
            db = ConnectDB()

            sql_select = '''SELECT nfe_remessa, cliente,
                                data_emissao,
                                (data_emissao + 180) as data_limite,
                                status
                            FROM remessa
                            WHERE nfe_remessa=%s'''
            
            tp_select = (self.nfe_remessa.get(),)
            
            self.lista = db.select_db(sql_select, tp_select)
            
            if not self.lista:
                messagebox.showinfo(title='ATENÇÃO',
                        message=f'''A REMESSA {self.nfe_remessa.get()},\nainda não foi cadastrada!''',
                        parent=self.app2)
                return self.listar_remessas()
            
            for (a, b, c, d, e) in self.lista:
                self.tv.insert('', END,
                                values=(a, b,
                                        c.strftime('%d/%m/%Y'),
                                        d.strftime('%d/%m/%Y'),
                                        e),)
            
            db.close_db()

        except Exception as err:
            print(err)

    def listar_remessas(self):
        self.tv.delete(*self.tv.get_children())
        try:
            db = ConnectDB()

            sql_select = '''SELECT nfe_remessa, cliente,
                                data_emissao,
                                (data_emissao + 180) as data_limite,
                                status
                            FROM remessa
                            ORDER BY status DESC, nfe_remessa DESC'''
            
            self.lista = db.select_db(sql_select, None)
            
            for (a, b, c, d, e) in self.lista:
                self.tv.insert('', END,
                                values=(a, b,
                                        c.strftime('%d/%m/%Y'),
                                        d.strftime('%d/%m/%Y'),
                                        e),)
            
            db.close_db()
        
        except Exception as err:
            print(err)