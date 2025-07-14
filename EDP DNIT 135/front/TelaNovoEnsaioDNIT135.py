# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import banco.bancodedados as bancodedados
from front.TelaRealizacaoEnsaioDNIT135 import TelaRealizacaoEnsaioDNIT135

DIAMETRO_MINIMO = 97.8
DIAMETRO_MAXIMO = 105.4
ALTURA_MINIMA = 35
ALTURA_MAXIMA = 70

'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT135(wx.Dialog):
    def __init__(self, mainref, *args, **kwargs):
        wx.Frame.__init__(self, None, -1, 'EDP - DNIT 135/2018ME', style=wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
        self.mainref = mainref

        '''Inserção do Ícone'''
        try:
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
        except:
            pass

        '''Configurações do Tamanho'''
        self.SetSize((600, 400))
        window_sizer = wx.BoxSizer(wx.VERTICAL)
        principal_box = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(0, 4, 10, 10)  # 4 colunas (label e input para cada coluna)
        
        window = wx.Panel(self)

        # Título da tela
        FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        title = wx.StaticText(window, label="Dados do Ensaio", style=wx.ALIGN_CENTRE)
        title.SetFont(FontTitle)
        principal_box.Add(title, 0, wx.EXPAND | wx.ALL, 10)

        def add_row(label, ctrl):
            text = wx.StaticText(window, label=label, style=wx.ALIGN_RIGHT)
            grid_sizer.Add(text, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            grid_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

        # Adicionando campos na primeira coluna
        self.identificador_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Identificação*", self.identificador_text_input)

        self.natureza_amostra_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Natureza da Amostra", self.natureza_amostra_text_input)

        self.altura_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Altura C.P. (mm)*", self.altura_text_input)

        self.diametro_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Diâmetro C.P. (mm)*", self.diametro_text_input)

        self.observacoes_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Observações", self.observacoes_text_input)
        
        # Adicionando campos na segunda coluna
        self.formacao_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Formação/CREA", self.formacao_text_input)

        self.resistencia_tracao_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row('R.T.', self.resistencia_tracao_text_input)

        self.data_text_input = wx.adv.DatePickerCtrl(window, id=wx.ID_ANY, dt=wx.DefaultDateTime, size=wx.DefaultSize, style=wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN)
        add_row("Data da coleta ou recebimento", self.data_text_input)

        self.responsavel_tecnico_text_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Responsável Técnico", self.responsavel_tecnico_text_input)

        self.tensao_input = wx.TextCtrl(window, -1, '', style=wx.TE_RIGHT)
        add_row("Nível de tensão %*", self.tensao_input)

        principal_box.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 15)

        continuar = wx.Button(window, -1, 'Continuar')
        continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)
        principal_box.Add(continuar, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        window_sizer.Add(principal_box, 1, wx.EXPAND | wx.ALL, 15)
        window.SetSizer(window_sizer)
        self.Centre()
        self.Show()

    def Prosseguir(self, event):
        identificador = self.identificador_text_input.GetValue()
        natureza_amostra = self.natureza_amostra_text_input.GetValue()
        tecnico = self.responsavel_tecnico_text_input.GetValue()
        formacao = self.formacao_text_input.GetValue()
        resistencia_tracao = self.resistencia_tracao_text_input.GetValue()
        resistencia_tracao = format(resistencia_tracao).replace(',', '.')
        data = self.data_text_input.GetValue()
        diametro = self.diametro_text_input.GetValue()
        diametro = format(diametro).replace(',', '.')
        diametro = format(diametro).replace('-', '')
        altura = self.altura_text_input.GetValue()
        altura = format(altura).replace(',', '.')
        altura = format(altura).replace('-', '')
        obs = self.observacoes_text_input.GetValue()
        tensao = self.tensao_input.GetValue()
        tensao = format(tensao).replace(',', '.')

        try:
            diametro = float(diametro)
            altura = float(altura)
            tensao = float(tensao) / 100
            resistencia_tracao = float(resistencia_tracao)
        except ValueError:
            menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK | wx.ICON_INFORMATION)
            menssagError.ShowModal()
            menssagError.Destroy()
            return

        if identificador == '' or (tensao > 0.25 or tensao < 0.05):
            dlg = wx.MessageDialog(None, 'É necessário que no mínimo a Identificação seja preenchida.', 'EDP', wx.OK | wx.CENTRE | wx.ICON_INFORMATION)
            dlg.ShowModal()
        else:
            if identificador in bancodedados.data_identificadores():
                dlg = wx.MessageDialog(None, 'Já existe um Ensaio com essa Identificação.', 'EDP', wx.OK | wx.CENTRE | wx.ICON_INFORMATION)
                dlg.ShowModal()
            else:
                if DIAMETRO_MINIMO <= diametro <= DIAMETRO_MAXIMO and ALTURA_MINIMA <= altura <= ALTURA_MAXIMA:
                    bancodedados.data_save_dados_135(identificador, natureza_amostra, tecnico, formacao, resistencia_tracao, data, diametro, altura, obs, tensao)
                    self.Close(True)
                    self.mainref.Hide()
                    TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
                    self.mainref.Show()
                else:
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx.CENTRE | wx.ICON_INFORMATION)
                    dlg.ShowModal()
