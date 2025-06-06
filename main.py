#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento - Arquivo Principal
Gerencia Loja de Roupas, Clientes e Fornecedores
"""

from database import DatabaseManager
from loja import LojaCRUD
from cliente import ClienteCRUD
from fornecedor import FornecedorCRUD

def menu_principal():
    """Menu principal do sistema"""
    # Inicializar banco de dados
    db = DatabaseManager()
    db.criar_tabelas()
    
    # Inicializar CRUDs
    loja = LojaCRUD(db)
    cliente = ClienteCRUD(db)
    fornecedor = FornecedorCRUD(db)
    
    while True:
        print("\n" + "="*50)
        print("🏪 SISTEMA DE GERENCIAMENTO COMERCIAL")
        print("="*50)
        print("1. 👕 Gerenciar Loja de Roupas")
        print("2. 👤 Gerenciar Clientes")
        print("3. 🏭 Gerenciar Fornecedores")
        print("4. 🚪 Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            loja.menu()
        elif opcao == '2':
            cliente.menu()
        elif opcao == '3':
            fornecedor.menu()
        elif opcao == '4':
            print("👋 Encerrando o sistema...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
