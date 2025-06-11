#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD para Fornecedores
"""

import re

class Fornecedor:
    def __init__(self, id=None, nome="", cnpj="", email="", telefone="", endereco="", categoria=""):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.categoria = categoria
    
    def __str__(self):
        return f"{self.nome} - {self.cnpj} - {self.categoria}"

class FornecedorCRUD:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def validar_email(self, email):
        requisitos = ['@', '.']
        for req in requisitos:
            if req not in email:
                return False
        return True
    
    def validar_cnpj(self, cnpj):
        """Validação básica de CNPJ (apenas formato)"""
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        return len(cnpj) == 14
    
    def formatar_cnpj(self, cnpj):
        """Formata CNPJ"""
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
    
    def adicionar_fornecedor(self):
        """Adiciona um novo fornecedor"""
        try:
            print("\n Cadastrar Novo Fornecedor")
            print("-" * 35)
            
            nome = input("Nome da empresa: ").strip()
            if not nome:
                print(" Nome não pode estar vazio.")
                return
            
            cnpj = input("CNPJ (apenas números): ").strip()
            if not self.validar_cnpj(cnpj):
                print(" CNPJ inválido. Deve ter 14 dígitos.")
                return
            
            cnpj = re.sub(r'[^0-9]', '', cnpj)  # Limpa CNPJ
            
            email = input("Email (opcional): ").strip().lower()
            if email and not self.validar_email(email):
                print(" Email inválido.")
                return
            
            telefone = input("Telefone: ").strip()
            endereco = input("Endereço: ").strip()
            categoria = input("Categoria/Ramo: ").strip()
            
            query = """
            INSERT INTO fornecedores (nome, cnpj, email, telefone, endereco, categoria)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            resultado = self.db.executar_query(query, (nome, cnpj, email, telefone, endereco, categoria))
            
            if resultado:
                print(" Fornecedor adicionado com sucesso!")
            else:
                print(" Erro ao adicionar fornecedor. CNPJ pode já estar cadastrado.")
                
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def listar_fornecedores(self):
        """Lista todos os fornecedores"""
        query = "SELECT * FROM fornecedores ORDER BY nome"
        fornecedores = self.db.executar_query(query)
        
        if not fornecedores:
            print(" Nenhum fornecedor cadastrado.")
            return False
        
        print("\n Lista de Fornecedores:")
        print("-" * 90)
        print(f"{'ID':<3} {'Nome':<25} {'CNPJ':<18} {'Categoria':<20} {'Telefone':<15}")
        print("-" * 90)
        
        for fornecedor in fornecedores:
            cnpj_formatado = self.formatar_cnpj(fornecedor['cnpj'])
            print(f"{fornecedor['id']:<3} {fornecedor['nome']:<25} {cnpj_formatado:<18} "
                  f"{fornecedor['categoria'] or 'N/A':<20} {fornecedor['telefone'] or 'N/A':<15}")
        
        return True
    
    def buscar_fornecedor_por_id(self, fornecedor_id):
        """Busca um fornecedor pelo ID"""
        query = "SELECT * FROM fornecedores WHERE id = ?"
        resultado = self.db.executar_query(query, (fornecedor_id,))
        
        if resultado:
            return resultado[0]
        return None
    
    def buscar_fornecedores(self):
        """Busca fornecedores por nome, CNPJ ou categoria"""
        termo = input("Digite nome, CNPJ ou categoria para buscar: ").strip()
        if not termo:
            print(" Termo de busca não pode estar vazio.")
            return
        
        # Remove formatação do CNPJ se for o caso
        termo_cnpj = re.sub(r'[^0-9]', '', termo)
        
        query = """
        SELECT * FROM fornecedores 
        WHERE nome LIKE ? OR cnpj LIKE ? OR categoria LIKE ?
        ORDER BY nome
        """
        fornecedores = self.db.executar_query(query, (f"%{termo}%", f"%{termo_cnpj}%", f"%{termo}%"))
        
        if not fornecedores:
            print(" Nenhum fornecedor encontrado.")
            return
        
        print(f"\n Resultados da busca por '{termo}':")
        print("-" * 90)
        print(f"{'ID':<3} {'Nome':<25} {'CNPJ':<18} {'Categoria':<20} {'Telefone':<15}")
        print("-" * 90)
        
        for fornecedor in fornecedores:
            cnpj_formatado = self.formatar_cnpj(fornecedor['cnpj'])
            print(f"{fornecedor['id']:<3} {fornecedor['nome']:<25} {cnpj_formatado:<18} "
                  f"{fornecedor['categoria'] or 'N/A':<20} {fornecedor['telefone'] or 'N/A':<15}")
    
    def atualizar_fornecedor(self):
        """Atualiza um fornecedor existente"""
        if not self.listar_fornecedores():
            return
        
        try:
            fornecedor_id = int(input("\nID do fornecedor para atualizar: "))
            fornecedor = self.buscar_fornecedor_por_id(fornecedor_id)
            
            if not fornecedor:
                print(" Fornecedor não encontrado.")
                return
            
            while True:
                print(f"\nFornecedor selecionado: {fornecedor['nome']} - {self.formatar_cnpj(fornecedor['cnpj'])}")
                print("O que deseja atualizar?")
                print("1. Nome")
                print("2. CNPJ")
                print("3. Email")
                print("4. Telefone")
                print("5. Endereço")
                print("6. Categoria")
                print("7. Voltar")
                
                escolha = input("Opção: ").strip()
                
                if escolha == '1':
                    novo_nome = input("Novo nome: ").strip()
                    if novo_nome:
                        query = "UPDATE fornecedores SET nome = ? WHERE id = ?"
                        self.db.executar_query(query, (novo_nome, fornecedor_id))
                        fornecedor = dict(fornecedor)
                        fornecedor['nome'] = novo_nome
                        print(" Nome atualizado!")
                    else:
                        print(" Nome não pode estar vazio.")
                
                elif escolha == '2':
                    novo_cnpj = input("Novo CNPJ (apenas números): ").strip()
                    if self.validar_cnpj(novo_cnpj):
                        novo_cnpj = re.sub(r'[^0-9]', '', novo_cnpj)
                        query = "UPDATE fornecedores SET cnpj = ? WHERE id = ?"
                        resultado = self.db.executar_query(query, (novo_cnpj, fornecedor_id))
                        if resultado:
                            fornecedor = dict(fornecedor)
                            fornecedor['cnpj'] = novo_cnpj
                            print(" CNPJ atualizado!")
                        else:
                            print(" CNPJ já está em uso.")
                    else:
                        print(" CNPJ inválido.")
                
                elif escolha == '3':
                    novo_email = input("Novo email: ").strip().lower()
                    if self.validar_email(novo_email):
                        query = "UPDATE fornecedores SET email = ? WHERE id = ?"
                        self.db.executar_query(query, (novo_email, fornecedor_id))
                        fornecedor = dict(fornecedor)
                        fornecedor['email'] = novo_email
                        print(" Email atualizado!")
                    else:
                        print(" Email inválido.")
                
                elif escolha == '4':
                    novo_telefone = input("Novo telefone: ").strip()
                    query = "UPDATE fornecedores SET telefone = ? WHERE id = ?"
                    self.db.executar_query(query, (novo_telefone, fornecedor_id))
                    fornecedor = dict(fornecedor)
                    fornecedor['telefone'] = novo_telefone
                    print(" Telefone atualizado!")
                
                elif escolha == '5':
                    novo_endereco = input("Novo endereço: ").strip()
                    query = "UPDATE fornecedores SET endereco = ? WHERE id = ?"
                    self.db.executar_query(query, (novo_endereco, fornecedor_id))
                    fornecedor = dict(fornecedor)
                    fornecedor['endereco'] = novo_endereco
                    print(" Endereço atualizado!")
                
                elif escolha == '6':
                    nova_categoria = input("Nova categoria: ").strip()
                    query = "UPDATE fornecedores SET categoria = ? WHERE id = ?"
                    self.db.executar_query(query, (nova_categoria, fornecedor_id))
                    fornecedor = dict(fornecedor)
                    fornecedor['categoria'] = nova_categoria
                    print(" Categoria atualizada!")
                
                elif escolha == '7':
                    break
                else:
                    print(" Opção inválida.")
                    
        except ValueError:
            print(" ID inválido.")
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def excluir_fornecedor(self):
        """Exclui um fornecedor"""
        if not self.listar_fornecedores():
            return
        
        try:
            fornecedor_id = int(input("\nID do fornecedor para excluir: "))
            fornecedor = self.buscar_fornecedor_por_id(fornecedor_id)
            
            if not fornecedor:
                print(" Fornecedor não encontrado.")
                return
            
            confirmacao = input(f"Confirma exclusão de '{fornecedor['nome']}'? (s/N): ").lower()
            
            if confirmacao == 's':
                query = "DELETE FROM fornecedores WHERE id = ?"
                resultado = self.db.executar_query(query, (fornecedor_id,))
                
                if resultado:
                    print(f" Fornecedor '{fornecedor['nome']}' excluído com sucesso!")
                else:
                    print(" Erro ao excluir fornecedor.")
            else:
                print(" Exclusão cancelada.")
                
        except ValueError:
            print(" ID inválido.")
        except Exception as e:
            print(f" Erro inesperado: {e}")
    
    def menu(self):
        """Menu principal de fornecedores"""
        while True:
            print("\n" + "="*40)
            print(" GERENCIAMENTO DE FORNECEDORES")
            print("="*40)
            print("1. Adicionar fornecedor")
            print("2. Listar fornecedores")
            print("3. Buscar fornecedores")
            print("4. Atualizar fornecedor")
            print("5. Excluir fornecedor")
            print("6. Voltar ao menu principal")
            print("="*40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.adicionar_fornecedor()
            elif opcao == '2':
                self.listar_fornecedores()
            elif opcao == '3':
                self.buscar_fornecedores()
            elif opcao == '4':
                self.atualizar_fornecedor()
            elif opcao == '5':
                self.excluir_fornecedor()
            elif opcao == '6':
                break
            else:
                print(" Opção inválida. Tente novamente.")