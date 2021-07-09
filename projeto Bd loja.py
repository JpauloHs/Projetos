import matplotlib.pyplot as plt
import pymysql.cursors

conexao = pymysql.Connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'pro',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
    
)
'''cadastro usuario'''

autentico = False

def cadastro():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Insira seu nome: \n')
        senha = input('Insira sua senha: \n')
        print('Entrando...')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            print('usuario ou senha errada')
                
    
    elif decisao == 2:
        print('Faça seu cadastro: ')
        nome = input('Insira seu nome: \n')
        senha = input('Insira sua senha: \n')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1

        if usuarioExistente == 1:
            print('Usuario ja cadastrado, tente um nome diferente!')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s,%s)', (nome, senha, 1))
                    conexao.commit()
                    print('Usuario cadastrado com sucesso!')
            except:
                print('Erro ao ensirir os dados!')

    return autenticado, usuarioMaster                                                     

def cadastrarProdutos():
    nome = input('Insira o nome do produto: ')
    departamento = input('Insiro o nome do departamento: ')
    preco = float(input('Insira o preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos(nome, departamento, preco) values (%s,%s,%s)',(nome, departamento, preco))
            conexao.commit()
            print('Produto cadastrado!')
    except:
        print('Erro ao inserir produto! tente novamente.')        

def listarProdutos():
    produtos = []
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao se conectar ao Banco de Dados! Tente novamente.')

    for i in produtosCadastrados:
        produtos.append(i)

    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto encontrado!')           

def deletarProdutos():
    DelP = int(input('Insira o id do produto para exclui-lo: \n'))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produtos where id ={}'.format(DelP))
            print('Produto Excluido!\n')
    except:
        print('Erro ao excluir produto! Insira o id novamente: \n')        

def listaPedidos():
    pedidos = []
    decision = 0
    while decision != 2:
        pedidos.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listapedidos.fetchall()
        except:
            print('Erro no banco de dados! Tente novamente.\n') 

        for i in listaPedidos:
            pedidos.append()
            
        if len(pedidos) != 0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('Pedido entregue!')     

            decision = int(input('1 para dar baixa no pedido:\n2 para voltar:'))  

            if decision == 1:
                idDeletar = int(input('Insira o id do produto para dar baixa:'))

                try:
                    with conexao.cursor() as cursor:
                        cursor.execute('delete from pedidos where id={}'.format(idDeletar))  
                        print('Produto Entregue!')
                except:
                    print('Produto nao foi entregue!')        

def estatisticas():

    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('Erro no banco de dados!') 

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticavendas') 
            vendido = cursor.fetchall()
    except:
        print('nErro no banco de dados!')


    estado = int(input('0 Para sair:\n1 Para pesquisar por nome:\n2 Para pesquisar por departamento:'))

    if estado == 1:
        decisao3 = int(input('1 Para pesquisar por dinheiro\n2 Para pesquisar por quantidade:'))
        if decisao3 == 1:   

            for i in produtos:
                nomeProdutos.append(i['nome'])

            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('QTD Vendidos em reais:')
            plt.xlabel('Produtos:')
            plt.show()            
        if decisao3 == 2:
            unico = []
            unico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    dep = cursor.fetchall()
            except:
                print('Erro no banco de dados') 

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticavendas')
                    vendidoD= cursor.fetchall()
            except:
                print('Erro no banco de dados')

            for i in dep:
                unico.append(i['nome'])

                unico = sorted(set(unico))

            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(unico)):
                qntUnitaria = 0
                for i in vendidoD:
                    if unico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)


            plt.plot(unico, qntFinal)
            plt.ylabel('Quantidade:')
            plt.xlabel('Produtos:')
            plt.show()




while not autentico:
    decisao = int(input('1 para entrar; \n2 para cadastrar; '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()
    except:
        print('Erro ao conectar no Banco de Dados!')

    
    autentico, usuarioSupremo = cadastro()


if autentico:
    if usuarioSupremo == True:
        decisaoUsuario = 1
        while decisaoUsuario != 0:
            decisaoUsuario = int(input('0 para sair:\n1 para cadastrar produtos:\n2 para listar produtos:\n3 para vizualizar estatisticas:'))
            print('\n')
            if decisaoUsuario == 1:
                cadastrarProdutos()
                print('\n')
            elif decisaoUsuario == 2:
                listarProdutos()
                print('\n')
                deletar = int(input('1 para excluir um produto:\n2 para sair:'))  
                if deletar == 1:
                    deletarProdutos()
                    print('\n')  
            elif decisaoUsuario == 3:
                estatisticas()

            
                
