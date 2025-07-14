# -*- coding: utf-8 -*-
import wx
import time
import back.connection as con
import back.SetarPressoes as SetarPressoes
from pubsub import publish
import numpy as np
from threading import Thread
import banco.bancodedados as bancodedados
from scipy.signal import savgol_filter

class LeituraDados(Thread):
    #-------------------------------------------------------------------
    def __init__(self,_self,valorLeitura0,ValorLeitura1):
        Thread.__init__(self)
        self._self=_self
        self.leituraZerob1=valorLeitura0
        self.leituraZerob2=ValorLeitura1
        self.converg_135=True
        self._pause=False
        self._ensaio=False
        self._stop_event = True
        self._Fase=""
        self._golpeAnterior=-1
        self._inicio=False
        self.yyy=[]
        self.pc1=[]
        self.pg1=[]
        self.copia=[]
        self.copia135=np.array([])
        self.copiaX=[]
        self.copiaXTratado=[]
        self.Tmax=0
        self.T1=0
        self.T2=0
        self.Tc=0
        self.Tf=0
        self.Ttg=0
        self.REFERENCIA_MEDIA=0
        self.mediaMovel=0
        self.sensor1=[]
        self.sensor2=[]
        self.lvdt1=[]
        self.lvdt2=[]
        self.tstamp=[]
        self.gAtual=[]
        self.gTot=[]
        self.vetorMR=[]
        self.vetorMI=[]
        self.vetorMT=[]
        self.avancaCond=False
        self.avancaMr=False
        self.temposDNIT179_01 = [1,2,3,4,5,10,15,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900]
        self.temposDNIT179_02 = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000,
                                19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,
                                35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48000,49000,50000,
                                55000,60000,65000,70000,75000,80000,85000,90000,95000,100000,110000,120000,130000,140000,150000,
                                160000,170000,180000,190000,200000,210000,220000,230000,240000,250000,260000,270000,280000,290000,
                                300000,310000,320000,330000,340000,350000,360000,370000,380000,390000,400000,410000,420000,430000,
                                440000,450000,460000,470000,480000,490000,500000]
        self.golpe = []
        self.vDR = []
        self.vDP = []
        self.ppc = []
        self.ppg = []
        self.larguraPulsoX=[]
        self.larguraPulsoY=[]
        self.maximoRT=[]
        self.minimoRT=[]

    def run(self):
        
        GolpeAnterior = -1
        x_counter = 0
        self.valoresEnsaio = [0,0,0,0,0,0,0,0,0,0]
        while self._stop_event:
            self.atualizarDadosTela()
            self.atualizarDadosTelaEnsaio()
                         

    #-------------------------------------------------------------------
    def stop(self):
        self._stop_event=False

    def updateValor(self,valorLeitura0,ValorLeitura1):
        self.leituraZerob1=valorLeitura0
        self.leituraZerob2=ValorLeitura1

    def pause(self):
        self._pause=not self._pause

    def inicioEnsaio(self):
        self._inicio= not self._inicio

    def  setEnsaio(self):
        self._ensaio=not self._ensaio

    def setAvancaCond(self):
        self.avancaCond=True
    
    def setAvancaMR(self):
        self.avancaMr=True

    def atualizarDadosTela(self):
        cont1 = 0
        self.valoresEnsaio = [0,0,0,0,0,0,0,0,0,0]
        while (not self._pause) and (not self._ensaio):
                con.modeJ()
                self.valoresEnsaio = con.ColetaI(self.valoresEnsaio,self._self.ensaio[0])
                if cont1 >= 20: #atualiza os dados na tela a cada 20 iterações
                    self.atributosTela()
                if cont1 == 20:
                    cont1 = 0
                cont1 = cont1 + 1

                self.ntglp = self.valoresEnsaio[9] #numero total de golpes
                self.y1 = self.valoresEnsaio[1]-self.leituraZerob1*0.999
                self.y2=self.y1
                self.ymedio = (self.y1 + self.y2)/2 + 0.0000001 #A média + H0 que é o ponto de referência inicial

    def atributosTela(self):
        self.valorLeitura0 = self.valoresEnsaio[1] #usado apenas no LZERO
        self.valorLeitura1 = self.valoresEnsaio[2] #usado apenas no LZERO
        self._self.y1mm.SetLabelText(str(round(abs(self.valoresEnsaio[1]-self.leituraZerob1), 4)))
        self._self.y1V.SetLabelText(str(round((self.valoresEnsaio[3]), 2)))
        self._self.SigmaReal.SetLabelText(str(round(abs(self.valoresEnsaio[6]), 3)))
        if self.leituraZerob1 == 0:
            self._self.AlturaFinal.SetLabelText(str(round(self._self.diametro, 3)))
        else:
            self._self.AlturaFinal.SetLabelText(str(round(self._self.diametro+abs(self.ymedio), 3)))
    
    def atualizarDadosTelaEnsaio(self):
        cont1=0
        self.amplitudeMaxima=0
        self.amplitudeMinima=0
        self.minimos=[]
        while (not self._pause) and (self._ensaio):
                self.valoresEnsaio = con.ColetaI(self.valoresEnsaio,self._self.ensaio[0])
                if cont1 >= 20: #atualiza os dados na tela a cada 20 iterações
                    self.atributosTela()
                if cont1 == 20:
                    cont1 = 0
                cont1 = cont1 + 1

                self.ntglp = self.valoresEnsaio[9] #numero total de golpes
                self.y1 = self.valoresEnsaio[1]-self.leituraZerob1*0.999
                # print self.y1
                self.y2=self.y1
                self.ymedio = (self.y1 + self.y2)/2 #A média + H0 que é o ponto de referência inicial
                # print self.ymedio
                
                if self._inicio:
                    valorGolpe=self.valoresEnsaio[8]
                    timestamp=self.valoresEnsaio[0]
                    self._self.NGolpes.SetLabelText(str(int(self.valoresEnsaio[9])))

                    
                    
                    if self.valoresEnsaio[0] > 0 : #só atualiza os pontos quando a leitura tiver sucesso
                        self._self.TopPanel.X=np.append(self._self.TopPanel.X, self.valoresEnsaio[0])
                        self._self.TopPanel.Y=np.append(self._self.TopPanel.Y, self.ymedio)
                        self.GolpeAnterior = int(self.valoresEnsaio[8])
                        self.timestamp=self.valoresEnsaio[0]
                        self._self.GolpeAtual.SetLabelText(str(int(self.valoresEnsaio[8])))
                        x_counter = len(self._self.TopPanel.X)
                        if x_counter >= 1000: #mantem o array de pontos com tamanho de 1000
                            self._self.TopPanel.X = np.delete(self._self.TopPanel.X, 0, 0)
                            self._self.TopPanel.Y = np.delete(self._self.TopPanel.Y, 0, 0)
                        if((self.timestamp-int(self.timestamp))==0 and self.timestamp != 0):
                            self._self.TopPanel.Y = savgol_filter(self._self.TopPanel.Y, 51, 6)
                            self.copia=self._self.TopPanel.Y[-200:]
                            self.copiaX=self._self.TopPanel.X[-200:]
                            i=0
                            self.copiaXTratado=[]
                            while i<len(self.copiaX):
                                self.copiaXTratado.append(self.copiaX[i]-int(self.copiaX[i]))
                                i+=1
                            self.copia135=np.array([self.copia])
                            self._self.TimeInterval()
                    
                    
                    self.calculo135()
                    parada=timestamp

                    if (self._self.Fase=="RT" and parada== int(self._self.NGolpes.GetValue())): # determinação da pressão inicial quando a RT é desconhecida
                        self._self.TopPanel.pausa.Disable()
                        self._self.TopPanel.fim_inicio.Disable()
                        self._self.TopPanel.avanca.Disable()
                        self._self.TopPanel.X = np.array([])
                        self._self.TopPanel.Y = np.array([])
                        self._self.mult = 0
                        self._self.TopPanel.draww()
                        self.valorGolpe=0
                        self._ensaio=False
                        self._inicio=False
                        self.timestamp=0
                        print ((sum(self.maximoRT)/len(self.maximoRT))-(sum(self.minimoRT)/len(self.minimoRT)))
                        if ((sum(self.maximoRT)/len(self.maximoRT))-(sum(self.minimoRT)/len(self.minimoRT)))<0.007:
                            self.maximoRT=[]
                            self.minimoRT=[]
                            self._self.resistencia=self._self.resistencia+0.025
                            evt=wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self._self.condic.GetId())
                            wx.PostEvent(self._self.condic,evt)
                        else:
                            self._self.Bind(wx.EVT_BUTTON, self._self.CONDIC, self._self.condic)
                            self._self.condic.Enable()
                            self._self.mr.Enable()

                    
                    
                    if (self._self.Fase=="CONDICIONAMENTO" and parada== int(self._self.NGolpes.GetValue())) or self.avancaCond: # condição para o fim do condicionamento=                        
                        time.sleep(1)
                        self.avancaCond=False
                        self._self.TopPanel.pausa.Disable()
                        self._self.TopPanel.fim_inicio.Disable()
                        self._self.TopPanel.avanca.Disable()
                        self._self.TopPanel.X = np.array([])
                        self._self.TopPanel.Y = np.array([])
                        self._self.mult = 0
                        self._self.TopPanel.draww()
                        self.valorGolpe=0
                        self._ensaio=False
                        self._inicio=False
                        self.timestamp=0
                        self._self._fase+=1
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.mr.GetId())
                        wx.PostEvent(self._self.mr, evt)

                        
                       
                    elif ((self._self.Fase=="MR" ) and parada== int(self.valoresEnsaio[9]))or self.avancaMr: # condição para o fim do condicionamento
                        time.sleep(1)
                        self.avancaMr=False
                        # bancodedados.teste_press(self._self.Nome,self._self._fase,self.sensor1,self.sensor2,self.lvdt1,self.lvdt2,self.tstamp,self.gAtual,self.gTot)
                        self._self.TopPanel.pausa.Disable()
                        self._self._fase+=1
                        self._self.TopPanel.avanca.Disable()
                        self._self.mult = 0
                        self._self.TopPanel.draww()
                        self.valorGolpe=0
                        self._ensaio=False
                        self._inicio=False
                        self.timestamp=0

                        pg = sum(self.pg1)/len(self.pg1)
                        self.pg1=[]
                        # dh = sum(self.yyy)/len(self.yyy)
                        mediamr=0
                        mediaMI=0
                        mediaMT=0
                        self.vetorMI = [x for x in self.vetorMI if x != float('inf') and x != float('-inf')]
                        i=-1
                        try:
                            if self.converg_135:
                                while i >= -5:
                                    mediamr=mediamr+self.vetorMR[i]
                                    i=i-1
                                mediamr=mediamr/5
                            else:
                                conv={}
                                listconv=0
                                cont_conv=0
                                mediatotal=sum(self.vetorMR)/len(self.vetorMR)
                                for valor in self.vetorMR:
                                    if abs(((mediatotal-valor)/mediatotal)*100)<5:
                                        conv[abs(((mediatotal-valor)/mediatotal)*100)]=valor
                                conv=dict(sorted(conv.items()))
                                print(conv)
                                for chave,value in conv.items():
                                    listconv+=value
                                    cont_conv+=1
                                    if cont_conv==5:
                                        break
                                mediamr=listconv/5
                            mediaMI=sum(self.vetorMI)/len(self.vetorMI)
                            mediaMT=sum(self.vetorMT)/len(self.vetorMT)
                        except Exception as e:
                            print("Exceção:", type(e).__name__)

                        bancodedados.saveDNIT135(self._self.Nome,self._self._fase-1,pg,mediamr,self._self.ensaio[15],self._self.AlturaFinal.GetValue(),mediaMI,mediaMT)
                        # SetarPressoes.ZerarPressaoGolpe(self._self.resistencia*self._self.TopPanel.PRESSOES[self._self._fase])
                        for item1,item2 in zip(self._self.TopPanel.X,self._self.TopPanel.Y):
                            bancodedados.pulso135(self._self.Nome,self._self._fase-1,item1,item2)
                        self._self.TopPanel.X=[]
                        self._self.TopPanel.Y=[]
                        self.vetorMR=[]
                        self.vetorMI=[]
                        self.vetorMT=[]
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.mr.GetId())
                        wx.PostEvent(self._self.mr, evt)
    
    
    def calculo135(self):
        if self._self.Fase == 'MR' and self._self.ensaio[0]=='135':
            if self.valoresEnsaio[0] > 1:
                self.pg1.append(self.valoresEnsaio[6]) #pressão de desvio
                # bancodedados.pontos135(self._self._fase,self.valoresEnsaio[0],self.ymedio)
                valoreS = self.valoresEnsaio[0] - int(self.valoresEnsaio[0])
                if valoreS==0:
                    try:
                        self.amplitudeMaxima=max(self.copia)
                        print ("pressão atual do golpe: "+ str(self.valoresEnsaio[6]))
                        self.Tmax=np.argmax(self.copia135)
                        self.T1=self.copia[self.Tmax+1]
                        self.T2=self.copia[self.Tmax+11]
                        self.Tc=self.copia[92]
                        self.Ttg=self.copia[119]
                        self.Tf=self.copia[182]
                        m=(self.T2-self.amplitudeMaxima)/(self.copiaXTratado[self.Tmax+11]-self.copiaXTratado[self.Tmax])
                        # print "Coeficiente angular: "+str(m) # pegar os respectivos valores dos pontos tmax e t2 no vetor de pontos x
                        n=self.copia[self.Tmax]-m*self.copiaXTratado[self.Tmax]
                        # print "coeficiente linear: "+str(n)
                        # print self.T2,self.amplitudeMaxima,self.copiaXTratado[self.Tmax+11],self.copiaXTratado[self.Tmax]

                        # print self.Ttg,self.Tc,self.copiaXTratado[119],self.copiaXTratado[92]

                        m2=(self.Ttg-self.Tc)/(self.copiaXTratado[119]-self.copiaXTratado[92])
                        # print "Coeficiente angular: "+str(m2)
                        n2=self.Tc-m2*self.copiaXTratado[92]
                        # print "coeficiente linear: "+str(n2)

                        coeficientes = np.array([[m, 1], [m2, 1]])
                        constantes = np.array([n, n2])
                        ponto_intersecao = np.linalg.solve(coeficientes, constantes)
                        pressao_media=sum(self.pg1)/len(self.pg1)
                        # Exibir o ponto de interseção
                        x_intersecao, y_intersecao = ponto_intersecao
                        # print "interseção em X: "+str(x_intersecao*(-1))
                        x_intersecao=int(x_intersecao*(-100)*2)
                        # print "local no vetor "+ str(self.copiaXTratado[x_intersecao])
                        minimo=self.copia[x_intersecao]
                        modulo_instantaneo=(pressao_media*1000000*3.141516*0.05*0.05*2/((abs(self.amplitudeMaxima-minimo))*self._self.altura))*(0.27+0.3)
                        print ("Modulo de Instantaneo: "+str(modulo_instantaneo))
                        self.vetorMI.append(modulo_instantaneo)
                        self._self.textoMI.SetLabelText(str(round(modulo_instantaneo,1)))

                        mr=(pressao_media*1000000*3.141516*0.05*0.05*2/(abs((self.amplitudeMaxima-y_intersecao))*self._self.altura))*(0.2692 + 0.9976*0.3)
                        print ("Modulo de Resiliencia: "+str(mr))
                        self._self.PCreal.SetLabelText(str(round(mr,2)))

                        self.amplitudeMinima=min(self.copia)
                        Tmin=np.argmin(self.copia135)

                        modulo_total=(pressao_media*1000000*3.141516*0.05*0.05*2/((abs(self.amplitudeMaxima-self.amplitudeMinima))*self._self.altura))*(0.27+0.3)
                        print ("Modulo de Total: "+str(modulo_total))
                        self._self.PCalvo.SetLabelText(str(round(modulo_total,1)))
                        self.vetorMT.append(modulo_total)
                        
                        verif=True
                        self.vetorMR.append(mr)
                        mediaMR=sum(self.vetorMR)/len(self.vetorMR)
                        print (self._self.GolpeAtual.GetValue())
                        if self.valoresEnsaio[8]>=15:
                            if len(self.vetorMR)>=5:
                                i=-1
                                while i >= -5:
                                    print ("discrepancia: "+ str(round( abs(((mediaMR-self.vetorMR[i])/mediaMR)*100),3))+"%")
                                    if abs(((mediaMR-self.vetorMR[i])/mediaMR)*100)>8:
                                        verif=True
                                        break
                                    else:
                                        verif=False
                                    i=i-1  
                                if verif==False or self.valoresEnsaio[8]>=200:
                                    self.avancaMr=True
                                    self.converg_135=False
                                    con.modeFIM()
                                else:
                                    self.converg_135=True
                    except Exception as e:
                        print("Exceção:", type(e).__name__)
                        print ("erro ao calcular os modulos")

        elif self._self.Fase == 'RT' and self._self.ensaio[0]=='135':
            if self.valoresEnsaio[0] > 1:
                valoreS = self.valoresEnsaio[0] - int(self.valoresEnsaio[0])
                if valoreS==0:
                    self.maximoRT.append(max(self.copia))
                    self.minimoRT.append(min(self.copia)) 

                        
                    


        
                



           
        


    
    