# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import datetime
import banco.bancodedados as bancodedados
from front.TelaRealizacaoEnsaioDNIT135 import TelaRealizacaoEnsaioDNIT135

tipos = ['SIMPLES', 'COMPLETO']

class EditarDNIT135(wx.Dialog):
    #--------------------------------------------------
    def __init__(self, idt,mainref, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 135/2018ME - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.mainref=mainref
            # self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()
            

        
        #--------------------------------------------------
    def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_iniciais_(idt)

        self.DIAMETRO_MINIMO = 97.8
        self.DIAMETRO_MAXIMO =  105.4
        self.ALTURA_MINIMA = 35
        self.ALTURA_MAXIMA = 70
        '''Iserção do IconeLogo'''
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
        extra_box=wx.BoxSizer(wx.HORIZONTAL)

        def add_row(label, ctrl):
            text = wx.StaticText(window, label=label, style=wx.ALIGN_RIGHT)
            grid_sizer.Add(text, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            grid_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

        # Adicionando campos na primeira coluna
        self.identificador_text_input = wx.TextCtrl(window, -1, idt, style=wx.TE_RIGHT)
        add_row("Identificação*", self.identificador_text_input)
        self.identificador_text_input.Disable()

        self.natureza_amostra_text_input = wx.TextCtrl(window, -1, self.list[3], style=wx.TE_RIGHT)
        add_row("Natureza da Amostra", self.natureza_amostra_text_input)
        self.natureza_amostra_text_input.Disable()

        self.altura_text_input = wx.TextCtrl(window, -1, str(self.list[14]), style=wx.TE_RIGHT)
        add_row("Altura C.P. (mm)*", self.altura_text_input)
        self.altura_text_input.Disable()

        self.diametro_text_input = wx.TextCtrl(window, -1, str(self.list[13]), style=wx.TE_RIGHT)
        add_row("Diâmetro C.P. (mm)*", self.diametro_text_input)
        self.diametro_text_input.Disable()

        self.observacoes_text_input = wx.TextCtrl(window, -1, self.list[15], style=wx.TE_RIGHT)
        add_row("Observações", self.observacoes_text_input)
        self.observacoes_text_input.Disable()
        
        # Adicionando campos na segunda coluna
        self.formacao_text_input = wx.TextCtrl(window, -1, self.list[23], style=wx.TE_RIGHT)
        add_row("Formação/CREA", self.formacao_text_input)
        self.formacao_text_input.Disable()

        self.resistencia_tracao_text_input = wx.TextCtrl(window, -1, self.list[24], style=wx.TE_RIGHT)
        add_row('R.T.', self.resistencia_tracao_text_input)
        self.resistencia_tracao_text_input.Disable()

        dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
        self.data_text_input = wx.adv.DatePickerCtrl(window, id=wx.ID_ANY, dt=dateC, size=wx.DefaultSize, style=wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN)
        add_row("Data da coleta ou recebimento", self.data_text_input)
        self.data_text_input.Disable()

        self.responsavel_tecnico_text_input = wx.TextCtrl(window, -1, self.list[22], style=wx.TE_RIGHT)
        add_row("Responsável Técnico", self.responsavel_tecnico_text_input)
        self.responsavel_tecnico_text_input.Disable()

        self.tensao_input = wx.TextCtrl(window, -1, str(float(self.list[25])*100), style=wx.TE_RIGHT)
        add_row("Nível de tensão %*", self.tensao_input)
        self.tensao_input.Disable()

        principal_box.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 15)

        self.editar = wx.Button(window, -1, 'Editar')
        self.editar.Bind(wx.EVT_BUTTON, self.Editar)
        self.salvar = wx.Button(window, -1, 'Salvar')
        self.salvar.Bind(wx.EVT_BUTTON, self.Salvar)
        self.salvar.Disable()
        self.Ensaio = wx.Button(window, -1, 'Ensaio')
        self.Ensaio.Bind(wx.EVT_BUTTON, self.Prosseguir)

        if int(self.list[1]) != 0:
            self.Ensaio.Disable()
        
        
        extra_box.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        extra_box.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        extra_box.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        

        principal_box.Add(extra_box, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

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
        resistencia_tracao=format(resistencia_tracao).replace(',','.')
        data = self.data_text_input.GetValue()
        diametro = self.diametro_text_input.GetValue()
        diametro = format(diametro).replace(',','.')
        diametro = format(diametro).replace('-','')
        altura = self.altura_text_input.GetValue()
        altura = format(altura).replace(',','.')
        altura = format(altura).replace('-','')
        obs = self.observacoes_text_input.GetValue()
        tensao=self.tensao_input.GetValue()
        tensao=format(tensao).replace(',','.')
        self.mainref.Hide()
        self.Hide()
        TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
        self.mainref.Show()
        self.Show()
        

    def Salvar(self, event):
        identificador = self.identificador_text_input.GetValue()
        natureza_amostra = self.natureza_amostra_text_input.GetValue()
        tecnico = self.responsavel_tecnico_text_input.GetValue()
        formacao = self.formacao_text_input.GetValue()
        resistencia_tracao = self.resistencia_tracao_text_input.GetValue()
        resistencia_tracao=format(resistencia_tracao).replace(',','.')
        data = self.data_text_input.GetValue()
        diametro = self.diametro_text_input.GetValue()
        diametro = format(diametro).replace(',','.')
        altura = self.altura_text_input.GetValue()
        altura = format(altura).replace(',','.')
        obs = self.observacoes_text_input.GetValue()
        tensao=self.tensao_input.GetValue()
        tensao=format(tensao).replace(',','.')
        

        try:
            diametro = float(diametro)
            altura = float(altura)
            tensao=float(tensao)/100
            resistencia_tracao=float(resistencia_tracao)

        except ValueError:
            # print('Os valores digitados em algum dos campos nao esta da maneira esperada')
            menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            return

        if identificador == '' or (tensao>0.25 or tensao<0.05):
            '''Diálogo para Forçar preenchimento da Identificacao'''
            dlg = wx.MessageDialog(None, 'É necessário que no mínimo a Indentificação seja preenchida.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
            dlg.ShowModal()
        else:
            # Confere altura e diametro do corpo de prova pra ve se estão dentro do parametro da Norma
            if diametro>= self.DIAMETRO_MINIMO and diametro<=self.DIAMETRO_MAXIMO and altura>=self.ALTURA_MINIMA and altura<=self.ALTURA_MAXIMA:
                '''Salva os dados iniciais de um ensaio'''
                bancodedados.update_dados_135(identificador, natureza_amostra, tecnico,formacao, resistencia_tracao, data, diametro, altura, obs,tensao)
                self.editar.Enable()
                if int(self.list[1]) != 0:
                    self.Ensaio.Disable()
                self.salvar.Disable()
                self.responsavel_tecnico_text_input.Disable()
                self.formacao_text_input.Disable()
                self.natureza_amostra_text_input.Disable()
                self.resistencia_tracao_text_input.Disable()
                self.data_text_input.Disable()
                self.diametro_text_input.Disable()
                self.altura_text_input.Disable()
                self.tensao_input.Disable()
                self.observacoes_text_input.Disable()
            else:
                '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()

    def Editar(self, event):
        self.editar.Disable()
        self.Ensaio.Disable()
        self.salvar.Enable()
        self.responsavel_tecnico_text_input.Enable()
        self.formacao_text_input.Enable()
        self.natureza_amostra_text_input.Enable()
        self.resistencia_tracao_text_input.Enable()
        self.data_text_input.Enable()
        self.diametro_text_input.Enable()
        self.altura_text_input.Enable()
        self.tensao_input.Enable()
        self.observacoes_text_input.Enable()

