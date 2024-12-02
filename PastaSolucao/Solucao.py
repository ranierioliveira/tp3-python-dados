# Elaborore aqui a sua solução do TP
import csv
import pandas as pd
from sqlalchemy import create_engine

def leitura_arquivo_csv_10_primeiros(arquivo_csv):
    '''
    'Printa' os 10 primeiros elementos de um arquivo csv
    
    Parâmetro:
    arquivo(str): nome do arquivo csv
    
    Atendendo os tópicos 1 e 2
    '''

    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=';')
            cabecalho = leitor.fieldnames
            for index, linha in enumerate(leitor, start=1):
                print(linha)
                if index == 10:
                    break   
            print('\nColunas do arquivo csv: ')
            for item in cabecalho:
                print(item)
                
    except FileNotFoundError:
        print(f"Arquivo {arquivo_csv} não encontrado")

def usuarios_mais_30(nome_arquivo):
    '''# Lê o arquivo CSV como um DataFrame, filtra e ,
    retorna um novo arquivo CSV
    
    Parâmetro:
    nome_arquivo (str): nome do arquivo
    
    Retorna:
    Arquivo CSV com os usuários com mais de 30
    '''
    df = pd.read_csv(nome_arquivo, delimiter=';')
    df_maior_que_30 = df[df['idade'] > 30]
    df_maior_que_30.to_csv('INFwebNET_30mais.xlsx', index=False)
    return df_maior_que_30

def limpeza_dados_usuarios(arquivo):
    '''
    Remove alguns usuários, e coloca valor padrão para outros
    
    Parâmetro:
    arquivo (str): nome do arquivo
    
    Retorna com alguns valores preenchidos e com alguns usuários removidos
    '''
    df = pd.read_csv(arquivo, delimiter=';')
    
    #Removendo os usuários com campo email vazio
    df_usuarios_com_email = df.dropna(subset=['email']) 
    df_usuarios_com_email['cidade'].fillna('Não Informada')
    df_usuarios_com_email['estado'].fillna('ZZ')
    return df_usuarios_com_email
    
def leitura_arquivo_excel(arquivo):
    '''
    Faz a leitura de um arquivo excel, contendo duas tabelas, une-as e remove as duplicatas baseadas no id
    
    Parâmetro:
    arquivo (str): nome do arquivo
    
    Retorna:
    Número de linhas de cada planilha ou uma exceção. Além retornar um df concatenado
    
    Tópico 5 e 6 do enunciado
    '''
    try:
        df_2022 = pd.read_excel(arquivo, sheet_name='INFwebNET2022')
        df_2023 = pd.read_excel(arquivo, sheet_name='INFwebNET2023')
        
        print(f'Número de linhas planilha de 2022: {len(df_2022)}')
        print(f'Número de linhas planilha de 2023: {len(df_2023)}')
        
        df_combinado = pd.concat([df_2022, df_2023], axis=0, ignore_index=True)
        df_combinado_formatado = df_combinado.drop_duplicates(subset=['id'])
        return df_combinado_formatado
    except FileNotFoundError as e:
        print('Arquivo não encontrado.', e)
    except Exception as e:
        print("Ocorreu um erro desconhecido durante a execução:", e)
    
def unindo_dfs(primeiro_df, segundo_df):
        '''
        Uni dois dfs
        
        Parâmetros:
        primeiro_df (df)
        segundo_df (df)
        
        Retorna a união dos dois dfs
        '''
        df_consolidado = pd.concat([primeiro_df, segundo_df], axis=0, ignore_index=True)
        return df_consolidado
        

leitura_arquivo_csv_10_primeiros('dados_usuarios.csv')
df_usuarios = usuarios_mais_30('dados_usuarios.csv')
df_usuarios_formatado = limpeza_dados_usuarios('dados_usuarios.csv')
df_historico_completo = leitura_arquivo_excel('INFwebNET_Historico.xlsx')
consolidado = unindo_dfs(df_usuarios_formatado, df_historico_completo) #Une os dois dfs

#Cria a conexão com o banco
engine = create_engine('sqlite:///INFwebNET.db')

#Insere as informações do histórico em uma tabela
df_historico_completo.to_sql('Usuarios_Historicos', engine, if_exists='replace', index=False)

#Insere as informações unificados em uma tabela
consolidado.to_sql('Consolidado', engine, if_exists='replace', index=False)

#Query para selecionar os usúrios do histórico
query = "SELECT * FROM Usuarios_Historicos WHERE idade BETWEEN 22 AND 30"
df_consulta_usuarios = pd.read_sql(query, engine)
print(df_consulta_usuarios.to_string())

query2 = "SELECT * FROM Consolidado"
df_consulta_completa = pd.read_sql(query2, engine)
print(df_consulta_completa.to_string())