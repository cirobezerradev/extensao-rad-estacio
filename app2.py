from tkinter import *
from tkinter import ttk

class app2:
    def __init__(self) -> None:
        self.app = Tk()
        self.app.title('Teste App')
        self.app.geometry('700x500+100+500')
        self.app.resizable(width=False, height=False)
        self.frames_app()
        self.widgets_app()
        self.position_grid()
        self.app.mainloop()
    
    def frames_app(self):
        self.frm1 = ttk.Frame(self.app, borderwidth=1, relief='solid')
        self.frm2 = ttk.Frame(self.app, borderwidth=1, relief='solid')
        self.frm3 = ttk.Frame(self.app, borderwidth=1, relief='solid')       

    def widgets_app(self):
        # FRAME 1
        self.lbl_codigo = ttk.Label(self.frm1, text='Código: ')
        self.lbl_produto = ttk.Label(self.frm1, text='Produto: ')
        self.lbl_preco = ttk.Label(self.frm1, text='Preço: ')

        # FRAME 2
        self.btn1 = ttk.Button(self.frm2, text='Cadastrar')

    def position_grid(self):
        # FRAME 1
        self.frm1.place(x=10, y=10, width=680, height=150)
        self.lbl_codigo.grid(row=0, column=0, padx=(30,0), pady=(10,0), sticky=W)
        self.lbl_produto.grid(row=1, column=0, padx=(30,0), pady=(10,0), sticky=W)
        self.lbl_preco.grid(row=2, column=0, padx=(30,0), pady=(10,0), sticky=W)
        # FRAME 2
        self.frm2.place(x=10, y=170, width=680, height=150)
        self.btn1.grid(row=0, column=0, padx=(30,0), pady=(10,0), sticky=W)
        # FRAME 3
        self.frm3.place(x=10, y=330, width=680, height=150)

if __name__ == '__main__':
    app2()