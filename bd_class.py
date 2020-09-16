#!python3

""" Inicialmente eu importo o sqlite3 para que eu possa usar
a funçao Banco de dados do Sqlite 3 """
import sqlite3


class Banco_de_dados:  # Criaçao da classe principal do banco de dados

    def __init__(self, banco, tabela):
        self.banco = banco
        self.tabela = tabela
        print('Banco de dados e tabela selecionados...')

    #Conexao no banco de dados e posicionamento do cursor
    def conectar_banco_de_dados(self):
        self.bd = sqlite3.connect(self.banco)
        self.cursor = self.bd.cursor()
        print('Cursor posicionado...')
        print('=====================')

    #Criaçao de tabela no banco selecionado
    def criar_tabela(self):
        self.cursor.execute(f"CREATE TABLE {self.tabela} (id INTEGER NOT NULL PRIMARY KEY, nome VARCHAR(30), idade VARCHAR(30))")
        print('Tabela criada...')

    #Inserçao de dados na tabela
    def inserir_dados(self, id, nome, idade):
        self.cursor.execute(f'INSERT INTO {self.tabela} (id, nome, idade) VALUES("{id}","{nome}","{idade}")')
        self.bd.commit()
        print('Dados inseridos...')

    def ler_tabela(self):
        self.cursor.execute(f'SELECT * FROM {self.tabela}')
        b = self.cursor.fetchall()
        return b