#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD para Clientes
"""

import re

class Cliente:
    def __init__(self, id=None, nome="", email="", telefone="", endereco=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
    
    def __str__(self):
        return f"{self.nome} - {self.email} - {self.telefone}"

class ClienteCRUD:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def validar_email(self, email):
        requisitos = ['@', '.']
        for req in requisitos:
            if req not in email:
                return False
        return True

    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        try:
            print("\n Cadastrar Novo Cliente")
            print("-" * 30)
            
            nome = input("Nome completo: ").strip()
            if not nome:
                print(" Nome não pode estar vazio.")
                return
            
            email = input("Email: ").strip().lower()
            if not self.validar_email(email):
                print(" Email inválido.")
                return
            
            telefone = input("Telefone: ").strip()
            endereco = input("Endereço: ").strip()
            
            query = """
            INSERT INTO clientes (nome, email, telefone, endereco)
            VALUES (?, ?, ?, ?)
            """
            resultado = self.db.executar_query(query, (nome, email, telefone, endereco))
            
            if resultado:
                print(" Cliente adicionado com sucesso!")
            else:
                print(" Erro ao adicionar cliente. Email pode já estar cadastrado.")
                
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        query = "SELECT * FROM clientes ORDER BY nome"
        clientes = self.db.executar_query(query)
        
        if not clientes:
            print(" Nenhum cliente cadastrado.")
            return False
        
        print("\n Lista de Clientes:")
        print("-" * 80)
        print(f"{'ID':<3} {'Nome':<25} {'Email':<25} {'Telefone':<15} {'Endereço':<50}")
        print("-" * 80)
        
        for cliente in clientes:
            print(f"{cliente['id']:<3} {cliente['nome']:<25} {cliente['email']:<25} "
                  f"{cliente['telefone'] or 'N/A':<15} {cliente['endereco']:<25}")
        
        return True
    
    def buscar_cliente_por_id(self, cliente_id):
        """Busca um cliente pelo ID"""
        query = "SELECT * FROM clientes WHERE id = ?"
        resultado = self.db.executar_query(query, (cliente_id,))
        
        if resultado:
            return resultado[0]
        return None
    
    def buscar_clientes(self):
        """Busca clientes por nome ou email"""
        termo = input("Digite nome ou email para buscar: ").strip()
        if not termo:
            print(" Termo de busca não pode estar vazio.")
            return
        
        query = """
        SELECT * FROM clientes 
        WHERE nome LIKE ? OR email LIKE ?
        ORDER BY nome
        """
        clientes = self.db.executar_query(query, (f"%{termo}%", f"%{termo}%"))
        
        if not clientes:
            print(" Nenhum cliente encontrado.")
            return
        
        print(f"\n Resultados da busca por '{termo}':")
        print("-" * 80)
        print(f"{'ID':<3} {'Nome':<25} {'Email':<25} {'Telefone':<15}")
        print("-" * 80)
        
        for cliente in clientes:
            print(f"{cliente['id']:<3} {cliente['nome']:<25} {cliente['email']:<25} "
                  f"{cliente['telefone'] or 'N/A':<15}")
    
    def atualizar_cliente(self):
        """Atualiza um cliente existente"""
        if not self.listar_clientes():
            return
        
        try:
            cliente_id = int(input("\nID do cliente para atualizar: "))
            cliente = self.buscar_cliente_por_id(cliente_id)
            
            if not cliente:
                print(" Cliente não encontrado.")
                return
            
            while True:
                print(f"\nCliente selecionado: {cliente['nome']} - {cliente['email']}")
                print("O que deseja atualizar?")
                print("1. Nome")
                print("2. Email")
                print("3. Telefone")
                print("4. Endereço")
                print("5. Voltar")
                
                escolha = input("Opção: ").strip()
                
                if escolha == '1':
                    novo_nome = input("Novo nome: ").strip()
                    if novo_nome:
                        query = "UPDATE clientes SET nome = ? WHERE id = ?"
                        self.db.executar_query(query, (novo_nome, cliente_id))
                        cliente = dict(cliente)
                        cliente['nome'] = novo_nome
                        print(" Nome atualizado!")
                    else:
                        print(" Nome não pode estar vazio.")
                
                elif escolha == '2':
                    novo_email = input("Novo email: ").strip().lower()
                    if self.validar_email(novo_email):
                        query = "UPDATE clientes SET email = ? WHERE id = ?"
                        resultado = self.db.executar_query(query, (novo_email, cliente_id))
                        if resultado:
                            cliente = dict(cliente)
                            cliente['email'] = novo_email
                            print(" Email atualizado!")
                        else:
                            print(" Email já está em uso.")
                    else:
                        print(" Email inválido.")
                
                elif escolha == '3':
                    novo_telefone = input("Novo telefone: ").strip()
                    query = "UPDATE clientes SET telefone = ? WHERE id = ?"
                    self.db.executar_query(query, (novo_telefone, cliente_id))
                    cliente = dict(cliente)
                    cliente['telefone'] = novo_telefone
                    print(" Telefone atualizado!")
                
                elif escolha == '4':
                    novo_endereco = input("Novo endereço: ").strip()
                    query = "UPDATE clientes SET endereco = ? WHERE id = ?"
                    self.db.executar_query(query, (novo_endereco, cliente_id))
                    cliente = dict(cliente)
                    cliente['endereco'] = novo_endereco
                    print(" Endereço atualizado!")
                
                elif escolha == '5':
                    break
                else:
                    print(" Opção inválida.")
                    
        except ValueError:
            print(" ID inválido.")
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def excluir_cliente(self):
        """Exclui um cliente"""
        if not self.listar_clientes():
            return
        
        try:
            cliente_id = int(input("\nID do cliente para excluir: "))
            cliente = self.buscar_cliente_por_id(cliente_id)
            
            if not cliente:
                print(" Cliente não encontrado.")
                return
            
            confirmacao = input(f"Confirma exclusão de '{cliente['nome']}'? (s/N): ").lower()
            
            if confirmacao == 's':
                query = "DELETE FROM clientes WHERE id = ?"
                resultado = self.db.executar_query(query, (cliente_id,))
                
                if resultado:
                    print(f" Cliente '{cliente['nome']}' excluído com sucesso!")
                else:
                    print(" Erro ao excluir cliente.")
            else:
                print(" Exclusão cancelada.")
                
        except ValueError:
            print(" ID inválido.")
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def menu(self):
        """Menu principal de clientes"""
        while True:
            print("\n" + "="*40)
            print(" GERENCIAMENTO DE CLIENTES")
            print("="*40)
            print("1. Adicionar cliente")
            print("2. Listar clientes")
            print("3. Buscar clientes")
            print("4. Atualizar cliente")
            print("5. Excluir cliente")
            print("6. Voltar ao menu principal")
            print("="*40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.adicionar_cliente()
            elif opcao == '2':
                self.listar_clientes()
            elif opcao == '3':
                self.buscar_clientes()
            elif opcao == '4':
                self.atualizar_cliente()
            elif opcao == '5':
                self.excluir_cliente()
            elif opcao == '6':
                break
            else:
                print(" Opção inválida. Tente novamente.")
