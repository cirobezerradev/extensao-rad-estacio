from connect_db import ConnectDB

class Tabelas:
    
    def criar_tabelas():
        try:
            db = ConnectDB()

            db.cursor.execute('''SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                AND table_type='BASE TABLE';''')
            
            tables = db.cursor.fetchall()

            if ('remessa',) not in tables:
                db.create_table('''CREATE TABLE REMESSA(
                                    NFE_REMESSA int NOT NULL,
                                    DATA_EMISSAO date NOT NULL,
                                    CLIENTE varchar(90) NOT NULL,
                                    VOLUMES int NOT NULL,
                                    PESO double precision NOT NULL,
                                    STATUS varchar(90) NOT NULL,
                                    CONSTRAINT CHAVEPREMESSA PRIMARY KEY (NFE_REMESSA)
                                    );''')
                print('TABELA REMESSA CRIADA')

            if ('retorno',) not in tables:
                db.create_table('''CREATE TABLE RETORNO(
                                    NFE_RETORNO int NOT NULL,
                                    DATA_EMISSAO date NOT NULL,
                                    CLIENTE varchar(90) NOT NULL,
                                    VOLUMES int NOT NULL,
                                    PESO double precision NOT NULL,
                                    NFE_REMESSA int NOT NULL,
                                    CONSTRAINT CHAVEPRETORNO PRIMARY KEY (NFE_RETORNO),
                                    FOREIGN KEY (NFE_REMESSA) REFERENCES REMESSA (NFE_REMESSA)
                                    );''')
                print('TABELA RETORNO CRIADA')

            if ('itemremessa',) not in tables:
                db.create_table('''CREATE TABLE ITEMREMESSA(
                                    COD_PRODUTO int NOT NULL,
                                    DESCRICAO varchar(90) NOT NULL,
                                    UN varchar(10) NOT NULL,
                                    QUANTIDADE double precision NOT NULL,
                                    VALOR_UNITARIO double precision NOT NULL,
                                    NFE_REMESSA int NOT NULL,
                                    CONSTRAINT CHAVEPITEMREMESSA PRIMARY KEY (COD_PRODUTO, NFE_REMESSA),
                                    FOREIGN KEY (NFE_REMESSA) REFERENCES REMESSA (NFE_REMESSA)
                                    );''')
                print('TABELA ITEMREMESSA CRIADA')
            
            if ('estoqueremessa',) not in tables:
                db.create_table('''CREATE TABLE ESTOQUEREMESSA(
                                  COD_PRODUTO int NOT NULL,
                                  DESCRICAO varchar(90) NOT NULL,
                                  UN varchar(10) NOT NULL,
                                  QUANTIDADE double precision NOT NULL,
                                  VALOR_UNITARIO double precision NOT NULL,
                                  NFE_REMESSA int NOT NULL,
                                  CONSTRAINT PK_ESTOQUEREMESSA PRIMARY KEY (COD_PRODUTO, NFE_REMESSA),
                                  FOREIGN KEY (NFE_REMESSA) REFERENCES REMESSA (NFE_REMESSA)
                                  );''')
                print('TABELA ESTOQUEREMESSA CRIADA')

            if ('itemretorno',) not in tables:
                db.create_table('''CREATE TABLE ITEMRETORNO(
                                    COD_PRODUTO int NOT NULL,
                                    DESCRICAO varchar(90) NOT NULL,
                                    UN varchar(10) NOT NULL,
                                    QUANTIDADE double precision NOT NULL,
                                    VALOR_UNITARIO double precision NOT NULL,
                                    NFE_RETORNO int NOT NULL,
                                    CONSTRAINT CHAVEPITEMRETORNO PRIMARY KEY (COD_PRODUTO, NFE_RETORNO),
                                    FOREIGN KEY (NFE_RETORNO) REFERENCES RETORNO (NFE_RETORNO)
                                    );''')
                print('TABELA ITEMRETORNO CRIADA')
               
            db.close_db()

        except Exception as err:
            print(err)