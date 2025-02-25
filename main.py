import os
import pandas as pd

caminho_base = input('Cole o caminho da pasta: ') # Caminho da pasta onde estão os arquivos

caminho_saida = input('Cole o caminho da pasta onde o arquivo .CSV será salvo: ')

nome_do_txt = input('Digite o nome do arquivo .txt: ')

# Verifica se a pasta de saída existe; se não, cria a pasta
if not os.path.exists(caminho_saida):
    print(f'A pasta de saída "{caminho_saida}" não existe. Criando...')
    os.makedirs(caminho_saida)


dados_clientes = [] # Lista para armazenar os dados dos clientes

clientes_desejados = input('clientes que devem ser verificado[separados por ,]:') # Clientes que devem ser verificados

lista_clientes_desejados = [cliente.strip() for cliente in clientes_desejados.split(',')]# Transforma a variavel clientes_desejados em uma Lista com os clientes que devem ser verificados

lista_clientes_desejados = list(set(lista_clientes_desejados))

for numero_cliente in lista_clientes_desejados: # Para cada cliente na lista de clientes desejados
    
    caminho_pasta_cliente = os.path.join(caminho_base, numero_cliente) # Cria o caminho completo da pasta do cliente
    
    try:
        os.chdir(caminho_pasta_cliente) # Muda o diretório de trabalho para a pasta do cliente
        
        print(f'Pasta do cliente: {caminho_pasta_cliente}') # Exibe o caminho da pasta do cliente
       	
        caminho_arquivo_txt = os.path.join(caminho_pasta_cliente, nome_do_txt + '.txt') # Cria o caminho completo do arquivo .txt
        
        
        if os.path.isfile(caminho_arquivo_txt):
            print(f'Aquivo {numero_cliente} encontrado') # Exibe mensagem de sucesso caso o arquivo seja encontrado
            with open(caminho_arquivo_txt, 'r') as arquivo_txt:
                linhas = arquivo_txt.readlines()
                
                if not linhas:  # Verifica se o arquivo está vazio
                    print(f'Arquivo {numero_cliente} está vazio.')
                
                else:          
                    acesso = None
                    senha = None
                    senha_nova = None
                    cnpj = None
                    login = None
                
                    for linha in linhas:
                        linha_lower = linha.lower()
                        
                        if any(palavra in linha_lower for palavra in ['acessos:', "acesso:" ]):  # Verifica se a linha contém 'Acesso:' ou 'acesso:'
                            acesso = linha.split(':')[1].strip()  # Pega o valor após o ':' e salva em acesso
                        elif any(palavra in linha_lower for palavra in ['senha:', 'senhas:']): # Verifica se a linha contém 'Senha:' ou 'senha:'
                            senha = linha.split(':')[1].strip()    
                        elif any(palavra in linha_lower for palavra in ['novo', 'nova', 'novas', 'novos']): # Verifica se a linha contém 'Senha:' ou 'senha:'
                            senha_nova = linha.split(':')[1].strip()
                        elif 'cnpj' in linha_lower:  # Verifica se a linha contém 'CNPJ:' ou 'cnpj:'
                            cnpj = linha.split(':')[1].strip()
                        elif any(palavra in linha_lower for palavra in['login', 'logins']): # Verifica se a linha contém 'Login:' ou 'login:'
                            login = linha.split(':')[1].strip()

                if senha or acesso or cnpj or login:
                    dados_clientes.append([numero_cliente, acesso, senha, senha_nova, cnpj, login]) 
                    print(f'Dados do cliente {numero_cliente} salvos:')
                    print(f'  Acesso: {acesso}')
                    print(f'  Senha: {senha}')
                    print(f'  Nova senha: {senha_nova}')
                    print(f'  CNPJ: {cnpj}')
                    print(f'  Login: {login}')
                    print('-' * 30)  # Linha separadora para melhor visualização # Exibe os dados do cliente
                
        else:
            print(f'Arquivo {numero_cliente} não encontrado') 
            # Exibe mensagem de erro caso o arquivo não seja encontrado
            print('-' * 30)  # Linha separadora para melhor visualização # Exibe os dados do cliente
               
    except FileNotFoundError:
        print(f'Pasta do cliente {numero_cliente} não encontrado')
        # Exibe mensagem de erro caso a pasta do cliente não seja encontrada
        print('-' * 30)  # Linha separadora para melhor visualização # Exibe os dados do cliente
        
    except Exception as e:
        print(f'Erro inesperado ao acessar a pasta do cliente {numero_cliente}: {e}')
        # Exibe mensagem de erro caso ocorra um erro inesperado ao acessar a pasta do cliente
        print('-' * 30)  # Linha separadora para melhor visualização # Exibe os dados do cliente
        
df = pd.DataFrame(dados_clientes, columns=['Cliente', 'Acesso', 'Senha', 'Nova Senha','CNPJ', 'Login'])
# Salva o DataFrame em um arquivo Excel

caminho_arquivo_csv = os.path.join(caminho_saida, 'dados_clientes.csv')

df.to_csv(caminho_arquivo_csv, index=False)

print(f'\nPlanilha criada com sucesso em {caminho_arquivo_csv}')  # Exibe mensagem de sucesso

finalizar_programa = input('Digite qualquer coisa para fechar o programa:')
