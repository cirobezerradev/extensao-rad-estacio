from cadastrosRR import CadastrosRR
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from DomRetorno import DomRetorno
from connect_db import ConnectDB
import psycopg2
from psycopg2 import errors

class EstoqueInsuficiente(Exception):
    pass

class CadastrarRetorno(CadastrosRR):

    def __init__(self, ref_remessa) -> None:
        self.ref_remessa = IntVar()
        self.ref_remessa.set(ref_remessa)

        super().__init__()
        self.app1.title('Cadastro de Retorno')
        self.widgets_app()
        self.position_grid()
        self.verificado = []

    def widgets_app(self):
        super().widgets_app()
        self.label_ref_remessa = ttk.Label(self.frm2,
                                           text='Ref. NFe Remessa:')
        self.etr_ref_remessa = ttk.Entry(
            self.frm2, textvariable=self.ref_remessa, state=DISABLED)

    def position_grid(self):
        super().position_grid()
        self.label_ref_remessa.grid(row=5, column=0, padx=(10, 0), sticky=W)
        self.etr_ref_remessa.grid(row=5, column=1, sticky=W)

    def abrir_xml(self):
        url_xml = filedialog.askopenfilename(parent=self.app1)
        self.retorno = DomRetorno(url_xml)
        self.nfe.set(self.retorno.num_nfe)
        self.data_emissao.set(self.retorno.data_emissao)
        self.cliente.set(self.retorno.cliente)
        self.volumes.set(self.retorno.volumes)
        self.peso.set(f'{self.retorno.peso:.2f}')
        self.ref_remessa.set(self.etr_ref_remessa.get())
        self.cfop.set(self.retorno.status_cfop())
        # VERIFICAÇÃO DE CFOP 6902
        if not self.cfop.get():
            messagebox.showinfo(title='ATENÇÃO',
                                message='Por favor insira uma XML de Retorno.',
                                parent=self.app1)
            self.limpar()
            return None
        # Inserção dos Itens na Treeview
        count = 1
        for (a, b, c, d, e) in self.retorno.itens:
            self.cod_produto = a
            self.descricao = b
            self.un = c
            self.quantidade = d
            self.valor_unitario = e
            self.tv.insert('', 'end', values=(count, a, b, c, d, e))
            count += 1

    def salvar(self) -> None:
        super().salvar()

        try:
            self.db = ConnectDB()

            # SCRIPT SQL PARA INSERIR DADOS NA TABELA RETORNO
            sql_retorno = '''INSERT INTO retorno(nfe_retorno,
                        data_emissao, cliente, volumes,
                        peso, nfe_remessa)
                        VALUES (%s, %s, %s, %s, %s, %s);'''
            # TUPLA COM VALORES P/ INSERÇÃO
            tp_retorno = (self.nfe.get(), self.data_emissao.get(),
                        self.cliente.get(), self.volumes.get(),
                        self.peso.get(), self.ref_remessa.get())
            
            self.db.insert_db(sql_retorno, tp_retorno)

            if FALSE in self.verifica_estoque():
                self.db.conn.rollback()
                self.db.close_db()
                raise EstoqueInsuficiente()
            
            # SCRIPT SQL PARA INSERIR DADOS NA TABELA ITEMRETORNO
            sql_itemretorno = '''INSERT INTO itemretorno(cod_produto,
                            descricao, un, quantidade, valor_unitario,
                            nfe_retorno)
                            VALUES (%s, %s, %s, %s, %s, %s);'''

            # ITERAÇÃO P TUPLA DE VALORES PARA INSERÇÃO
            for (a, b, c, d, e) in self.retorno.itens:
                tp_itens = (a, b, c, d, e, self.nfe.get())
                # INSERSÃO NA TABELA ITEMRETORNO
                self.db.insert_db(sql_itemretorno, tp_itens)
                # Atualiza o estoque
                self.update_estoque(d, a, self.ref_remessa.get())
            
            self.db.conn.commit()

            messagebox.showinfo(title='INFORMAÇÃO',
            message=f'''RETORNO {self.nfe.get()} CADASTRADO COM SUCESSO.''',
            parent=self.app1)

            self.verifica_estoque()

            self.db.close_db()

            return self.limpar()
        
        # TRATA ERRO DE DUPLICIDADE NO BANCO DE DADOS
        except psycopg2.errors.UniqueViolation as err:
            msg = f'O Retorno {self.nfe.get()} já foi cadastrado!'
            messagebox.showinfo(
                title="ATENÇÃO", message=msg, parent=self.app1)
            self.limpar()
            self.db.conn.rollback()
            self.db.close_db()
            return None
        
        except psycopg2.errors.ForeignKeyViolation:
            msg = f'A Remessa {self.ref_remessa.get()} referenciada ainda não foi cadastrada'
            messagebox.showinfo(
                title="ATENÇÃO", message=msg, parent=self.app1)
            self.db.conn.rollback()
            self.db.close_db()
            self.limpar()
            return None
        
        except EstoqueInsuficiente:
            messagebox.showinfo(title='Cadastramento Negado',
                    message='''Não foi possível cadastrar o retorno.\n
                    Item insuficiente em estoque''',
                    parent=self.app1)
 
    def limpar(self):
        super().limpar()
        self.tv.delete(*self.tv.get_children())
    
    def verifica_estoque(self):
        try:

            lista_verificados = []

            for item in self.retorno.itens:

                sql_select = '''SELECT quantidade
                FROM estoqueremessa
                WHERE nfe_remessa = %s AND 
                cod_produto = %s'''

                tp_sql = (self.ref_remessa.get(), item[0])

                lista_verificados.append(self.db.select_db(sql_select, tp_sql)[0][0] >= item[3])

            self.update_status()
            
            return lista_verificados
        
        except Exception as err:
            print(err)
    
    def update_estoque(self, quantidade, cod_produto, nfe_remessa):
            try:

                  sql_update = '''
                  UPDATE estoqueremessa
                  SET quantidade=quantidade - %s
                  WHERE cod_produto = %s
                  AND nfe_remessa = %s'''

                  tp_sql = (quantidade, cod_produto, nfe_remessa)

                  self.db.update_db(sql_update, tp_sql)

            except Exception as err:
                  print(err)
    
    def update_status(self):
        try:

            sql_quantidade = '''
            SELECT SUM(quantidade)
            FROM estoqueremessa
            WHERE nfe_remessa = %s'''

            tp_remessa = (self.ref_remessa.get(),)

            quantidade = self.db.select_db(sql_quantidade, tp_remessa)[0][0]

            if quantidade == 0:

                sql_select = '''
                SELECT status
                FROM remessa
                WHERE nfe_remessa = %s'''

                tp_update = (self.ref_remessa.get(),)

                if self.db.select_db(sql_select, tp_update)[0][0] == 'PENDENTE':

                    sql_update = '''
                    UPDATE remessa
                    SET status = 'FINALIZADA'
                    WHERE nfe_remessa = %s
                    '''
                    
                    self.db.update_db(sql_update, tp_update)

                    self.db.conn.commit()

                    messagebox.showinfo(title='Remessa Finalizada',
                        message=f'''A Remessa {self.ref_remessa.get()} foi FINALIZADA''',
                        parent=self.app1)
        
        except Exception as err:
            print(err)