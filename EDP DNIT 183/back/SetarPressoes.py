# -*- coding: utf-8 -*-
import time
import banco.bdConfiguration as bdConfiguration
import back.connection as con
import math

class SetarPressaoGolpe():

    def __init__(self,pressGolpe,PressaoAtual,diametro):
        self.pressGolpe=pressGolpe
        self.diametro=diametro
        self.p1Ant=PressaoAtual
        self.run()

    def run(self):
        E = bdConfiguration.DadosD1()
        F= bdConfiguration.dados_d3()

        pi = math.pi
        A2 = (self.diametro*self.diametro)*(pi/4)



        AE2=float(F[0])
        BE2=float(F[1])             #fator de correçao para a pressão na prensa de asfalto
        pressao1 = (self.pressGolpe)*AE2+BE2
        pressao1Ant = (self.p1Ant)*AE2+BE2

        time.sleep(.5)
        con.modeE() #envia para o arduino o codigo para alterar a pressão
        time.sleep(.5)
        valor1 = con.modeDIN(pressao1, pressao1Ant) #envia para o arduino o valor de pressão do golpe de modo incremental
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE OK')
            time.sleep(1)


class ZerarPressaoGolpe():

    def __init__(self, p1Sen):
        self.p1Sen = p1Sen
        self.run()

    def run(self):
        E = bdConfiguration.DadosD1()
        F= bdConfiguration.dados_d3()
   
        AE2=float(F[0])
        BE2=float(F[1])
        pressao1 = 0
        pressao1Sen = (self.p1Sen)*AE2+BE2

        time.sleep(5)
        con.modeES()
        time.sleep(0.5)
        valor1 = con.modeDINZERO(0, pressao1Sen )
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE ZERADO')
            time.sleep(1)
            

