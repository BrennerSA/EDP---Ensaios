# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bancodedadosCAB as bancodedadosCAB
import banco.bdPreferences as bdPreferences
import wx.lib.mixins.listctrl as listmix
from front.NovoCabecalho import NovoCabecalho
from front.EditarCabecalho import EditarCabecalho
from wx.lib.agw import ultimatelistctrl as ULC
import back.HexForRGB as HexRGB

'''Classe da Lista editável'''
class EditableListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):
    #----------------------------------------------------------------------
        def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_NO_HIGHLIGHT)


'''Tela Cabeçalhos'''
class Cab(wx.Dialog):

        def UpdateListCtrl(self):
            lista = bancodedadosCAB.ListaVisualizacaoCab()
            index = 0
            list_cab = []

            for key, row in lista:
                   list_cab.append(row[0])
                   if index == 0:
                           pos = self.list_ctrl.InsertStringItem(index, row[0])
                           buttonEDT = wx.Button(self.list_ctrl,  label=str(key))
                           buttonDEL = wx.Button(self.list_ctrl,  label=str(key))
                           buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-neditar-arquivo-24px.png'))
                           buttonEDT.SetForegroundColour(buttonEDT.GetBackgroundColour())
                           buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-nlixo-24px.png'))
                           buttonDEL.SetForegroundColour(buttonEDT.GetBackgroundColour())
                           self.list_ctrl.SetItemWindow(pos, col=1, wnd=buttonEDT, expand=True)
                           self.list_ctrl.SetItemWindow(pos, col=2, wnd=buttonDEL, expand=True)
                           self.list_ctrl.SetItemData(index, key)
                           index += 1
                   else:
                           pos = self.list_ctrl.InsertStringItem(index, row[0])
                           buttonEDT = wx.Button(self.list_ctrl,  label=str(key))
                           buttonDEL = wx.Button(self.list_ctrl,  label=str(key))
                           buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-neditar-arquivo-24px.png'))
                           buttonEDT.SetForegroundColour(buttonEDT.GetBackgroundColour())
                           buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-nlixo-24px.png'))
                           buttonDEL.SetForegroundColour(buttonEDT.GetBackgroundColour())
                           self.list_ctrl.SetItemWindow(pos, col=1, wnd=buttonEDT, expand=True)
                           self.list_ctrl.SetItemWindow(pos, col=2, wnd=buttonDEL, expand=True)
                           self.list_ctrl.SetItemData(index, key)
                           self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
                           self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
                           index += 1

            self.list_ctrl.SetColumnWidth(0, width=230)
            self.list_ctrl.SetColumnWidth(1, width=40)
            self.list_ctrl.SetColumnWidth(2, width=40)

            return list_cab
        #--------------------------------------------------
        # construtor
        def __init__(self, *args, **kwargs):
                wx.Dialog.__init__(self, None, -1, 'EDP - Cabeçalhos', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                v_sizer = wx.BoxSizer(wx.VERTICAL)
                h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
                panel = wx.Panel(self)

                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Iserção do IconeLogo'''
                try:
                    ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                    self.SetIcon(ico)
                except:
                    pass

                '''Configurações do Size'''
                self.SetSize((360,520))

                self.CadastrarCabecalhoButton = wx.Button(panel, -1, '', size=(30, 30))
                self.CadastrarCabecalhoButton.SetBitmap(wx.Bitmap(r'icons\icons-adicionar-48px.png'))
                self.Bind(wx.EVT_BUTTON, self.NovoCabecalho, self.CadastrarCabecalhoButton)
                self.Bind(wx.EVT_CLOSE, self.onExit)
                v_sizer.AddStretchSpacer(5)
                v_sizer.Add(self.CadastrarCabecalhoButton, 0, wx.ALIGN_CENTER_HORIZONTAL)
                v_sizer.AddStretchSpacer(4)
                panel.SetSizerAndFit(v_sizer)


                # '''Lista onde os Cabeçalhos são armazenados na tela'''
                self.list_ctrl = EditableListCtrl(panel, size=(315,0))
                h_sizer.AddStretchSpacer(5)
                h_sizer.Add(self.list_ctrl, 0, wx.EXPAND)
                h_sizer.AddStretchSpacer(5)
                v_sizer.Add(h_sizer, 40, wx.ALIGN_CENTER_HORIZONTAL)
                v_sizer.AddStretchSpacer(1)
                panel.SetSizerAndFit(v_sizer)

                 # definindo as colunas a serem mostradas na tela
                self.list_ctrl.InsertColumn(0, 'CABEÇALHOS', wx.LIST_FORMAT_CENTRE, width=230)
                self.list_ctrl.InsertColumn(1, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
                self.list_ctrl.InsertColumn(2, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)


                self.list_cab = self.UpdateListCtrl()
                

                self.definirAtual = wx.Button(panel, -1, 'Definir Atual')

                if len(self.list_cab) == 1:
                    self.combo = wx.ComboBox(panel, value = self.list_cab[0], choices = self.list_cab, style = wx.EXPAND | wx.CB_READONLY)
                    self.definirAtual.Disable()
                else:
                    self.combo = wx.ComboBox(panel, value = self.list_cab[0], choices = self.list_cab, style = wx.EXPAND | wx.CB_READONLY)
                    self.Bind(wx.EVT_BUTTON, self.DefinirATUAL, self.definirAtual)

                h2_sizer.AddStretchSpacer(5)
                h2_sizer.Add(self.combo, 10, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
                h2_sizer.Add(self.definirAtual, 10, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
                h2_sizer.AddStretchSpacer(5)
                v_sizer.Add(h2_sizer, 5, wx.ALIGN_CENTER_HORIZONTAL)
                v_sizer.AddStretchSpacer(1)

                panel.SetSizer(v_sizer)
                self.Centre()
                self.Show()

    #--------------------------------------------------
        def NovoCabecalho(self, event):
            dialogo = NovoCabecalho().ShowModal()

            self.list_ctrl.DeleteAllItems()
            self.list_cab = self.UpdateListCtrl()
            

            self.combo.SetItems(self.list_cab) # adiciona ao combobox todos itens da lista de cabeçalhos
            idCabImpress = bancodedadosCAB.idEscolha() #seleciona a id do cabeçalho marcado para impressão
            nomeCab = bancodedadosCAB.id_identificador(idCabImpress) #busca o identificador do cabeçalho marcado
            index = self.list_cab.index(str(nomeCab)) # recebe o index do cabeçalho com esse identificador
            self.combo.SetSelection(index) # define o item selecionado no combobox pelo index
            self.definirAtual.Enable() # libera o botão que define o cabeçalho
            self.Bind(wx.EVT_BUTTON, self.DefinirATUAL, self.definirAtual)


    #--------------------------------------------------
        def DefinirATUAL(self, event):
            try:
                nomeCab = self.combo.GetStringSelection() #obtem o nome do identificador do cab
                idCab = bancodedadosCAB.identificador_id(nomeCab) #busca a id do cabeçalho com esse nome
                bancodedadosCAB.updateEscolha(idCab) # atualiza a tabela do banco de dados que marca o cabeçalho escolhido
                dlg = wx.MessageDialog(self, 'O cabeçalho '+str(nomeCab)+' foi definido como atual.', 'EDP', wx.OK | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
            except:
                dlg = wx.MessageDialog(self, 'O cabeçalho não pode ser definido como atual', '#ERROR', wx.OK | wx.ICON_INFORMATION)
                result = dlg.ShowModal()


    #--------------------------------------------------
        def Editar(self, event):
            botao=event.GetEventObject() #trecho utilizado para resolver o problema com as ids, futuramente replicar
            id = int(botao.GetLabel())
            dialogo = EditarCabecalho(id).Show()

            self.list_ctrl.DeleteAllItems()
            self.list_cab = self.UpdateListCtrl()

            self.combo.SetItems(self.list_cab)
            idCabImpress = bancodedadosCAB.idEscolha()
            nomeCab = bancodedadosCAB.id_identificador(idCabImpress)
            index = self.list_cab.index(str(nomeCab))
            self.combo.SetSelection(index)
            self.definirAtual.Enable()
            self.Bind(wx.EVT_BUTTON, self.DefinirATUAL, self.definirAtual)

    #--------------------------------------------------
        def Deletar(self, event):
            botao=event.GetEventObject() 
            id = int(botao.GetLabel())

            '''Diálogo se deseja realmente excluir a Cápsula'''
            dlg = wx.MessageDialog(None, 'Deseja mesmo excluir essa Cabeçalho?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                bancodedadosCAB.deleteCAB(id)
                self.list_ctrl.DeleteAllItems()
                self.list_cab = self.UpdateListCtrl()
                idCabImpress = bancodedadosCAB.idEscolha()
                atual = self.combo.GetStringSelection()
                

                if len(self.list_cab) == 1:
                    self.combo.SetItems(self.list_cab)
                    self.combo.SetSelection(0)
                    self.combo.Update()
                    bancodedadosCAB.updateEscolha(0)
                    self.definirAtual.Disable()
                elif id == idCabImpress:
                    self.combo.SetItems(self.list_cab)
                    self.combo.SetSelection(0)
                    self.combo.Update()
                    bancodedadosCAB.updateEscolha(0)
                else:
                    self.combo.SetItems(self.list_cab)
                    nomeCab = bancodedadosCAB.id_identificador(idCabImpress) #busca o identificador do cabeçalho marcado
                    index = self.list_cab.index(str(nomeCab))
                    self.combo.SetSelection(index)
                    self.combo.Update()
            else:
                dlg.Destroy()
        
        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
