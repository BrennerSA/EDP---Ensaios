# -*- coding: utf-8 -*-
import wx
import back.connection as con
from pubsub import publish

########################################################################
'''ConexaoThread'''
class ConexaoThread():
    #-------------------------------------------------------------------

    def __init__(self, DISCREP):
        self.DISCREP = DISCREP
        self.status=''
        self.run()
        

    #-------------------------------------------------------------------
    def run(self):
        # wx.CallAfter(pub.sendMessage, "update", msg="      Conectando...")
        try:
            valor = con.connect(self.DISCREP)
            if valor == 'connectado':
                print ('CONECTADO')
                # wx.CallAfter(pub.sendMessage, "update", msg="          CONECTADO")
                self.status= 'connectado'
            else:
                print ('DESCONECTADO')
                # wx.CallAfter(pub.sendMessage, "update", msg="       DESCONECTADO")
                self.status= 'desconnectado'
        except:
            print ('ERRO VALOR DISCREP')
            # wx.CallAfter(pub.sendMessage, "update", msg="       DESCONECTADO")
            self.status= 'desconnectado'
    #-------------------------------------------------------------------

    def getStatus(self):
        return self.status
    
