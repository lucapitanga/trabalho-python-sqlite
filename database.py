#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador do Banco de Dados SQLite
"""

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="sistema_comercial.db"):
        self.db_name = db_name
        self.conn = None
    
    def conectar(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            return self.conn
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            return None
    
    def desconectar(self):
        """Desconecta do banco de dados"""
        if self.conn:
            self.conn.close()
    
    def executar_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        conn = self.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    resultado = cursor.fetchall()
                else:
                    conn.commit()
                    resultado = cursor.rowcount
                
                return resultado
            except sqlite3.Error as e:
                print(f"❌ Erro ao executar query: {e}")
                return None
            finally:
                self.desconectar()
        return None
    
    def criar_tabelas(self):
        """Cria as tabelas do sistema"""
        
        # Tabela de produtos (loja de roupas)
        query_produtos = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            tamanho TEXT NOT NULL CHECK(tamanho IN ('P', 'M', 'G', 'GG')),
            estoque INTEGER DEFAULT 0,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Tabela de clientes
        query_clientes = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            endereco TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Tabela de fornecedores
        query_fornecedores = """
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT UNIQUE NOT NULL,
            email TEXT,
            telefone TEXT,
            endereco TEXT,
            categoria TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Executar criação das tabelas
        self.executar_query(query_produtos)
        self.executar_query(query_clientes)
        self.executar_query(query_fornecedores)
        
        print("✅ Tabelas criadas/verificadas com sucesso!")
    
    def limpar_banco(self):
        """Remove o arquivo do banco de dados (use com cuidado!)"""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
            print("🗑️ Banco de dados removido!")
