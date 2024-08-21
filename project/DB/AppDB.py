# import psycopg2
# from psycopg2 import sql
# from datetime import datetime
#
# class AppDB:
#
#     def __init__(self):
#         self.url = "dbname='postgres' user='postgres' host='localhost' password='131627'"
#         self.connection = None
#
#     # ABRIR CONEXÃO COM O BANCO
#     def abrirConexao(self):
#         try:
#             self.connection = psycopg2.connect(self.url)
#             #print("Conexão aberta!\n")
#         except Exception as e:
#             print(e)
#
#     # FECHAR CONEXÃO COM O BANCO
#     def fecharConexao(self):
#         try:
#             if self.connection:
#                 self.connection.close()
#                 #print("\nConexão fechada!")
#         except Exception as e:
#             print(e)
#
#     # SELECIONA TODOS OS DADOS DA TABELA CHAMADO
#     def selecionarDados(self):
#         query = sql.SQL("SELECT * FROM \"CHAMADO\"")
#
#         try:
#             self.abrirConexao()
#             with self.connection.cursor() as cursor:
#                 cursor.execute(query)
#                 rows = cursor.fetchall()
#                 for row in rows:
#                     print(f"ID: {row[0]}\nLocal: {row[1]}\nDescrição: {row[2]}\nAbertura: {row[3]}\nFechamento: {row[4]}\n")
#                 return rows
#         except Exception as e:
#             print(e)
#             return None
#         finally:
#             self.fecharConexao()
#
#     # INSERIR DADOS NA TABELA CHAMADO
#     def inserirChamado(self, id, local, descricao, abertura):
#         insert_query = sql.SQL("INSERT INTO \"CHAMADO\" (\"CODIGO\", \"LOCAL\", \"DESCRICAO\", \"ABERTURA\") VALUES (%s, %s, %s, %s)")
#
#         try:
#             self.abrirConexao()
#             with self.connection.cursor() as cursor:
#                 cursor.execute(insert_query, (id, local, descricao, abertura))
#                 self.connection.commit()
#                 print("Registro inserido com sucesso!")
#         except Exception as e:
#             print("Falha ao inserir os dados na tabela")
#             print(e)
#         finally:
#             self.fecharConexao()
#
#     # ATUALIZAR DADOS NA TABELA CHAMADO
#     def atualizarChamado(self, id, local_novo, descricao_nova):
#         select_query = sql.SQL("SELECT * FROM \"CHAMADO\" WHERE \"CODIGO\" = %s")
#         update_query = sql.SQL("UPDATE \"CHAMADO\" SET \"LOCAL\" = %s, \"DESCRICAO\" = %s WHERE \"CODIGO\" = %s")
#
#         try:
#             self.abrirConexao()
#             with self.connection.cursor() as cursor:
#                 cursor.execute(select_query, (id,))
#                 print("Seleção antes da atualização.")
#                 rows = cursor.fetchall()
#                 for row in rows:
#                     print(f"Código: {row[0]}\nLocal: {row[1]}\nDescrição: {row[2]}")
#
#                 cursor.execute(update_query, (local_novo, descricao_nova, id))
#                 self.connection.commit()
#                 print("Atualização realizada com sucesso!")
#
#                 cursor.execute(select_query, (id,))
#                 print("Seleção depois da atualização.")
#                 rows = cursor.fetchall()
#                 for row in rows:
#                     print(f"Código: {row[0]}\nLocal: {row[1]}\nDescrição: {row[2]}")
#         except Exception as e:
#             print(e)
#         finally:
#             self.fecharConexao()
#
#     # FINALIZAR O TICKET DA TABELA DE CHAMADOS
#     def finalizarChamado(self, id):
#         query = sql.SQL("UPDATE \"CHAMADO\" SET \"FECHAMENTO\" = %s WHERE \"CODIGO\" = %s")
#
#         try:
#             self.abrirConexao()
#             with self.connection.cursor() as cursor:
#                 now = datetime.now().strftime("%Y-%m-%d")
#                 cursor.execute(query, (now, id))
#                 self.connection.commit()
#                 print("Chamado finalizado.")
#         except Exception as e:
#             print(e)
#         finally:
#             self.fecharConexao()
#
#     # DELETAR CHAMADO DO BANCO DE DADOS
#     def deletarChamado(self, id):
#         delete_query = sql.SQL("DELETE FROM \"CHAMADO\" WHERE \"CODIGO\" = %s")
#
#         try:
#             self.abrirConexao()
#             with self.connection.cursor() as cursor:
#                 cursor.execute(delete_query, (id,))
#                 self.connection.commit()
#                 print("Chamado deletado!")
#         except Exception as e:
#             print(e)
#         finally:
#             self.fecharConexao()