# -*- coding: utf-8 -*-

import wx
import time
import numpy as np
import banco.bancodedados as bancodedados
import back.connection as con
import matplotlib.pyplot as plt
import back.SetarPressoes as SetarPressoes
import banco.bdPreferences as bdPreferences
from drawnow import *
from front.dialogoDinamico import dialogoDinamico
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas



class TopPanel(wx.Panel):
        PRESSOES=[1,1.05,1.05]
        PressaoAtualGolpe=0
        PressaoAtualCamara=0
        X = np.array([])
        Y = np.array([])
        cond135=0   

        def __init__(self, parent, _self):
            wx.Panel.__init__(self, parent = parent)
            global colorLineGrafic
            
            colors = bdPreferences.ListColors()
            colorCard = colors[0]
            colorTextCtrl = colors[1]
            colorBackground = colors[2]
            colorLineGrafic = colors[3]
            colorBackgroundGrafic = colors[4]
            

            self._self = _self
            self.SetBackgroundColour(colorBackground)
            

            FontTitle = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)

            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.figure = plt.figure(constrained_layout=True,figsize=(8, 3.5))
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(self, -1, self.figure)
            rect = self.figure.patch
            rect.set_facecolor(colorBackgroundGrafic)


            self.avanca = wx.Button(self, -1, 'AVANÇA')
            self.Bind(wx.EVT_BUTTON, self.AVANCA, self.avanca)
            self.pausa = wx.Button(self, -1, 'PAUSA')
            self.Bind(wx.EVT_BUTTON, self.PAUSA, self.pausa)
            self.continua = wx.Button(self, -1, 'CONTINUA')
            self.Bind(wx.EVT_BUTTON, self.CONTINUA, self.continua)
            self.fim_inicio = wx.Button(self, -1, 'INICIO') 
            self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)

            self.avanca.Disable()
            self.pausa.Disable()
            self.continua.Disable()
            self.fim_inicio.Disable()

            self.avanca.SetFont(FontTitle)
            self.pausa.SetFont(FontTitle)
            self.continua.SetFont(FontTitle)
            self.fim_inicio.SetFont(FontTitle)

            self.v_sizer.Add(self.avanca, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.pausa, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.continua, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.fim_inicio, 1, wx.EXPAND | wx.ALL, 5)

            self.h_sizer.Add(self.canvas, 12, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)
            self.h_sizer.AddStretchSpacer(4)

            self.sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)
            self.DINAMICA2_ANTERIOR = 0
            self.DINAMICA1_ANTERIOR = 0
            self.AVANCA = False

    #--------------------------------------------------
        '''Função AVANCA'''
        def AVANCA(self, event):
            print ('\nTopPanel - AVANCA')

            # '''Diálogo se deseja realmente avancar um FASE'''
            dlg = wx.MessageDialog(None, 'Deseja realmente avancar um FASE?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                dlg.Destroy()
                con.modeFIM()
                time.sleep(1)
                self.fim_inicio.SetLabel('INICIO')
                self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                self.pausa.Disable()
                self.avanca.Disable()
                self.continua.Disable()
                self.fim_inicio.Disable()
                if self._self.bottom.Fase=='CONDICIONAMENTO':
                    self._self.bottom.threadLeituraDados.setAvancaCond()
                elif self._self.bottom.Fase=='MR':
                    self._self.bottom.threadLeituraDados.setAvancaMR()
              
                

    #--------------------------------------------------
        '''Função PAUSA'''
        def PAUSA(self, event):
            print ('\nTopPanel - PAUSA')

            con.modeP()
            self._self.bottom.threadLeituraDados.inicioEnsaio()
            self.continua.Enable()
            self.fim_inicio.Enable()
            self.pausa.Disable()
            self.avanca.Disable()

    #--------------------------------------------------
        '''Função CONTINUA'''
        def CONTINUA(self, event):
            print ('\nTopPanel - CONTINUA')

            con.modeC()
            self.pausa.Enable()
            self._self.bottom.threadLeituraDados.inicioEnsaio()
            self.fim_inicio.Enable()
            self.continua.Disable()
            self.avanca.Enable()

    #--------------------------------------------------
        '''Função INICIO'''
        def INICIO(self, event):
            print ('\nTopPanel - INICIO')
            self._self.Raise()
            self._self.RequestUserAttention()
            self.fim_inicio.Disable()
            self._fase = self._self.bottom._fase
            self._self.bottom.threadLeituraDados.pause()
            dialog = wx.ProgressDialog("Aguarde", "Aguarde, calibrando pressões", maximum=100)
            if self._self.bottom.Fase == 'CONDICIONAMENTO':
                time.sleep(.5)
                dialog.Update(33)
                if not self._self.bottom.condRT:
                    press=SetarPressoes.SetarPressaoGolpe(self._self.bottom.resistencia*float(self._self.bottom.ensaio[26]),0,float(self._self.bottom.DiametroMM.GetValue()))
                    self.PressaoAtualGolpe=self._self.bottom.resistencia*float(self._self.bottom.ensaio[26])
                time.sleep(0.5)
                dialog.Update(66)

            elif self._self.bottom.Fase == 'MR': 
                if self._fase > 0 and self._fase <=3 :
                    time.sleep(.5)
                    dialog.Update(33)
                    if(self.PressaoAtualGolpe!=self.PressaoAtualGolpe*self.PRESSOES[self._fase-1] or self._self.bottom.onlyMR):
                        press=SetarPressoes.SetarPressaoGolpe(self.PressaoAtualGolpe*self.PRESSOES[self._fase-1],self.PressaoAtualGolpe,float(self._self.bottom.DiametroMM.GetValue()))        
                        self.PressaoAtualGolpe=self.PressaoAtualGolpe*self.PRESSOES[self._fase-1]
                        self._self.bottom.onlyMR=False
                    time.sleep(0.5)
                    dialog.Update(66)
                else:
                    time.sleep(.5)
                    press=SetarPressoes.SetarPressaoGolpe(self._self.bottom.resistencia*self.PRESSOES[self._fase],float(self._self.bottom.DiametroMM.GetValue()))
                
                if self._self.bottom.Automatico == False:
                    condition = True
                    dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "MÓDULO DE RESILIÊNCIA", "Tudo pronto!", "Aperte INICIO.", "", None)
                    dlg3.ShowModal()
                    time.sleep(1)

            dialog.Update(100)
            dialog.Close()
            self._self.Raise()
            self._self.Maximize()
            # self._self.SetCursor()
            gl = self._self.bottom.NGolpes.GetValue()
            freq = self._self.bottom.freq.GetValue()
            if self._self.bottom.Automatico==False:
                info = "EDP 135/2018ME"
                titulo = "Preparação do ensaio."
                message1 = "Verifique se está tudo certo!"
                message2 = "Verifique se o CP esta posicionado corretamente, e se os sensores estão configurados."
                dlg = dialogoDinamico(5, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    con.modeG()
                    time.sleep(0.5)
                    con.modeGOLPES135(int(gl), int(freq),self.cond135)
                    self.pausa.Enable()
                    self.avanca.Enable()
                    self.fim_inicio.SetLabel('FIM')
                    self.fim_inicio.Enable()
                    self.Bind(wx.EVT_BUTTON, self.FIM, self.fim_inicio)
                    self._self.bottom.threadLeituraDados.inicioEnsaio()
                    self._self.bottom.threadLeituraDados.setEnsaio()
                    self._self.bottom.threadLeituraDados.pause()
                    self._self.Raise()
                    self._self.RequestUserAttention()
                elif dlg.ShowModal()== wx.ID_ABORT:
                    self.Bind(wx.EVT_BUTTON, self.FIM, self.fim_inicio)
                    evt=wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.fim_inicio.GetId())
                    wx.PostEvent(self.fim_inicio,evt)
            else:
                con.modeG()
                time.sleep(0.5)                
                con.modeGOLPES135(int(gl), int(freq),self.cond135)
                self.pausa.Enable()
                self.avanca.Enable()
                self.fim_inicio.SetLabel('FIM')
                self.fim_inicio.Enable()
                self.Bind(wx.EVT_BUTTON, self.FIM, self.fim_inicio)
                self._self.bottom.threadLeituraDados.inicioEnsaio()
                self._self.bottom.threadLeituraDados.setEnsaio()
                self._self.bottom.threadLeituraDados.pause()
                self._self.Raise()
                self._self.RequestUserAttention()
        

    #--------------------------------------------------
        '''Função FIM'''
        def FIM(self, event):
            print ('\nTopPanel - FIM')
      

            '''Diálogo se deseja realmente finalizar o CONDICIONAMENTO'''
            dlg = wx.MessageDialog(None, 'Deseja realmente finalizar o '+self._self.bottom.Fase+'?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                dlg.Destroy()
                self.fim_inicio.Disable()
                con.modeFIM()
                self.avanca.Disable()
                self.continua.Disable()

                self._self.bottom.threadLeituraDados.inicioEnsaio()
                self._self.bottom.threadLeituraDados.setEnsaio()
                self.X = np.array([])
                self.Y = np.array([])
                self._self.bottom.mult = 0
                self.draww()

                if self._self.bottom.Fase == 'CONDICIONAMENTO':
                    self._self.bottom._fase = 0
                    self._self.bottom.mr.Enable()
                    self.fim_inicio.SetLabel('INICIO')
                    self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                    SetarPressoes.ZerarPressaoGolpe(self.PressaoAtualGolpe)

                elif self._self.bottom.Fase == 'RT':
                    self._self.bottom._fase = 0
                    self._self.bottom.condic.Enable()
                    self._self.bottom.mr.Enable()
                    self.fim_inicio.SetLabel('INICIO')
                    self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                    self._self.bottom.Bind(wx.EVT_BUTTON,self._self.bottom.CONDIC,self._self.bottom.condic)

                elif self._self.bottom.Fase == 'MR':
                    SetarPressoes.ZerarPressaoGolpe(self.PressaoAtualGolpe)
                    bancodedados.data_final_Update_idt(self._self.bottom.Nome)
                    dlg3 = dialogoDinamico(3, "EDP 135/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório podem ser gerados na tela inicial.", "FIM!", "", None)
                    dlg3.ShowModal()
                    time.sleep(3)
                    self._self.bottom.threadLeituraDados.pause()
                    self._self.bottom.threadLeituraDados.stop()
                    time.sleep(.3)
                    con.modeB()
                    time.sleep(.3)
                    con.modeD()
                    time.sleep(0.3)
                    self._self.Destroy()
                


    #--------------------------------------------------
        def draww(self):
            print ('\nTopPanel - draww')
            self.axes.clear()
            self.axes.set_xlim(float(0), float(5))
            self.axes.set_ylim(float(0), float(0.01))
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.canvas.draw()

    #--------------------------------------------------
        def draw(self):
            print ('\nTopPanel - draw')
            self._self.bottom.mult
            if self._self.bottom.mult==1 and self.X[0]>1:
                self.X = np.delete(self.X, 0)
                self.Y = np.delete(self.Y,0)
            global colorLineGrafic
            self.axes.clear()
            if self._self.bottom.mult<=5:
                self.axes.set_xlim(float(0),float(5))
            else:
                self.axes.set_xlim(self._self.bottom.mult-5, self._self.bottom.mult)
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.axes.plot(self.X, self.Y, colorLineGrafic)
            self.canvas.draw()

        def criaBarraCarregamento(self,event):
            self.dialog = wx.ProgressDialog("Aguarde", "Aguarde, calibrando pressões", maximum=100,style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

        def updateBarra(self,event,valor):
            self.dialog.Update(valor)

        def cloesBarra(self,event):
            self.dialog.Destroy()

