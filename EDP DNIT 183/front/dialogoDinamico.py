# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences 
import back.ConexaoThread as ConexaoThread
import back.connection as con
import banco.bancodedados as bancodedados
import back.SetarPressoes as SetarPressoes
import time
import threading

'''Tela Dialogo Dinamico'''
class dialogoDinamico(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, info, texto0, texto1, texto2, texto3, texto4, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "%s" %info, style = wx.CLOSE_BOX)

            colors = bdPreferences.ListColors()
            colorBackground = colors[2]

            self.SetBackgroundColour(colorBackground)
            self.ensaio=bancodedados.tipo_ensaio(texto4)
            self.Nome=self.ensaio[2]
            
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer2 = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h_sizer2= wx.BoxSizer(wx.HORIZONTAL)
            self.Bind(wx.EVT_CLOSE, self.onExit)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            Fonttext = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            colors = bdPreferences.ListColors()
            colorCard = colors[0]
            colorTextCtrl = colors[1]
            colorBackground = colors[2]
            colorLineGrafic = colors[3]
            colorBackgroundGrafic = colors[4]
            colorStaticBox = HexRGB.RGB(colorCard)
            colorTextBackground = HexRGB.RGB(colorCard)
            colorTextCtrl = HexRGB.RGB(colorTextCtrl)
            staticbox5 = wx.StaticBox(self, -1, '')
            staticbox6 = wx.StaticBox(self, -1, '')
            staticboxSizer5 = wx.StaticBoxSizer(staticbox5, wx.VERTICAL)
            staticboxSizer6 = wx.StaticBoxSizer(staticbox6, wx.VERTICAL)
            staticbox5.SetBackgroundColour(colorStaticBox)
            staticbox6.SetBackgroundColour(colorStaticBox)

            
            

            self.resistencia=float(self.ensaio[25])
            self.tensao=float(self.ensaio[26])/100
            FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
            TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))
            TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
            TextoCorpo1.SetFont(FontCorpo1)
            TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
            TextoCorpo2.SetFont(FontCorpo2)
            TextoCorpo2.SetForegroundColour((231,160,48))
            self.ButtonConectar = wx.Button(self, label = "Conectar", style = wx.BORDER_NONE)
            ButtonSair=wx.Button(self, label= "Sair", style=wx.BORDER_NONE)
            self.ButtonInicio = wx.Button(self, label = "Iniciar", style = wx.BORDER_NONE)
            self.ButtonFim = wx.Button(self, label = "Finalizar", style = wx.BORDER_NONE)
            self.ButtonPausar = wx.Button(self, label = "Pausar", style = wx.BORDER_NONE)
            self.ButtonInicio.Disable()
            self.ButtonFim.Disable()
            self.ButtonPausar.Disable()
            self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
            self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
            self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
            # self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER | wx.LEFT)
            # self.v_sizer.Add(Button2,1,wx.ALL | wx.CENTER)
            self.h_sizer2.Add(self.ButtonConectar, 0, wx.ALL | wx.CENTER)
            self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
            self.h_sizer2.Add(self.ButtonInicio, 0, wx.ALL | wx.CENTER)
            self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
            self.h_sizer2.Add(self.ButtonPausar, 0, wx.ALL | wx.CENTER)
            self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
            self.h_sizer2.Add(self.ButtonFim, 0, wx.ALL | wx.CENTER)
            self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
            self.h_sizer2.Add(ButtonSair, 0, wx.ALL | wx.CENTER)
            self.v_sizer2.Add(self.h_sizer2,1, wx.CENTER)
            self.v_sizer.Add(self.v_sizer2,0,  wx.EXPAND | wx.ALL, 1)
            # self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
            self.Bind(wx.EVT_BUTTON, self.Conectar, self.ButtonConectar)
            self.Bind(wx.EVT_BUTTON, self.Cancelar, ButtonSair)
            self.Bind(wx.EVT_BUTTON, self.inicio, self.ButtonInicio)
            self.Bind(wx.EVT_BUTTON, self.pausar, self.ButtonPausar)
            self.Bind(wx.EVT_BUTTON, self.finalizar, self.ButtonFim)
            
            
            texto_sigmad = wx.StaticText(self, label = "σd - Tensão Tração (MPa)", style = wx.ALIGN_CENTRE)
            texto_real = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto_alvo = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
                        
            texto_sigmad.SetFont(FontTitle)
            texto_real.SetFont(Fonttext)
            texto_alvo.SetFont(Fonttext)

            texto_sigmad.SetBackgroundColour(colorTextBackground )
            texto_real.SetBackgroundColour(colorTextBackground )
            texto_alvo.SetBackgroundColour(colorTextBackground )

            self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

            self.SigmaReal.Disable()
            self.SigmaAlvo.Disable()

            self.SigmaReal.SetFont(Fonttext)
            self.SigmaAlvo.SetFont(Fonttext)

            self.SigmaReal.SetForegroundColour(colorTextCtrl)
            self.SigmaAlvo.SetForegroundColour(colorTextCtrl)

            self.v8_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v9_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v10_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h6_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v8_sizer.Add(texto_alvo, 1, wx.ALL | wx.CENTER)
            self.v8_sizer.Add(self.SigmaAlvo, 2, wx.ALL | wx.CENTER)

            self.v9_sizer.Add(texto_real, 1, wx.ALL | wx.CENTER)
            self.v9_sizer.Add(self.SigmaReal, 2, wx.ALL | wx.CENTER)

            self.h5_sizer.Add(self.v9_sizer, 6, wx.CENTER)
            self.h5_sizer.AddStretchSpacer(1)
            self.h5_sizer.Add(self.v8_sizer, 6, wx.CENTER)

            self.v10_sizer.Add(texto_sigmad, 1, wx.ALL | wx.CENTER)
            self.v10_sizer.Add(self.h5_sizer, 3, wx.ALL | wx.CENTER)

            self.h6_sizer.Add(self.v10_sizer, 1, wx.CENTER)
            staticboxSizer5.Add(self.h6_sizer, 0, wx.ALL | wx.CENTER, 10)
            self.v_sizer.Add(staticboxSizer5,1,wx.CENTER)
            # self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
            
            
            
            
            
            texto_fase = wx.StaticText(self, label = "Nivel de Tensão", style = wx.ALIGN_CENTER)
            texto_numero_ciclos = wx.StaticText(self, label = "CICLO Atual", style = wx.ALIGN_CENTER)

            # texto_ciclo_atual = wx.StaticText(self, label = "CICLO Atual", style = wx.ALIGN_CENTER)

            texto_fase.SetFont(FontTitle)
            texto_numero_ciclos.SetFont(Fonttext)

            # texto_ciclo_atual.SetFont(Fonttext)

            texto_fase.SetBackgroundColour(colorTextBackground )
            texto_numero_ciclos.SetBackgroundColour(colorTextBackground )

            # texto_ciclo_atual.SetBackgroundColour(colorTextBackground )

            self.fase = wx.TextCtrl(self, -1, str(self.tensao*100)+'%', size = (60, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (60, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            # self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            
            
            
            self.fase.Disable()
            self.NGolpes.Disable()
            # self.GolpeAtual.Disable()

            
            self.fase.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            # self.GolpeAtual.SetFont(Fonttext)

            
            self.fase.SetForegroundColour(colorTextCtrl)
            self.NGolpes.SetForegroundColour(colorTextCtrl)
            # self.GolpeAtual.SetForegroundColour(colorTextCtrl)
            
            self.v3_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v4_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v5_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v6_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v7_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h4_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # self.v3_sizer.Add(texto_ciclo_atual, 1, wx.ALL | wx.CENTER)
            # self.v3_sizer.Add(self.GolpeAtual, 2, wx.ALL | wx.CENTER, 5)


            self.v5_sizer.Add(texto_numero_ciclos, 1, wx.ALL | wx.CENTER)
            self.v5_sizer.Add(self.NGolpes, 2, wx.ALL | wx.CENTER, 5)

            self.v6_sizer.Add(texto_fase, 1, wx.ALL | wx.CENTER)
            self.v6_sizer.Add(self.fase, 2, wx.ALL | wx.CENTER, 5)

            self.h2_sizer.Add(self.v4_sizer, 3, wx.CENTER)
            self.h2_sizer.AddStretchSpacer(1)
            self.h2_sizer.Add(self.v3_sizer, 4, wx.CENTER)

            self.h3_sizer.Add(self.v6_sizer, 3, wx.CENTER)
            self.h3_sizer.AddStretchSpacer(1)
            self.h3_sizer.Add(self.v5_sizer, 4, wx.CENTER)

            self.v7_sizer.Add(self.h3_sizer, 3, wx.ALL | wx.CENTER)
            self.v7_sizer.AddStretchSpacer(1)
            self.v7_sizer.Add(self.h2_sizer, 3, wx.ALL | wx.CENTER)

            self.h4_sizer.Add(self.v7_sizer, 1, wx.CENTER)
            staticboxSizer6.Add(self.h4_sizer, 0, wx.ALL | wx.CENTER, 10)
            
            self.v_sizer.Add(staticboxSizer6,1,wx.CENTER)
            self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
            

            self.SetSizer(self.h_sizer)
            self.SetSize((620,450))


            self.Centre()
            self.Show()
            
    #--------------------------------------------------
        def Button(self, event):
            self.EndModal(wx.ID_OK)
            self.Destroy()
        
        def threadAttDados(self):
            print ("inicio thread")
            cont1 = 0
            self.pressoes=[]
            self.fim=False
            self.valoresEnsaio = [0,0,0,0,0,0,0,0,0,0]
            while not self.fim:
                self.valoresEnsaio = con.ColetaI(self.valoresEnsaio,self.ensaio[0])
                if cont1 >= 20: #atualiza os dados na tela a cada 20 iterações
                    self.NGolpes.SetLabelText(str(self.valoresEnsaio[8]))
                    # self.GolpeAtual.SetLabelText(str(int(self.valoresEnsaio[8])))
                    self.SigmaReal.SetLabelText(str(round(abs(self.valoresEnsaio[6]), 3)))
                    self.pressoes.append(self.valoresEnsaio[6])
                if cont1 == 20:
                    cont1 = 0
                cont1 = cont1 + 1
                # if int(self.valoresEnsaio[0])==self.valoresEnsaio[0] and int(self.valoresEnsaio[0])%3600==0:
                #     bancodedados.dados_dnit183_parcial(self.Nome,0,self.resistencia,self.tensao,sum(self.pressoes)/len(self.pressoes),int(self.valoresEnsaio[8]),self.ensaio[14],self.ensaio[15],self.ensaio[28])
                if self.valoresEnsaio[5]!=0 or self.valoresEnsaio[7]!=0:
                    if self.valoresEnsaio[7]==2:
                        print("Tensão do lvdt ultrapassou o limite permitido")
                    elif self.valoresEnsaio[7]==4:
                        print("rompimento do corpo de prova ou sensor indutivo saiu da posição")
                    # or self.valoresEnsaio[5]!=0
                    self.fim=True
                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.ButtonFim.GetId())
                    wx.PostEvent(self.ButtonFim, evt)
                    break
            print ("fim da thread de leitura do arduino")
            
        
    #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
        

        def Cancelar(self, event):
            try:
                con.modeB()
                time.sleep(1)
                con.modeD()
                time.sleep(1)
           
            except Exception as e:
                print("Exceção:", type(e).__name__)
                print ("não conectado")
            self.EndModal(wx.ID_ABORT)
            self.Destroy()
        
        def Conectar(self,event):
            try:
                teste=ConexaoThread.ConexaoThread(1.05) #roda thread de conexão
                status=teste.getStatus()
                if status == 'connectado':
                    menssagError = wx.MessageDialog(self, 'CONECTADO!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    con.modeConectDNIT135() #acessa o ensaio da 135 no arduino
                    self.ButtonInicio.Enable()
                    self.ButtonConectar.Disable()
                else:
                        menssagError = wx.MessageDialog(self, 'Não é possível manter uma conexão serial!', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                        aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                        menssagError.ShowModal()
                        menssagError.Destroy()
            except Exception as e:
                print("Exceção:", type(e).__name__)
                menssagError = wx.MessageDialog(self, 'ERRO AO EXECUTAR O CONECTAR', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()

        def inicio(self,event):
            Forca=(self.resistencia*self.tensao*3.1416*self.ensaio[14]*self.ensaio[15]*0.000001)/2
            # tens=Forca/((3.1416*0.01)/4)
            tens2=Forca*0.1618*1000
            self.SigmaAlvo.SetLabelText("%.3f" % (tens2))
            self.NGolpes.SetLabelText(str(0))
            self.fase.SetLabelText(str(self.tensao*100)+"%")
            # self.GolpeAtual.SetLabelText(str(0))
            dialog = wx.ProgressDialog("Aguarde", "Aguarde, calibrando pressões", maximum=100,parent=self)
            time.sleep(.5)
            dialog.Update(33)
            SetarPressoes.SetarPressaoGolpe(tens2,0,0.1)
            self.PressaoAtualGolpe=self.resistencia*self.tensao
            time.sleep(0.5)
            dialog.Update(66)
            dialog.Update(100)
            dialog.Close()
            gl = 50
            freq = 1
            con.modeG()
            bancodedados.Update_freq(self.Nome, int(freq))
            bancodedados.data_inicio_Update_idt(self.Nome)
            con.modeGOLPES135(int(gl), int(freq),1)
            self.ButtonPausar.Enable()
            self.ButtonFim.Enable()
            self.ButtonInicio.Disable()
            self.t = threading.Thread(target=self.threadAttDados, args=())
            self.t.start()

        def pausar(self,event):
            con.modeP()
            self.ButtonPausar.SetLabelText("Continua")
            self.Bind(wx.EVT_BUTTON, self.continua, self.ButtonPausar)

        def finalizar(self,event):
            self.ButtonInicio.Disable()
            self.ButtonFim.Disable()
            con.modeFIM()
            self.fim=True
            time.sleep(3)
            bancodedados.data_final_Update_idt(self.Nome)
            # if self.ensaio[27] != '':
            #     self.Nome=self.ensaio[27]
            bancodedados.dados_dnit183(self.Nome,self.ensaio[16],self.resistencia,self.tensao,sum(self.pressoes)/len(self.pressoes),int(self.NGolpes.GetLabel()),self.ensaio[14],self.ensaio[15],self.ensaio[28])
            SetarPressoes.ZerarPressaoGolpe(self.PressaoAtualGolpe)
            menssagFinal = wx.MessageDialog(self, 'ENSAIO FINALIZADO - PRESSIONE "SAIR" PARA FECHAR A JANELA!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
            aboutPanel = wx.TextCtrl(menssagFinal, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagFinal.ShowModal()
            menssagFinal.Destroy()
            self.ButtonConectar.Disable()
            self.ButtonInicio.Disable()
            self.ButtonPausar.Disable()
            self.ButtonPausar.Disable()
        
        def continua(self,event):
            con.modeC()
            self.ButtonPausar.SetLabelText("Pausar")
            self.Bind(wx.EVT_BUTTON, self.pausar, self.ButtonPausar)
            


       


