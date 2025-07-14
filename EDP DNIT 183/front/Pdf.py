# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import banco.bancodedadosCAB as bancodedadosCAB
import banco.bancodedados as bancodedados
import banco.bdPreferences as bdPreferences
import banco.bdConfiguration as bdConfiguration
import back.HexForRGB as HexRGB
import wx.lib.agw.hyperlink as hl
import wx.lib.mixins.listctrl as listmix
from wx.lib.agw import ultimatelistctrl as ULC
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import subprocess
from pyppeteer import launch
import asyncio

#--------------------------------------------------
def pm(mm):
    return mm/0.352777

class EditableListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):
    #--------------------------------------------------
        def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_NO_HIGHLIGHT)

class pdf183(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF', style = wx.CLOSE_BOX)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.lista_ensaios=[]
        self.idt = idt

        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)
        self.SetSize((420,300))
        self.Centre()
        

        
        colors = bdPreferences.ListColors()
        colorBackground = colors[2]
        self.SetBackgroundColour(colorBackground)
        colors = bdPreferences.ListColors()
        colorTextCtrl = colors[1]
        colorBackground = colors[2]
        colorTextCtrl = HexRGB.RGB(colorTextCtrl)

        self.list_ctrl = EditableListCtrl(panel, size=(420,0))
        self.h_sizer.AddStretchSpacer(5)
        self.h_sizer.Add(self.list_ctrl, 0, wx.EXPAND)
        self.h_sizer.AddStretchSpacer(5)
        self.v_sizer.Add(self.h_sizer, 40, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddStretchSpacer(1)
        self.ok_button=wx.Button(panel, -1, 'OK')
        self.cancel_button=wx.Button(panel,-1,'Cancelar')
        self.h2_sizer.Add(self.ok_button, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.h2_sizer.Add(self.cancel_button, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.v_sizer.Add(self.h2_sizer, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizerAndFit(self.v_sizer)

        self.Bind(wx.EVT_BUTTON, self.onOK, self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.onExit, self.cancel_button)
        


        self.list_ctrl.InsertColumn(0, 'IDENTIFICAÇÃO', wx.LIST_FORMAT_CENTRE, width=120)
        self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=120)
        self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=125)
        self.list_ctrl.InsertColumn(3, '', wx.LIST_FORMAT_CENTRE, width=50)

        lista = bancodedados.ListaVisualizacao()
        index = 0
        for key, row in lista:
            pos = self.list_ctrl.InsertStringItem(index, row[0])
            self.list_ctrl.SetStringItem(index, 1, row[1])
            self.list_ctrl.SetStringItem(index, 2, row[2])
            self.checkbox = wx.CheckBox(self.list_ctrl,label=str(key))
            self.list_ctrl.SetItemWindow(pos, col=3, wnd=self.checkbox, expand=True)
            self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_toggle, self.checkbox)
            index += 1

        self.ShowModal()

        

        


        

        

    #--------------------------------------------------
     def on_checkbox_toggle(self, event):
        # print (self.checkbox.IsChecked())
        self.checkbox=event.GetEventObject()
        if self.checkbox.IsChecked():
            botao=event.GetEventObject() 
            id = int(botao.GetLabel()) 
            nome = bancodedados.qual_identificador(id)
            if len(self.lista_ensaios)==0:
                self.lista_ensaios=bancodedados.dados_da_coleta_183_pdf(nome[1])
            else:
                self.lista_ensaios.append(bancodedados.untrated183(nome[1]))
            # print(self.lista_ensaios)
        else:
            wx.MessageBox("Checkbox unchecked!", "Info", wx.OK | wx.ICON_INFORMATION)

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def onOK(self, event):
        # Continuar
        
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()


    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        # for ensaio in self.lista_ensaios:
                # self.list.append(bancodedados.dados_da_coleta_183_pdf(ensaio[1]))
        # self.list = bancodedados.dados_da_coleta_183_pdf(idt)
        self.list=self.lista_ensaios
        # self.list.extend(self.lista_ensaios)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)
    
    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            '''Obtendo os dados do cabeçario no bancoCAB'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) #obtenção do cabeçariao do ensaio
            

            '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) #obtenção dos dados do ensaio
            # lvdt = bdConfiguration.S1S2() #obtem dados do sensores S1 e S2

            if int(list[2]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''

            '''Criando arquivo PDF'''
            with wx.FileDialog(self,defaultDir=idt,defaultFile=idt, name=idt, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                # if fileDialog.ShowModal() == wx.ID_CANCEL:
                #     return

                # pathname = fileDialog.GetPath()
                pathname= 'C:\\Users\\brenn\\OneDrive\\Documentos\\testesEDP\\'+idt
                pathname=bancodedados.get_dir_result(1)
                pathname=pathname+"\\"+idt
                # try:
                if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                    diretorio = pathname
                else:
                    diretorio = pathname+".pdf"

                cnv = canvas.Canvas(diretorio, pagesize=A4)
                cnv.setTitle(idt)

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Fadiga')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Resistencia a tração:')
                cnv.drawRightString(pm(110), pm(200+x), 'Nivel de Tensão:')
                cnv.drawRightString(pm(110), pm(195+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Modulo de resiliencia Medio [MPa]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 183/2018-ME')
                cnv.drawString(pm(112), pm(225+x), list[9])
                cnv.drawString(pm(112), pm(220+x), list[10])
                cnv.drawString(pm(112), pm(215+x), list[11])
                cnv.drawString(pm(112), pm(210+x), list[3])
                cnv.drawString(pm(112), pm(205+x), list[24])
                list[25]=float(list[25])*100
                cnv.drawString(pm(112), pm(200+x), str(list[25]/100)+'%')
                cnv.drawString(pm(112), pm(195+x), str(list[16]))
                cnv.drawString(pm(112), pm(190+x), str(list[27]))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 700, 576)
                t.drawOn(cnv, pm(12), pm((23-len(lista))*6.35+25))

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])

                cnv.showPage()
                # pagina 2

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                
                defResiliente=[]
                difTensao=[]
                Ngolpes=[]
                i=1
                while i < len(lista):
                    defResiliente.append(float(lista[i][1]))
                    difTensao.append(float(lista[i][8]))
                    Ngolpes.append(float(lista[i][4]))
                    i+=1
                
                x=np.array(defResiliente)
                y=np.array(Ngolpes)

                log_x_data = np.log(x)
                log_y_data = np.log(y)

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared)

                

                intercept_MR_x_sigmad=intercept
                slope_MR_sigmad=slope

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=x, y=y, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Deformação especifica resiliente X Vida de Fadiga',xaxis=dict(title='Deformação especifica resiliente'), yaxis=dict(title='Numero de aplicações, N'))
                fig = go.Figure(data=data, layout=layout)
                fig.write_html('Img\\grafico.html')

                async def html_to_png(input_file, output_file):
                    browser = await launch()
                    page = await browser.newPage()
                    with open(input_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    await page.setContent(html_content)
                    await page.screenshot({'path': output_file, 'fullPage': True})
                    await browser.close()
                # options = {
                #     'format': 'png',
                #     'width': 1920,
                #     'height': 1280,
                # }
                # with open('grafico1.html') as f:
                #     imgkit.from_file(f, 'out.jpg')
                    
                html_input_file = 'Img\\grafico.html'
                output_file = 'Img\\grafico.png'

                asyncio.get_event_loop().run_until_complete(html_to_png(html_input_file, output_file))

                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(220), 'N='+ str(round(np.exp(intercept),4))+'*ε')
                cnv.setFont("Helvetica", 8)
                cnv.drawString(pm(172), pm(222), str(round(slope,4)))
                cnv.drawString(pm(170), pm(220), 'r')
                cnv.setFont("Helvetica", 11) 
                cnv.drawString(pm(150), pm(215), 'R^2= '+ str(round(r_squared,4)))
                cnv.drawString(pm(150), pm(210), 'K3= '+ str(round(np.exp(intercept),4)))
                cnv.drawString(pm(150), pm(205), 'n3= '+ str(round(slope,4)))
                
                
    


                x=np.array(difTensao)
                y=np.array(Ngolpes)

                log_x_data = np.log(x)
                log_y_data = np.log(y)

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared)

                

                intercept_MR_x_sigmad=intercept
                slope_MR_sigmad=slope

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=x, y=y, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Diferença de tensões X Vida de Fadiga',xaxis=dict(title='Diferença de tensões'), yaxis=dict(title='Numero de aplicações, N'))
                fig = go.Figure(data=data, layout=layout)
                # fig.update_xaxes(type='log')
                # fig.update_yaxes(type='log')
                fig.write_html('Img\\grafico1.html')

                async def html_to_png(input_file, output_file):
                    browser = await launch()
                    page = await browser.newPage()
                    with open(input_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    await page.setContent(html_content)
                    await page.screenshot({'path': output_file, 'fullPage': True})
                    await browser.close()
                # options = {
                #     'format': 'png',
                #     'width': 1920,
                #     'height': 1280,
                # }
                # with open('grafico1.html') as f:
                #     imgkit.from_file(f, 'out.jpg')
                    
                html_input_file = 'Img\\grafico1.html'
                output_file = 'Img\\grafico1.png'

                asyncio.get_event_loop().run_until_complete(html_to_png(html_input_file, output_file))
                
                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(120), 'N='+ str(round(np.exp(intercept),4))+'*σ')
                cnv.setFont("Helvetica", 8)
                cnv.drawString(pm(175), pm(122), str(round(slope,4)))
                cnv.drawString(pm(173), pm(120), 'd')
                cnv.setFont("Helvetica", 11) 
                cnv.drawString(pm(150), pm(115), 'R^2= '+ str(round(r_squared,4))) 
                cnv.drawString(pm(150), pm(110), 'K3= '+ str(round(np.exp(intercept),4)))
                cnv.drawString(pm(150), pm(105), 'n3= '+ str(round(slope,4)))

                cnv.drawInlineImage("Img\\grafico.png", 50, 400,width=300,height=300)
                
                cnv.drawInlineImage("Img\\grafico1.png", 50, 100,width=300,height=300)

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])


                leitorpdf='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
                leitorpdf=str(bancodedados.get_dir_result(2))

                cnv.save()
                self.Destroy()
                subprocess.Popen([leitorpdf, diretorio])