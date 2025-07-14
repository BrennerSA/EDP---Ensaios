# -*- coding: utf-8 -*-
#SQL
import os
import sqlite3
import time
import datetime
import math
import banco.bdConfiguration as bdConfiguration
import locale


pi = math.pi

connection = sqlite3.connect('banco/banco.db', check_same_thread = False)
c = connection.cursor()

######################################################################################
################################### INICIAL ##########################################
######################################################################################
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, ensaio text, status text, identificacao text, tipo text, naturazaDaAmostra text, teorUmidade text, pesoEspecifico text, umidadeOtima text, energiaCompactacao text, grauCompactacao text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, obs text, freq int, pressaoConf text, pressaoDesvio text, tipoEstabilizante text, pesoEstabilizante int, tempoCura text, tecnico text, formacao text)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134ADM (idt text, fase text, x real, y1 real, yt1 real, y2 real, yt2 real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134 (idt text, fase text, pc real, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT179 (idt text, glp int, DR real, DP real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT181 (idt text, fase text, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS referenciaADM (idt text, fase text, r1 real, r2 real)")
    c.execute("CREATE TABLE IF NOT EXISTS referencia (idt text, fase text, r real)")
    
    

create_table()

######################################################################################
####################################  GERAL  #########################################
######################################################################################
'''Atualiza a frequencia do Ensaio de acordo com a idt'''
def Update_freq(idt, freq):
    c.execute("UPDATE dadosIniciais SET freq = ? WHERE identificacao = ?", (freq, idt,))
    connection.commit()

def diretorio_resultados(id,pathname):
    diretorio=str(pathname)
    c.execute("UPDATE dirResults SET path = ? WHERE id = ?", (pathname,id,))
    connection.commit()


def get_dir_result(id):
    path=c.execute('SELECT * FROM dirResults WHERE id = ?', (id,))
    list=[]
    for row in path:
        list.append(row[1])
    return list[0]


'''Data de quando finaliza o ensaio acordo com o idt'''
def data_final_Update_idt(idt):
    date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S  %d/%m/%Y'))
    status = '2'
    c.execute("UPDATE dadosIniciais SET status = ?, dataFim = ? WHERE identificacao = ?", (status, date, idt,))
    connection.commit()

'''Data de quando inicia o ensaio de acordo com o idt'''#pode ser juntado com o metodo update_freq
def data_inicio_Update_idt(idt):
    date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S  %d/%m/%Y'))
    status = '1'
    c.execute("UPDATE dadosIniciais SET status = ?, dataInicio = ? WHERE identificacao = ?", (status, date, idt,))
    connection.commit()


def dados_dnit183(idt,cp,resistencia,tensao,pressGolpe,qtdgolpe,diametro,espessura,mr):
    c.execute('INSERT INTO dadosDNIT183 (idt,cp, resistencia, nivel_tensao, pressao_golpe, Qtd_golpes, diametro, espessura,mr) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (idt,cp,resistencia,tensao,pressGolpe,qtdgolpe,diametro,espessura,mr))
    connection.commit()


'''coleta uma lista com os dados iniciais dos ensaio de acordo com o ID'''

def teste_pontos(nome,lista1,list2):
    i=0
    c.execute('CREATE TABLE IF NOT EXISTS SensoresLVDT (idt text, sensor1 real, sensor2 real)')
    for elemento1,elemento2 in zip(lista1,list2):
        c.execute('INSERT INTO SensoresLVDT (idt, sensor1, sensor2) VALUES (?, ?, ?)', (nome,elemento1,elemento2))
        i+=1
    connection.commit()
    print (i)

def teste_press(nome,fase,lista1,list2,lvdt1,lvdt2,timestamp,gAtual,gTotal):
    i=0
    c.execute('CREATE TABLE IF NOT EXISTS PressTeste (idt text,fase int, sensor1 real, sensor2 real, timestamp real, y1 real, y2 real, golpeAtual int ,total int)')
    for elemento1,elemento2,elemento3,elemento4,elemneto5,elemento6,elemento7 in zip(lista1,list2,timestamp,lvdt1,lvdt2,gAtual,gTotal):
        c.execute('INSERT INTO PressTeste (idt, fase, sensor1, sensor2, timestamp, y1, y2,golpeAtual, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (nome,fase,elemento1,elemento2,elemento3,elemento4,elemneto5,elemento6,elemento7))
        i+=1
    connection.commit()

def dados_iniciais_(idt):
    list = []
    tupla=c.execute('SELECT * FROM dadosIniciais WHERE identificacao = ?', (idt,))
    for row in tupla:
        list.append(row[1]) #0 ensaio
        list.append(row[2]) #1 status
        list.append(row[4]) #2 tipo
        list.append(row[5]) #3 naturazaDaAmostra
        list.append(row[6]) #4 teorUmidade
        list.append(row[7]) #5 pesoEspecifico
        list.append(row[8]) #6 umidadeOtima
        list.append(row[9]) #7 energiaCompactacao
        list.append(row[10]) #8 grauCompactacao
        list.append(row[11]) #9 datadacoleta
        list.append(row[12]) #10 datainicio
        list.append(row[13]) #11 datafim
        list.append(row[14]) #12 amostra
        list.append(row[15]) #13 diametro
        list.append(row[16]) #14 altura
        list.append(row[17]) #15 obs
        list.append(row[18]) #16 freq
        list.append(row[19]) #17 pressaoConf
        list.append(row[20]) #18 pressaoDesvio
        list.append(row[21]) #19 tipoEstabilizante
        list.append(row[22]) #20 pesoEstabilizante
        list.append(row[23]) #21 tempoCura
        list.append(row[24]) #22 tecnico
        list.append(row[25]) #23 formacao
        list.append(row[26]) #24 resistencia a tração
        list.append(row[27]) #25 nivel de tensao
        list.append(row[28]) #26 continuação
        list.append(row[29]) #27 mr medio

    return list

'''pega os tipo e a identificação do ensaio de acordo com o ID'''
def qual_identificador(id):
    list = []
    tupla=c.execute('SELECT * FROM dadosIniciais WHERE id = ?', (id,))
    for row in tupla:
        list.append(row[1])
        list.append(row[3])

    return list

def pulso135(nome,fase,X,Y):
    c.execute('INSERT INTO pulso135 (idt,fase, dadosX,dadosY) VALUES (?, ?, ?, ?)', (nome,fase,X,Y))
    connection.commit()

def getpulso135(idt):
    lista=[]
    l=[]
    tupla=c.execute('SELECT * FROM pulso135 WHERE idt=?',(idt,))
    for row in tupla:
        l.append(row[1])
        l.append(row[2])
        l.append(row[3])
        lista.append(l)
        l=[]
    
    return lista



'''Lista com os ids'''
def ids():
    lista_id = []
    tupla=c.execute('SELECT * FROM dadosIniciais  WHERE ensaio= ? ORDER BY id DESC LIMIT 30', ('183',))
    for row in tupla:
        lista_id.append([row[0]])

    return lista_id

'''Junta as informações para visualização em uma lista'''
def juncaoLista():
    a = data_identificadores()
    b = dataInicial()
    c = datafinal()

    d = []
    cont = 0
    id = len(a) - 1
    e = ['']
    f = ['']

    while cont <= id:
        try:
            d.append([[a[cont]] + b[cont] + c[cont]])
            cont = cont +1
        except IndexError:
            d.append([[a[cont]] + e + f])
            cont = cont +1

    return d

'''Captura as datas iniciais dos ensaios para criar uma lista para visualização'''
def dataInicial():
    list_dateincial = []
    tupla=c.execute('SELECT * FROM dadosIniciais  WHERE ensaio= ? ORDER BY id DESC LIMIT 30', ('183',))
    for row in tupla:
        list_dateincial.append([row[12]])

    return list_dateincial

'''Captura as datas finais dos ensaios para criar uma lista para visualização'''
def datafinal():
    list_datefinal = []
    tupla=c.execute('SELECT * FROM dadosIniciais  WHERE ensaio= ? ORDER BY id DESC LIMIT 30', ('183',))
    for row in tupla:
        list_datefinal.append([row[13]])

    return list_datefinal

'''Captura as identificacoes'''
def data_identificadores():
    list_id = []
    tupla=c.execute('SELECT * FROM dadosIniciais  WHERE ensaio= ? ORDER BY id DESC LIMIT 30', ('183',))
    for row in tupla:
        list_id.append(row[3])

    return list_id

'''Cria uma Lista Index de visualização e indentificação'''
def ListaVisualizacao():
    a = ids()
    b = juncaoLista()
    cont = 0
    id = len(a) - 1
    c = []
    while cont <= id:
        c.append(a[cont] + b[cont])
        cont = cont +1

    return c #retorna a lista c de mado invertido

'''Deleta o ensaio no banco de dados'''
def delete(idt):
    c.execute("DELETE FROM dadosIniciais WHERE identificacao = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT134ADM WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT134 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT179 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT181 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT183 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT135 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM referenciaADM WHERE idt = ?", (idt,))
    c.execute("DELETE FROM referencia WHERE idt = ?", (idt,))
    c.execute("DELETE FROM pulso135 WHERE idt = ?", (idt,))
    connection.commit()

'''pega a altura do CP de acordo com a identificação'''
def altura_cp(idt):
    tupla=c.execute('SELECT * FROM dadosIniciais WHERE identificacao = ?', (idt,))
    for row in tupla:
        altura = row[16]
    return altura

######################################################################################
################################## CALIBRAÇÕES #######################################
######################################################################################
'''Atualiza os dados I, A e B de Calibração dos sensores S1 e S2'''
def update_dados_S1S2(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE s1s2 SET I0 = ?, A0 = ?, B0 = ?, C0 = ?, I1 = ?, A1= ?, B1 = ?, C1 = ? WHERE id = ?", (i0,a0,b0,c0,i1,a1,b1,c1, id,))
    connection.commit()

'''Atualiza os dados I, A e B de Calibração dos sensores S3 e S4'''
def update_dados_S3S4(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE s3s4 SET I0 = ?, A0 = ?, B0 = ?, C0 = ?, I1 = ?, A1= ?, B1 = ?, C1 = ? WHERE id = ?", (i0,a0,b0,c0,i1,a1,b1,c1, id,))
    connection.commit()

######################################################################################
###################################  DNIT 134  #######################################
######################################################################################
'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_134_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    x=[]
    y=[]
    list  = [['FASE', 'Tensão\nconfinante\nσ3\n[MPa]', 'Tensão\ndesvio\nσd\n[MPa]', 'Deslocamento\nrecuperável\nδ\n[mm]', 'Deformação\nresiliente\nε\n[%]', 'Módulo de\nResiliência\nMR\n[MPa]']]
    tupla=c.execute('SELECT * FROM dadosDNIT134 WHERE idt = ?', (idt,))
    for row in tupla:
        l.append(row[1]) #Fase
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #TC
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #TD
        l.append(format("%.3f" % float(row[4])).replace('.',',')) #Desl. R.
        # x.append(float(row[3]))
        # y.append (float(row[3])/(float(row[4])/float(row[5])))
        acumulado = acumulado + float(row[5])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[4])/float(row[5])))).replace('.',',')) #DEF.R
        l.append(format(str("%.3f" % (float(row[3])/(float(row[4])/float(row[5]))))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []
    

    return list

def untrated183(idt):
    l =[]
    tupla=c.execute('SELECT * FROM dadosDNIT183 WHERE idt = ?', (idt,))
    for row in tupla:
        l.append(row[1])
        l.append(round(row[4]/row[8],7))
        l.append(str(float(row[3])*100)+'%')
        l.append(round(row[4],3))
        l.append(row[5])
        l.append(row[6])
        l.append(row[7])
        l.append(round(row[4]*6.1752*1000,3))
        l.append(round((row[4]*6.1752*1000*2)/(math.pi*row[6]*0.001*row[7]),3))
    
    return l


def dados_da_coleta_183_pdf(idt):
    l =[]
    list  = [['N° Corpo de \nProva', 'Deformação\nEspecifica \nResiliente [mm]', 'Nivel de\nTensão\n %', 'Pressão\nManometrica\n[mPa]', 'N° de \nGolpes','Diametro\n[mm]', ' Altura\n[mm]' ,'Carga\nAplicada\n[N]','Tensão \nde Tração\n[kPa]']]
    tupla=c.execute('SELECT * FROM dadosDNIT183 WHERE idt = ?', (idt,))
    for row in tupla:
        l.append(row[1])
        l.append(round(row[4]/row[8],7))
        l.append(str(float(row[3])*100)+'%')
        l.append(round(row[4],3))
        l.append(row[5])
        l.append(row[6])
        l.append(row[7])
        l.append(round(row[4]*6.1752*1000,3))
        l.append(round((row[4]*6.1752*1000*2)/(math.pi*row[6]*0.001*row[7]),3))
        # l.append(round(row[4]*0.0127*row[7]*0.001*1000000*2/3.14*row[7]*row[6]*0.001*0.001,3))
        list.append(l)
        l = []
    
    return list

def dados_da_coleta_135_pdf(idt):
    l=[]
    list = [['Fase','Espessura [mm]','Diametro [mm]','Carga\nAplicada \n[Kgf]','Modulo de \nResiliencia\n[MPa]','Modulo\nInstantaneo\n[MPa]','Modulo\nTotal\n[MPa]']]
    tupla=c.execute('SELECT * FROM dadosDNIT135 WHERE idt = ?', (idt,))
    for row in tupla:
        l.append(row[1])
        l.append(row[4])
        l.append(row[5])
        l.append(round(row[2]*0.05*0.05*3.141516*1000000/9.80665,3))
        l.append(round(row[3],3))
        l.append(round(row[6],3))
        l.append(round(row[7],3))
        list.append(l)
        l=[]
    
    return list


def pontos135(fase,timestamp,deslocamento):
    c.execute('INSERT INTO dadoscurva135 (fase,timestamp, deslocamento) VALUES (?, ?, ?)', (fase,timestamp,deslocamento))
    connection.commit()

def getpontos135(fase):
    lista=[]
    l=[]
    tupla=c.execute('SELECT * FROM dadoscurva135 WHERE fase = ?', (fase,))
    for row in tupla:
        l.append(row[1])
        l.append(row[2])
        lista.append(l)
        l=[]
    
    return lista



# Verifica qual ensaio está sendo realizado
def tipo_ensaio(idt):
     return c.execute('SELECT ensaio FROM dadosiniciais WHERE idt = ?',(idt,))   

def dados_iniciais_183(ensaio):
    lista=[]
    tupla=c.execute('SELECT * FROM dadosiniciais WHERE ensaio = ?',(ensaio,))
    for row in tupla:
        lista.append(row[3])
    return lista[::-1]

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_134(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['FASE', 'TC[MPa]', 'TD[MPa]', 'Desl. R. [mm]', 'DEF. R [%]', 'MOD. R. [MPa]']]
    tupla=c.execute('SELECT * FROM dadosDNIT134 WHERE idt = ?', (idt,))
    for row in tupla:
        l.append(row[1]) #Fase
        l.append(format(row[2]).replace('.',',')) #TC
        l.append(format(row[3]).replace('.',',')) #TD
        l.append(format(row[4]).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[5])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[4])/alturaRF)).replace('.',',')) #DEF.R
        l.append(format(str(float(row[3])/(float(row[4])/alturaRF))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Atualiza os dados iniciais do ensaio 134'''
def update_dados_134(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET tipo = ? ,naturazaDaAmostra = ?, teorUmidade = ?, pesoEspecifico = ?, umidadeOtima = ?, energiaCompactacao = ?, grauCompactacao = ?, dataColeta = ?, amostra = ?, diametro = ?, altura = ?, obs = ?, tecnico = ?, formacao = ? WHERE identificacao = ?", (tipo, naturazaDaAmostra,teorUmidade,pesoEspecifico,umidadeOtima,energiaCompactacao,grauCompactacao,dataColeta,amostra,diametro,altura,obs,tecnico,formacao, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 134'''
def data_save_dados_134(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '134'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()

def saveDNIT134(idt, fase, pc, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT134 (idt, fase, pc, pg, dr, r) VALUES (?, ?, ?, ?, ?, ?)", (idt, fase, pc, pg, dr, r))
    connection.commit()

def saveDNIT135(idt, fase, pg ,dh, espess,diametro,mediaMI,mediaMT):
    c.execute("INSERT INTO dadosDNIT135 (idt, fase, pg, mr, espessura,diametro,moduloInstantaneo,moduloTotal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (idt, fase, pg, dh, espess,diametro,mediaMI,mediaMT))
    connection.commit()

def saveReferencia(idt, fase, r):
    c.execute("INSERT INTO referencia (idt, fase, r) VALUES (?, ?, ?)", (idt, fase, r))
    connection.commit()

def saveDNIT134ADM(idt, fase, x, y1, yt1, y2, yt2, pc, pg):
    c.execute("INSERT INTO dadosDNIT134ADM (idt, fase, x, y1, yt1, y2, yt2, pc, pg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (idt, fase, x, y1, yt1, y2, yt2, pc, pg))
    connection.commit()

def saveReferenciaADM(idt, fase, r1, r2):
    c.execute("INSERT INTO referenciaADM (idt, fase, r1, r2) VALUES (?, ?, ?, ?)", (idt, fase, r1, r2))
    connection.commit()

def tipo_ensaio(idt):
    ensaio=[]
    tupla=c.execute('SELECT * FROM dadosiniciais WHERE identificacao = ?',(idt,))
    for row in tupla:
        ensaio.append(row[1])
        ensaio.append(row[2])
        ensaio.append(row[3])
        ensaio.append(row[4])
        ensaio.append(row[5])
        ensaio.append(row[6])
        ensaio.append(row[7])
        ensaio.append(row[8])
        ensaio.append(row[9])
        ensaio.append(row[10])
        ensaio.append(row[11])
        ensaio.append(row[12])
        ensaio.append(row[13])
        ensaio.append(row[14])
        ensaio.append(row[15])
        ensaio.append(row[16])
        ensaio.append(row[17])
        ensaio.append(row[18])
        ensaio.append(row[19])
        ensaio.append(row[20])
        ensaio.append(row[21])
        ensaio.append(row[22])
        ensaio.append(row[23])
        ensaio.append(row[24])
        ensaio.append(row[25])
        ensaio.append(row[26])
        ensaio.append(row[27])
        ensaio.append(row[28])
        ensaio.append(row[29])
    return ensaio

######################################################################################
###################################  DNIT 135  #######################################
######################################################################################
'''Funções referente a 135 aqui...'''
def data_save_dados_135(identificacao,natureza_amostra, tecnico,formacao, resistencia_tracao, dataColeta, diametro, altura, obs,tensao):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '135'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    tipo='0'
    teorUmidade=''
    pesoEspecifico=''
    umidadeOtima=''
    energiaCompactacao=''
    grauCompactacao=''
    amostra=''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao, resistenciaTracao,tensao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (ensaio, status, identificacao, tipo, natureza_amostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao, resistencia_tracao,tensao))
    connection.commit()

def update_dados_135(identificacao,natureza_amostra, tecnico,formacao, resistencia_tracao, dataColeta, diametro, altura, obs,tensao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ?, tecnico = ?, formacao = ?, resistenciaTracao = ?, tensao = ?, dataColeta = ?, diametro = ?, altura = ?, obs = ? WHERE identificacao = ?", (natureza_amostra,tecnico,formacao,resistencia_tracao,tensao,dataColeta,diametro,altura,obs, identificacao,))
    connection.commit()

def update_dados_183(identificacao,natureza_amostra, tecnico,formacao, resistencia_tracao, dataColeta, diametro, altura, obs,tensao,sequencia,mr):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ?, tecnico = ?, formacao = ?, resistenciaTracao = ?, tensao = ?, dataColeta = ?, diametro = ?, altura = ?, obs = ?, sequencia = ?, mr = ? WHERE identificacao = ?", (natureza_amostra,tecnico,formacao,resistencia_tracao,tensao,dataColeta,diametro,altura,obs,sequencia,mr, identificacao,))
    connection.commit()

def data_save_dados_183(identificacao,natureza_amostra, tecnico,formacao, resistencia_tracao, dataColeta, diametro, altura, obs,tensao,sequencia,mr):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '183'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    tipo='0'
    teorUmidade=''
    pesoEspecifico=''
    umidadeOtima=''
    energiaCompactacao=''
    grauCompactacao=''
    amostra=''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao, resistenciaTracao, tensao, sequencia,mr) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (ensaio, status, identificacao, tipo, natureza_amostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao, resistencia_tracao, tensao, sequencia,mr))
    connection.commit()

######################################################################################
###################################  DNIT 179  #######################################
######################################################################################
'''Cria Lista com a Coleta para criar grafico local'''
def dados_GDP_179(idt):
    x = []
    y = []
    tupla=c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,))
    for row in tupla:
        x.append(int(row[1])) #golpe
        y.append(float(row[3])) #Desl. Permanente.
        
    return x, y

'''Cria Lista com a Coleta dos resultados do ensaio no banco de dados'''
def dados_da_coleta_179_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    tupla=c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,))
    list  = [['Número\nde ciclos\nN', 'Deslocamanto plástico\nou permanente\nacumulado\nδp\n[mm]', 'Deslocamanto\nelástico ou\nrecuperável\nδ\n[mm]', 'Deformação\nplástica ou\npermanente\nεp\n[%]', 'Deformação\nresiliente ou\nelástica\nε\n[%]']]
    for row in tupla:
        l.append(row[1]) #CICLO
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #Desl. Permanente.
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #Desl. R.
        acumulado = float(row[3])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[3])/alturaRF))).replace('.',',')) #DEF. Permanente.
        l.append(format(str("%.3f" % (100*float(row[2])/alturaRF))).replace('.',',')) #DEF. R.
        list.append(l)
        l = []

    return list

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_179(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    tupla=c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,))
    list  = [['N', 'Desl. P. [mm]', 'Desl. R. [mm]', 'DEF. P. [%]', 'DEF. R. [%]']]
    for row in tupla:
        l.append(row[1]) #CICLOS
        l.append(format(row[3]).replace('.',',')) #Desl. Permanente.
        l.append(format(row[2]).replace('.',',')) #Desl. R.
        acumulado = float(row[3])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[3])/alturaRF)).replace('.',',')) #DEF.Permanente.
        l.append(format(str(100*float(row[2])/alturaRF)).replace('.',',')) #DEF.R.
        list.append(l)
        l = []

    return list

'''Atualiza os dados iniciais do ensaio 179'''
def update_dados_179(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    pressaoConf = bdConfiguration.QD_179_MOD()[1][tipo][0]
    pressaoDesvio = bdConfiguration.QD_179_MOD()[1][tipo][1] - pressaoConf
    c.execute("UPDATE dadosIniciais SET tipo = ? ,naturazaDaAmostra = ?, teorUmidade = ?, pesoEspecifico = ?, umidadeOtima = ?, energiaCompactacao = ?, grauCompactacao = ?, dataColeta = ?, amostra = ?, diametro = ?, altura = ?, obs = ?, tecnico = ?, formacao = ?, pressaoConf = ?, pressaoDesvio = ? WHERE identificacao = ?", (tipo, naturazaDaAmostra,teorUmidade,pesoEspecifico,umidadeOtima,energiaCompactacao,grauCompactacao,dataColeta,amostra,diametro,altura,obs,tecnico,formacao,pressaoConf,pressaoDesvio, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 179'''
def data_save_dados_179(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '179'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = bdConfiguration.QD_179_MOD()[1][tipo][0]
    pressaoDesvio = bdConfiguration.QD_179_MOD()[1][tipo][1] - pressaoConf
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()

def saveDNIT179(idt, glp, DR, DP, pc, pg, ref):
    c.execute("INSERT INTO dadosDNIT179 (idt, glp, DR, DP, pc, pg, ref) VALUES (?, ?, ?, ?, ?, ?, ?)", (idt, glp, DR, DP, pc, pg, ref))
    connection.commit()

######################################################################################
###################################  DNIT 181 ########################################
######################################################################################
'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_181_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    tupla=c.execute('SELECT * FROM dadosDNIT181 WHERE idt = ?', (idt,))
    list  = [['FASE', 'Tesão\nvertical\nσd\n[MPa]', 'Deslocamento\nrecuperável\nδ\n[mm]', 'Deformação\nresiliente\nε\n[%]', 'Módulo de\nResiliência\nMR\n[MPa]']]
    for row in tupla:
        l.append(row[1]) #Fase
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #TV
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[4])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[3])/alturaRF))).replace('.',',')) #DEF.R
        l.append(format(str("%.3f" % (float(row[2])/(float(row[3])/alturaRF)))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_181(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    tupla=c.execute('SELECT * FROM dadosDNIT181 WHERE idt = ?', (idt,))
    list  = [['FASE', 'Tensao V. [MPa]', 'Desl. R. [mm]', 'DEF. R. [%]', 'MOD. R. [MPa]']]
    for row in tupla:
        l.append(row[1]) #Fase
        l.append(format(row[2]).replace('.',',')) #TV
        l.append(format(row[3]).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[4])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[3])/alturaRF)).replace('.',',')) #DEF.R
        l.append(format(str(float(row[2])/(float(row[3])/alturaRF))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Salva os dados do ensaio 181'''
def saveDNIT181(idt, fase, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT181 (idt, fase, pg, dr, r) VALUES (?, ?, ?, ?, ?)", (idt, fase, pg, dr, r))
    connection.commit()

'''Atualiza os dados iniciais do ensaio 181'''
def update_dados_181(identificacao, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, diametro, altura, obs, tecnico, formacao, tipoEstabilizante, tempoCura, pesoEstabilizante):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ?, teorUmidade = ?, pesoEspecifico = ?, umidadeOtima = ?, energiaCompactacao = ?, grauCompactacao = ?, dataColeta = ?, diametro = ?, altura = ?, obs = ?, tecnico = ?, formacao = ?, tipoEstabilizante = ?, pesoEstabilizante = ?, tempoCura = ? WHERE identificacao = ?", (naturazaDaAmostra,teorUmidade,pesoEspecifico,umidadeOtima,energiaCompactacao,grauCompactacao,dataColeta,diametro,altura,obs,tecnico,formacao,tipoEstabilizante,pesoEstabilizante,tempoCura, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 181'''
def data_save_dados_181(identificacao, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, diametro, altura, obs, tecnico, formacao, tipoEstabilizante, tempoCura, pesoEstabilizante):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '181'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    amostra = 0
    tipo = 0
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()
