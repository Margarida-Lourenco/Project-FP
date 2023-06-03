
def limpa_texto(c):
    """
Recebe uma cadeia de caracteres e devolve uma cadeia de caracteres limpa 
(sem caracteres brancos e sem espaços em excesso).
"""
    l = c.split()   
    total = ''
    for i in range(len(l)): 
        palavra = l[i] + ' '
        total += palavra
    return total.rstrip() 
    

def corta_texto (c,num):
    """
Recebe uma cadeia de caracteres limpa e um inteiro positivo. Devolve um tuplo 
com duas subcadeias obtidas a partir da cadeia de entrada. A primeira subcadeia 
tem comprimento num e a segunda subcadeia contem o resto da cadeia de entrada. 
"""
    c = limpa_texto(c) 
    lst = c.split()  # retorna uma lista com as palavras completas
    c1 =''
    t = ()
    if c == '':
        return(c, '')
    if len(lst) == 1:
        return (lst[0], '')
    for i in range (len(lst)):
        if len(c1) + len(lst[i]) <= num: 
            c1 += lst[i] + ' ' 
            t += (c1.rstrip(),) 
        else:
            break
    t1 = ((t[len(t)-1]),)  # cria um tuplo com a ultima subcadeia de t
    return t1 + (((c[len(t1[0]):]).lstrip()),)   


def insere_espacos(c1,num1):
    """
    Recebe uma cadeia de caracteres limpa e um inteiro positivo. Verifica se a 
    cadeia tem pelos menos duas palavras.  Se sim, adiciona espacos entre as 
    palavras ate ao comprimento num1, caso contrario devolve a cadeia original 
    seguida de espaços ate ter comprimento num1.
    """
    c1 = limpa_texto(c1)
    lst1 = c1.split() 
    if len(lst1) >= 2: 
        while len(c1) < num1:
            for i in range(len(lst1)-1):
                if len(c1) < num1:
                    lst1[i] += ' '
                    c1 = ' '.join(lst1)
        return c1
    else:
        while len(c1) < num1:
            c1 += ' '
    return c1

def justifica_texto(c2,num2):
    """
    Recebe uma cadeia de caracteres limpa e um inteiro positivo. Devolve um tuplo 
    onde cada elemento e uma subcadeia justificada.  Verifica a validade dos argumentos,
    gerando um ValueError caso os argumentos nao sejam validos.
    """
    t = ()
    if c2 == '' or type(num2)!= int or num2 < 0:
        raise ValueError('justifica_texto: argumentos invalidos')
    if not isinstance(c2,str):
        raise ValueError('justifica_texto: argumentos invalidos')
    lst = c2.split()
    for i in range (len(lst)):
        if len(lst[i]) > num2:
            raise ValueError('justifica_texto: argumentos invalidos')
    t = corta_texto(((c2)),num2)
    t1 = [insere_espacos(t[0],num2)]
    while t[1] != '':  # enquanto a segunda subcadeia nao for vazia continua a dividir o texto
        t = corta_texto(t[1],num2)
        t1.append(insere_espacos(t[0],num2))
    t1[-1] = limpa_texto(t1[-1]) + ' ' * ((num2) - len(limpa_texto(t1[-1])))
    return tuple(t1)
        

def calcula_quocientes(votos,n_deputados):
    """
    Recebe um dicionario com os votos de cada partido e o numero de deputados a eleger.
    Devolve um dicionario com os quocientes.  Nao altera o dicionario original.
    """
    a = list(votos.keys())
    d = dict(dict.fromkeys(a,[])) 
    for i in range(len(votos)): 
        d[a[i]] = [votos[a[i]]/n for n in range(1,n_deputados+1)]  # valores passam a ser listas com os quocientes
    return d

def atribui_mandatos(dic, num_depu): 
    """
    Recebe um dicionario e o numero de deputados a eleger. Devolve uma lista com os 
    partidos ordenados por ordem de eleicao (o partido com o primeiro deputado e o 
    primeiro da lista, o partido com o segundo deputado e o segundo da lista, etc).
    Nao altera o dicionario passado como argumento de entrada.
    """
    def compara(x):
            return dic[x]
    def ordena(partidos):
            return sorted(partidos, key = compara)
    d = calcula_quocientes(dic, num_depu)
    a = list(dict.values(d)) 
    b = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] not in b:
                 b.append(a[i][j])  # lista com todos os quocientes unicos
    b.sort(reverse = True)  # ordena a lista de forma decrescente
    deputados = []
    while len(deputados) < num_depu:
        lista_t = []
        q1 = b[0]
        del b[0]
        for partido in d:
            if q1 in d[partido]:
                lista_t += [partido]
        deputados += ordena(lista_t)
    return deputados[:num_depu]            


def obtem_partidos(d):
    """
    Recebe um dicionario e devolve uma lista ordenada (por ordem alfabetica) com os
    partidos que participaram nas eleicoes.  Nao altera o dicionario original.
    """
    partidos = []
    for circulo in d:
        for partido in d[circulo]['votos']:
            if partido not in partidos: 
                partidos.append(partido) 
    return sorted(partidos)


def obtem_resultado_eleicoes(dic):
    """
    recebe um dicionario e devolve a lista ordenada de comprimento igual ao numero total
    de partidos com os resultados das eleicoes.  Nao altera o dicionario original.
    Verifica a validade dos argumentos, gerando um ValueError caso nao sejam validos.
    """
    if not isinstance(dic,dict) or dic == {}:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    for circulo in dic:
        if len(dic[circulo]) != 2:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if not isinstance(circulo, str) or circulo == '':
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if dic[circulo]['deputados'] < 1 or dic[circulo]['votos'] == {}:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if not isinstance(dic[circulo]['deputados'], int) or not isinstance(dic[circulo]['votos'], dict):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido') 
        for partido in dic[circulo]['votos']:
            if not isinstance(dic[circulo]['votos'][partido], int):
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            if dic[circulo]['votos'][partido] <= 0 :
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            if partido == '' or not isinstance(partido, str):
                raise ValueError('obtem_resultado_eleicoes: argumento invalido')
            
    partidos = obtem_partidos(dic)
    deputados = []
    votos = []
    atribui = []
    for partido in partidos:
        deputados.append(0)
        votos.append(0)
    for circulo in dic: 
        atribui += atribui_mandatos(dic[circulo]['votos'], dic[circulo]['deputados'])
    for partido in atribui:
        deputados[partidos.index(partido)] += 1 
    for circulo in dic:
        for partido in dic[circulo]['votos']:
            votos[partidos.index(partido)] += dic[circulo]['votos'][partido] 
    tuplos = []
    for i in range(len(partidos)):
        tuplos.append((partidos[i],deputados[i],votos[i]))   
    return sorted(tuplos, key = lambda tuplo: tuplo[2], reverse = True)


def produto_interno(t1,t2):
    """
    Recebe como argumento dois vetores e calcula o seu produto interno.
    """
    total = 0
    if len(t1) != len(t2):
        raise ValueError("Os tuplos devem ser da mesma dimensao")
    for i in range (len(t1)):
        total = total + ((t1[i]) * (t2[i])) 
    return float(total)  

def verifica_convergencia(v,c,x,E):
    """
    Recebe como argumentos uma matriz, um vetor das constantes, um vetor x 
    (solucao atual) e um numero real E. Devolve True se o valor absoluto 
    do erro de todas as equacoes for inferior a precisao (E) e False caso contrario.
"""    
    soma = 0 
    for i in range (len(v)):
        soma += abs((produto_interno(v[i],x)) - c[i]) 
    if soma < E: 
       return True 
    return False
  

def tuplo_lista2(tuplo):
    lista = []
    for i in range(len(tuplo)):
        lista.append(tuplo_lista(tuplo[i]))
    return lista

def tuplo_lista(tuplo):
    lista = []
    for i in range(len(tuplo)):
        lista.append(tuplo[i])
    return lista

def tuplo(matriz):
    for i in range(len(matriz)):
        matriz[i] = tuple(matriz[i])
    return tuple(matriz)

"""
Funcao tuplo_lista: converte o tuplo recebido em lista.
Funcao tuplo_lista2: converte o tuplo de tuplos recebido numa lista de listas.
Funcao tuplo: converte a lista de listas recebida num tuplo de tuplos.
"""    

def retira_zeros_diagonal(tt,tn): 
    """
    Recebe como argumento uma matriz e um vetor de constantes. Retira os zeros 
    da diagonal principal da matriz por troca de linhas, aplicando essa mesma 
    reordenacao ao vetor das constantes.
    """
    l = []
    tt = tuplo_lista(tt)
    tt= tuplo_lista2(tt)
    tn = tuplo_lista(tn)
    for i in range(len(tt)):
        if tt[i][i] == 0: 
            for j in range(len(tt[i])):
                if tt[j][i] != 0: 
                    tt[i],tt[j] = tt[j],tt[i]  # troca as linhas da matriz
                    tn[i],tn[j] = tn[j],tn[i]  # troca os valores das constantes
                    break
    return (tuplo(tt),tuple(tn))

def eh_diagonal_dominante(matriz):
    """
    recebe uma matriz. Retorna True se a matriz for diagonal dominante e 
    False caso nao seja.
    """
    for i in range(len(matriz)):
        soma = 0
        for j in range(len(matriz)):
            if i != j:
                soma += abs(matriz[i][j])
        if abs(matriz[i][i]) < soma:
            return False
    return True

def resolve_sistema(tt1,tn1,precisao):
    """
Recebe uma matriz, um vetor de constantes e um valor real. Verifica os argumentos,
levantando erro caso nao sejam validos.  De seguida resolve o sistema de equacoes 
segundo o metodo de jacobi, devolvendo o resultado em forma de tuplo.
"""  
   
    if not isinstance(precisao, float) or precisao <= 0:
        raise ValueError("resolve_sistema: argumentos invalidos")
    if not isinstance(tt1, tuple) or not type(tn1) == tuple:
            raise ValueError("resolve_sistema: argumentos invalidos")
    if  len(tt1) != len(tn1):
        raise ValueError("resolve_sistema: argumentos invalidos")
    if tt1 == () or tn1 == (): 
            raise ValueError("resolve_sistema: argumentos invalidos")
    for i in range(len(tt1)):
        if not isinstance(tt1[i], tuple) or tt1[i] == ():
            raise ValueError("resolve_sistema: argumentos invalidos")
        if len(tt1[i]) != len(tt1):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for j in range(len(tt1)):
            if not isinstance(tt1[i][j], (float,int)):
                raise ValueError("resolve_sistema: argumentos invalidos")
        if not isinstance(tn1[i], (float,int)) or tn1[i] == ():
            raise ValueError("resolve_sistema: argumentos invalidos") 
            
    tt1,tn1 = retira_zeros_diagonal(tt1,tn1)
    if eh_diagonal_dominante(tt1) == False:
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")
    x = [0 for i in range(len(tt1))]  # vetor inicial
    while verifica_convergencia(tt1,tn1,x,precisao) == False:  # enquanto o sistema nao convergir
        for i in range(len(tt1)): 
            soma = 0
            for j in range(len(tt1)): 
                if i != j:
                    soma += (tt1[i][j] * x[j])  
            x[i] = (tn1[i] - soma) / tt1[i][i]  
    return tuple(x)




            



        
    
   
