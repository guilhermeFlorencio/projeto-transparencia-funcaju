import cx_Oracle

host  = 'localhost'
porta = 1521
sid   = 'xe'
usuario = 'sys'
senha = '1234'

def conectar_ao_oracle(host, porta, sid, usuario, senha):
    try:
        # Crie uma conexão com o Oracle
        dsn = cx_Oracle.makedsn(host, porta, sid)
        conexao = cx_Oracle.connect(usuario, senha, dsn)

        # Retorne a conexão para ser usada em outras partes do código
        return conexao
    except cx_Oracle.Error as erro:
        print(f"Erro ao conectar ao Oracle: {erro}")
        return None

# Exemplo de uso:
if __name__ == "__main__":
    host = "localhost"
    porta = 1521  # Porta padrão do Oracle
    sid = "xe"  # Substitua pelo SID do seu banco de dados
    usuario = "sys"
    senha = "1234"

    conexao = conectar_ao_oracle(host, porta, sid, usuario, senha)
    if conexao:
        print("Conexão bem-sucedida ao Oracle!")
        # Aqui você pode executar consultas SQL ou outras operações no banco de dados
        # Lembre-se de fechar a conexão quando terminar: conexao.close()
    else:
        print("Falha na conexão ao Oracle.")
