# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import time
# import numpy as np
import banco.bancodedados as bancodedados
import back.connection as con
import front.BottomPanel135 as BottomPanel135
import front.TopPanel135 as TopPanel135
from drawnow import *
from front.dialogoDinamico import dialogoDinamico

'''Frequencias para o ensaio'''
frequencias = ['1']

'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNIT135(wx.Dialog):
    #--------------------------------------------------
        
    def __init__(self, identificador,  *args, **kwargs):
        ensaio=bancodedados.tipo_ensaio(identificador)
        wx.Dialog.__init__(self, parent = None, title = 'EDP - Ensaios Dinâmicos para Pavimentação - DNIT 135/2018ME - Tela Ensaio', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

        self.Bind(wx.EVT_CLOSE, self.onExit)

        
        '''Variáveis Globais'''
        global NomeEnsaio #nome do ensaio passado pela chamada da função
        NomeEnsaio=identificador

       

        '''Iserção do IconeLogo'''
        try:
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
        except:
            pass

        '''Configurações do SPLITTER'''
        splitter = wx.SplitterWindow(self)
        top=TopPanel135.TopPanel(splitter,self)
        self.bottom = BottomPanel135.BottomPanel(self,splitter, NomeEnsaio, top)
        splitter.SplitHorizontally(top,self.bottom, 0)
        splitter.SetMinimumPaneSize(390)
        top.draww()
        #top.draw(X,Y)
        '''plt.ion()'''

        self.Centre()
        self.Show()
        self.Maximize(True)

        '''Dialogo Inicial'''
        info = "EDP 135/2018ME"
        titulo = "Ajuste o Zero dos LVDTs"
        message1 = "Com o valor entre:"
        message2 = "2.5 e 3.0 Volts"
        message3 = "realizando a CONEXAO"
        dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, NomeEnsaio)
        dlg.ShowModal()

    #--------------------------------------------------
    def onExit(self, event):
        '''Opcao Sair'''
        print ("saindo")
        try:            
            self.bottom.threadLeituraDados.pause()
            self.bottom.threadLeituraDados.stop()
            time.sleep(3)
            con.modeB()
            time.sleep(.3)
            con.modeD()
        except Exception as e:
            print ("erro")
        self.Destroy()
    
    