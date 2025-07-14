# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
import unicodecsv
import csv
import math

pi = math.pi

'''Class Export CSV134'''
class Csv134(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        self.Bind(wx.EVT_CLOSE, self.onExit)
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_134(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

          '''Obter dados do banco'''
          list = bancodedados.dados_iniciais_(idt)
          lvdt = bdConfiguration.S1S2()
          
          
          if int(list[12]) == 0:
               valoramostra = 'Deformada'
          else:
               valoramostra = 'Indeformada'
          
          try:
               desvioUmidade = float(list[4])-float(list[6])
          except:
               desvioUmidade = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', list[9]])
                         editor.writerow(['Inicio do ensaio:', list[10]])
                         editor.writerow(['Fim do ensaio:', list[11]])
                         editor.writerow(['Natureza da amostra:', list[3]])
                         editor.writerow(['Tipo da amostra:', valoramostra])
                         editor.writerow(['Energia de compactacao:', list[7]])
                         editor.writerow(['Diametro [mm]:', format(list[13]).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(list[14]).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', list[4]])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', list[5]])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', list[8]])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', list[16]])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])                         
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1
                    dlg = wx.MessageDialog(None, 'CSV gerado com sucesso', 'EDP', wx.OK|wx.CENTRE)#codigo para mostrar uma mensagem de confirmação quando o csv for gerado
                    dlg.ShowModal()

               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

'''Class Export CSV179'''
class Csv179(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()
          
    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_179(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

          '''Obter dados do banco'''
          list = bancodedados.dados_iniciais_(idt)
          lvdt = bdConfiguration.S1S2()
          
          
          if int(list[12]) == 0:
               valoramostra = 'Deformada'
          else:
               valoramostra = 'Indeformada'
          
          try:
               desvioUmidade = float(list[4])-float(list[6])
          except:
               desvioUmidade = ''
          try:
               pressaoConf = float(list[17])*1000
          except:
               pressaoConf = ''
          try:
               pressaoDesvio = float(list[18])*1000
          except:
               pressaoDesvio = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', list[9]])
                         editor.writerow(['Inicio do ensaio:', list[10]])
                         editor.writerow(['Fim do ensaio:', list[11]])
                         editor.writerow(['Natureza da amostra:', list[3]])
                         editor.writerow(['Tipo da amostra:', valoramostra,])
                         editor.writerow(['Energia de compactacao:', list[7]])
                         editor.writerow(['Diametro [mm]:', format(list[13]).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(list[14]).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', list[4]])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', list[5]])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', list[8]])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', list[16]])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])
                         editor.writerow(['Sigma3 [kPa]:', format(pressaoConf).replace('.',',')])    
                         editor.writerow(['Sigmad [kPa]:', format(pressaoDesvio).replace('.',',')])                      
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1
                    dlg = wx.MessageDialog(None, 'CSV gerado com sucesso', 'EDP', wx.OK|wx.CENTRE)#codigo para mostrar uma mensagem de confirmação quando o pdf csv gerado
                    dlg.ShowModal()
               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

'''Class Export CSV181'''
class Csv181(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_181(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

          '''Obter dados do banco'''
          list = bancodedados.dados_iniciais_(idt)
          lvdt = bdConfiguration.S1S2()
          
          
          if int(list[12]) == 0:
               valoramostra = 'Deformada'
          else:
               valoramostra = 'Indeformada'
          
          try:
               desvioUmidade = float(list[4])-float(list[6])
          except:
               desvioUmidade = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', list[9]])
                         editor.writerow(['Inicio do ensaio:', list[10]])
                         editor.writerow(['Fim do ensaio:', list[11]])
                         editor.writerow(['Natureza da amostra:', list[3]])
                         editor.writerow(['Tipo de estabilizante quimico:', list[19]])
                         editor.writerow(['Tempo de cura [dias]:', list[21]])
                         editor.writerow(['Peso do estabilizante quimico [%]:', list[19]])
                         editor.writerow(['Energia de compactacao:', list[7]])
                         editor.writerow(['Diametro [mm]:', format(list[13]).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(list[14]).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', list[4]])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', list[5]])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', list[8]])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', list[16]])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])                         
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1
                    dlg = wx.MessageDialog(None, 'CSV gerado com sucesso', 'EDP', wx.OK|wx.CENTRE)#codigo para mostrar uma mensagem de confirmação quando o csv for gerado
                    dlg.ShowModal()
               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

