# -*- coding: utf-8 -*-

import wx
import back.HexForRGB as HexRGB

class MyFrame(wx.Frame):
    def __init__(self,):
        wx.Frame.__init__(self, None, title="Tela de Carregamento")
        self.panel = wx.Panel(self)

        # Cria o texto de carregamento
        self.loading_text = wx.StaticText(self.panel, label="Aguarde", pos=(50, 50))
        self.loading_text.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        # Cria a barra de progresso
        self.progress_bar = wx.Gauge(self.panel, range=10, pos=(50, 100), size=(200, 25))

        # Define o tamanho da janela e a centraliza na tela
        self.SetSize((300, 200))
        self.Center()


    def update_progress(self):
        # Atualiza a barra de progresso
        self.progress_bar.Pulse()

    def close(self):
        # Fecha a janela
        self.Close()

    def updateBarra(self,valor):
        self.progress_bar.SetValue(valor)
        self.Refresh()
        wx.MilliSleep(100)

    




