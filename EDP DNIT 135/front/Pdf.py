# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import banco.bancodedadosCAB as bancodedadosCAB
import banco.bancodedados as bancodedados
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

class pdf135(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_135_pdf(idt)

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
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Modulo de Resiliencia para misturas asfalticas')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Resistencia a tração [MPa]:')
                cnv.drawRightString(pm(110), pm(200+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(195+x), 'Temperatura do ensaio:')
                cnv.drawRightString(pm(110), pm(190+x), 'Coeficiente de Poisson adotado [μ]:')
                cnv.drawRightString(pm(110), pm(185+x), 'Nivel de Tensão Inicial:')


                # cnv.drawRightString(pm(110), pm(190+x), 'Modulo de resiliencia Medio [MPa]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 135/2018-ME')
                cnv.drawString(pm(112), pm(225+x), list[9])
                cnv.drawString(pm(112), pm(220+x), list[10])
                cnv.drawString(pm(112), pm(215+x), list[11])
                cnv.drawString(pm(112), pm(210+x), list[3])
                cnv.drawString(pm(112), pm(205+x), list[24])
                # list[25]=float(list[25])*100
                # cnv.drawString(pm(112), pm(200+x), str(list[25])+'%')
                cnv.drawString(pm(112), pm(200+x), str(list[16]))
                cnv.drawString(pm(112), pm(195+x), '25°C')
                # cnv.drawString(pm(112), pm(190+x), str(list[27]))
                cnv.drawString(pm(112), pm(190+x), '0,3')
                nivel_tensao=float(list[25])*100
                cnv.drawString(pm(112), pm(185+x), str(nivel_tensao)+"%")

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 700, 576)
                t.drawOn(cnv, pm(30), pm((21-len(lista))*6.35+25))

                fase1=[]
                fase2=[]
                fase3=[]
                x3=[]
                y3=[]
                pontos=bancodedados.getpulso135(idt)
                for item in pontos:
                    if item[0]==1:
                        fase1.append(item)
                    elif item[0]==2:
                        fase2.append(item)
                    else:
                        x3.append(item[1])
                        y3.append(item[2])

                trace_scatter = go.Scatter(x=x3, y=y3, mode='markers',name='Pontos',marker=dict(color='black'))
                data = [trace_scatter]
                layout = go.Layout(title='Pulso dos ultimos 5 golpes',xaxis=dict(title='Numero de Golpes, N',showline=True, linecolor='black'), yaxis=dict(title='Deslocamento, (mm)',showline=True,linecolor='black'),plot_bgcolor='white',xaxis_gridcolor='lightgray',yaxis_gridcolor='lightgray')
                fig = go.Figure(data=data, layout=layout)
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

                # imgkit.from_file(html_file_path, output_image_path,options=options)
                # image_bytes = to_image(fig, format='png')
                # fig.write_image('D:\\Games\\Nova pasta\\grafico1.jpeg')
                # pio.write_image(fig, 'grafico1.png')
                cnv.drawInlineImage("Img\\grafico1.png", 55, 75,width=500,height=300)
                

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
