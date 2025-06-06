#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para visualizar dados do banco SQLite de forma organizada
"""

import sqlite3
from datetime import datetime

def conectar_banco(db_name="sistema_comercial.db"):
    """Conecta ao banco de dados"""
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def visualizar_tabela(nome_tabela):
    """Visualiza uma tabela específica"""
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Buscar dados
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        dados = cursor.fetchall()
        
        if not dados:
            print(f"📭 Tabela '{nome_tabela}' está vazia.")
            return
        
        # Buscar nomes das colunas
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = [col[1] for col in cursor.fetchall()]
        
        print(f"\n📊 TABELA: {nome_tabela.upper()}")
        print("=" * 80)
        
        # Cabeçalho
        header = " | ".join([f"{col[:15]:15}" for col in colunas])
        print(header)
        print("-" * len(header))
        
        # Dados
        for linha in dados:
            valores = []
            for valor in linha:
                if valor is None:
                    valores.append("N/A".ljust(15))
                else:
                    str_valor = str(valor)[:15]
                    valores.append(str_valor.ljust(15))
            print(" | ".join(valores))
        
        print(f"\n📈 Total de registros: {len(dados)}")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao consultar tabela: {e}")
    finally:
        conn.close()

def listar_tabelas():
    """Lista todas as tabelas do banco"""
    conn = conectar_banco()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        return tabelas
    except sqlite3.Error as e:
        print(f"❌ Erro ao listar tabelas: {e}")
        return []
    finally:
        conn.close()

def estatisticas_banco():
    """Mostra estatísticas gerais do banco"""
    tabelas = listar_tabelas()
    
    if not tabelas:
        print("📭 Banco de dados vazio ou não encontrado.")
        return
    
    print("\n📊 ESTATÍSTICAS DO BANCO")
    print("=" * 40)
    
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            
            for tabela in tabelas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"📋 {tabela.capitalize():15}: {count:3} registros")
                
        except sqlite3.Error as e:
            print(f"❌ Erro: {e}")
        finally:
            conn.close()

def exportar_para_csv(nome_tabela):
    """Exporta uma tabela para CSV"""
    import csv
    
    conn = conectar_banco()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        dados = cursor.fetchall()
        
        if not dados:
            print(f"📭 Tabela '{nome_tabela}' está vazia.")
            return
        
        # Nome do arquivo
        arquivo_csv = f"{nome_tabela}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Buscar nomes das colunas
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = [col[1] for col in cursor.fetchall()]
        
        # Escrever CSV
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(colunas)  # Cabeçalho
            
            for linha in dados:
                writer.writerow(linha)
        
        print(f"✅ Dados exportados para: {arquivo_csv}")
        
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")
    finally:
        conn.close()

def menu_visualizador():
    """Menu principal do visualizador"""
    while True:
        print("\n" + "="*50)
        print("🔍 VISUALIZADOR DE BANCO DE DADOS")
        print("="*50)
        print("1. Ver estatísticas gerais")
        print("2. Visualizar tabela específica")
        print("3. Visualizar todas as tabelas")
        print("4. Exportar tabela para CSV")
        print("5. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            estatisticas_banco()
            
        elif opcao == '2':
            tabelas = listar_tabelas()
            if tabelas:
                print("\nTabelas disponíveis:")
                for i, tabela in enumerate(tabelas, 1):
                    print(f"{i}. {tabela}")
                
                try:
                    escolha = int(input("\nEscolha uma tabela: ")) - 1
                    if 0 <= escolha < len(tabelas):
                        visualizar_tabela(tabelas[escolha])
                    else:
                        print("❌ Opção inválida.")
                except ValueError:
                    print("❌ Digite um número válido.")
            else:
                print("📭 Nenhuma tabela encontrada.")
                
        elif opcao == '3':
            tabelas = listar_tabelas()
            for tabela in tabelas:
                visualizar_tabela(tabela)
                
        elif opcao == '4':
            tabelas = listar_tabelas()
            if tabelas:
                print("\nTabelas disponíveis:")
                for i, tabela in enumerate(tabelas, 1):
                    print(f"{i}. {tabela}")
                
                try:
                    escolha = int(input("\nEscolha uma tabela para exportar: ")) - 1
                    if 0 <= escolha < len(tabelas):
                        exportar_para_csv(tabelas[escolha])
                    else:
                        print("❌ Opção inválida.")
                except ValueError:
                    print("❌ Digite um número válido.")
            else:
                print("📭 Nenhuma tabela encontrada.")
                
        elif opcao == '5':
            print("👋 Saindo do visualizador...")
            break
            
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    menu_visualizador()
