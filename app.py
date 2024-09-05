from tkinter import *
from tkinter import ttk
from cadastrar_remessa import CadastrarRemessa
from select_remessa import SelectRemessa
from buscar_remessa import BuscarRemessa
from tabelas import Tabelas


class application:

    def __init__(self):
        self.app = Tk()
        self.app.title('Controle de Remessas')
        self.app.geometry('700x300+500+450')
        self.app.resizable(width=False, height=False)
        self.w_styles()
        self.frames_app()
        self.widgets_app()
        self.position_grid()
        Tabelas.criar_tabelas()
        self.app.mainloop()

    # Styles
    def w_styles(self):
        ttk.Style().configure('TButton', padding=5,
                              font=('roboto', 12, 'bold'),
                              foreground='#4C5C57', relief='raised',
                              width=20)

    def frames_app(self):
        self.frm1 = ttk.Frame(self.app, borderwidth=1, relief='solid')

    # Widgets
    def widgets_app(self):
        # Botão para Cadastro de Remessa
        self.btn1 = ttk.Button(
            self.frm1, text='Cadastro de Remessa',
            style='TButton', command=CadastrarRemessa)
        # Botão para Cadastro de Retorno
        self.btn2 = ttk.Button(
            self.frm1, text='Cadastro de Retorno',
            style='TButton', command=SelectRemessa)
        # Botão para Buscas Remessas
        self.btn3 = ttk.Button(
            self.frm1, text='Buscar Remessas',
            style='TButton', command=BuscarRemessa)

    def position_grid(self):
        self.frm1.place(x=5, y=5, width=690, height=290)
        self.btn1.grid(row=1, column=0, padx=(150, 0), pady=(100, 0))
        self.btn2.grid(row=1, column=1, pady=(100, 0))
        self.btn3.grid(row=2, column=0, padx=(150, 0), pady=(20,0), sticky=W)

if __name__ == '__main__':
    application()
