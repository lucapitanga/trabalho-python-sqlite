#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD para Loja de Roupas
"""

class Produto:
    tamanhos_validos = ["P", "M", "G", "GG"]
    
    def __init__(self, id=None, nome="", preco=0.0, tamanho="", estoque=0):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.tamanho = tamanho
        self.estoque = estoque
    
    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - Tamanho: {self.tamanho} - Estoque: {self.estoque}"

class LojaCRUD:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def adicionar_produto(self):
        """Adiciona um novo produto"""
        try:
            print("\n📝 Cadastrar Novo Produto")
            print("-" * 30)
            
            nome = input("Nome do produto: ").strip()
            if not nome:
                print("❌ Nome não pode estar vazio.")
                return
            
            preco = float(input("Preço: R$"))
            if preco < 0:
                print("❌ Preço não pode ser negativo.")
                return
            
            tamanho = input("Tamanho (P, M, G, GG): ").upper().strip()
            if tamanho not in Produto.tamanhos_validos:
                print("❌ Tamanho inválido.")
                return
            
            estoque = int(input("Quantidade em estoque: "))
            if estoque < 0:
                print("❌ Estoque não pode ser negativo.")
                return
            
            query = """
            INSERT INTO produtos (nome, preco, tamanho, estoque)
            VALUES (?, ?, ?, ?)
            """
            resultado = self.db.executar_query(query, (nome, preco, tamanho, estoque))
            
            if resultado:
                print("✅ Produto adicionado com sucesso!")
            else:
                print("❌ Erro ao adicionar produto.")
                
        except ValueError:
            print("❌ Erro: valores numéricos inválidos.")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        query = "SELECT * FROM produtos ORDER BY nome"
        produtos = self.db.executar_query(query)
        
        if not produtos:
            print("📭 Nenhum produto cadastrado.")
            return False
        
        print("\n📦 Lista de Produtos:")
        print("-" * 70)
        print(f"{'ID':<3} {'Nome':<20} {'Preço':<10} {'Tamanho':<8} {'Estoque':<8}")
        print("-" * 70)
        
        for produto in produtos:
            print(f"{produto['id']:<3} {produto['nome']:<20} R${produto['preco']:<9.2f} "
                  f"{produto['tamanho']:<8} {produto['estoque']:<8}")
        
        return True
    
    #def buscar_produto_por_id(self, produto_id):
        """Busca um produto pelo ID"""
        query = "SELECT * FROM produtos WHERE id = ?"
        resultado = self.db.executar_query(query, (produto_id,))
        
        if resultado:
            return resultado[0]
        return None
    
    def buscar_produtos(self):
        """Busca produtos por nome ou email"""
        termo = input("Digite nome para buscar: ").strip()
        if not termo:
            print("❌ Termo de busca não pode estar vazio.")
            return
        
        query = """
        SELECT * FROM produtos 
        WHERE nome LIKE ? 
        ORDER BY nome
        """
        produtos = self.db.executar_query(query, (f"%{termo}%",))
        
        if not produtos:
            print("📭 Nenhum produto encontrado.")
            return
        
        print(f"\n🔍 Resultados da busca por '{termo}':")
        print("-" * 80)
        print(f"{'ID':<3} {'Nome':<25} {'Preço':<25} {'Tamanho':<15} {'Estoque':<15}")
        print("-" * 80)
        
        for produto in produtos:
            print(f"{produto['id']:<3} {produto['nome']:<25} {produto['preco']:<25} "
                  f"{produto['tamanho']:<15} {produto['estoque']:<25}")
    
    def atualizar_produto(self):
        """Atualiza um produto existente"""
        if not self.listar_produtos():
            return
        
        try:
            produto_id = int(input("\nID do produto para atualizar: "))
            produto = self.buscar_produto_por_id(produto_id)
            
            if not produto:
                print("❌ Produto não encontrado.")
                return
            
            while True:
                print(f"\nProduto selecionado: {produto['nome']} - R${produto['preco']:.2f}")
                print("O que deseja atualizar?")
                print("1. Nome")
                print("2. Preço")
                print("3. Tamanho")
                print("4. Estoque")
                print("5. Voltar")
                
                escolha = input("Opção: ").strip()
                
                if escolha == '1':
                    novo_nome = input("Novo nome: ").strip()
                    if novo_nome:
                        query = "UPDATE produtos SET nome = ? WHERE id = ?"
                        self.db.executar_query(query, (novo_nome, produto_id))
                        produto = dict(produto)
                        produto['nome'] = novo_nome
                        print("✅ Nome atualizado!")
                    else:
                        print("❌ Nome não pode estar vazio.")
                
                elif escolha == '2':
                    try:
                        novo_preco = float(input("Novo preço: R$"))
                        if novo_preco >= 0:
                            query = "UPDATE produtos SET preco = ? WHERE id = ?"
                            self.db.executar_query(query, (novo_preco, produto_id))
                            produto = dict(produto)
                            produto['preco'] = novo_preco
                            print("✅ Preço atualizado!")
                        else:
                            print("❌ Preço não pode ser negativo.")
                    except ValueError:
                        print("❌ Preço inválido.")
                
                elif escolha == '3':
                    novo_tamanho = input("Novo tamanho (P, M, G, GG): ").upper().strip()
                    if novo_tamanho in Produto.tamanhos_validos:
                        query = "UPDATE produtos SET tamanho = ? WHERE id = ?"
                        self.db.executar_query(query, (novo_tamanho, produto_id))
                        produto = dict(produto)
                        produto['tamanho'] = novo_tamanho
                        print("✅ Tamanho atualizado!")
                    else:
                        print("❌ Tamanho inválido.")
                
                elif escolha == '4':
                    try:
                        novo_estoque = int(input("Novo estoque: "))
                        if novo_estoque >= 0:
                            query = "UPDATE produtos SET estoque = ? WHERE id = ?"
                            self.db.executar_query(query, (novo_estoque, produto_id))
                            produto = dict(produto)
                            produto['estoque'] = novo_estoque
                            print("✅ Estoque atualizado!")
                        else:
                            print("❌ Estoque não pode ser negativo.")
                    except ValueError:
                        print("❌ Estoque inválido.")
                
                elif escolha == '5':
                    break
                else:
                    print("❌ Opção inválida.")
                    
        except ValueError:
            print("❌ ID inválido.")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def excluir_produto(self):
        """Exclui um produto"""
        if not self.listar_produtos():
            return
        
        try:
            produto_id = int(input("\nID do produto para excluir: "))
            produto = self.buscar_produto_por_id(produto_id)
            
            if not produto:
                print("❌ Produto não encontrado.")
                return
            
            confirmacao = input(f"Confirma exclusão de '{produto['nome']}'? (s/N): ").lower()
            
            if confirmacao == 's':
                query = "DELETE FROM produtos WHERE id = ?"
                resultado = self.db.executar_query(query, (produto_id,))
                
                if resultado:
                    print(f"🗑️ Produto '{produto['nome']}' excluído com sucesso!")
                else:
                    print("❌ Erro ao excluir produto.")
            else:
                print("❌ Exclusão cancelada.")
                
        except ValueError:
            print("❌ ID inválido.")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def menu(self):
        """Menu principal da loja"""
        while True:
            print("\n" + "="*40)
            print("👕 GERENCIAMENTO LOJA DE ROUPAS")
            print("="*40)
            print("1. Adicionar produto")
            print("2. Listar produtos")
            print("3. Buscar produtos")
            print("4. Atualizar produto")
            print("5. Excluir produto")
            print("6. Voltar ao menu principal")
            print("="*40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.adicionar_produto()
            elif opcao == '2':
                self.listar_produtos()
            elif opcao == '3':
                self.buscar_produtos()
            elif opcao == '4':
                self.atualizar_produto()
            elif opcao == '5':
                self.excluir_produto()
            elif opcao == '6':
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
