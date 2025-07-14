# -*- coding: utf-8 -*-

import wx
import banco.bdPreferences as bdPreferences

class ColorSelectionFrame(wx.Frame):
    def __init__(self, parent,tipo, id=wx.ID_ANY, title="Seleção de Cor", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(ColorSelectionFrame, self).__init__(parent, id, title, pos, size, style)

        panel = wx.Panel(self)
        self.tipo=tipo
        color_button = wx.Button(panel, label="Selecionar Cor")
        color_button.Bind(wx.EVT_BUTTON, self.on_color_button_click)

        self.color_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.color_text.SetValue("Cor selecionada: Nenhum")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(color_button, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self.color_text, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)
        self.Show()

    def on_color_button_click(self, event):
        color_data = wx.ColourData()
        color_dialog = wx.ColourDialog(self, data=color_data)

        if color_dialog.ShowModal() == wx.ID_OK:
            selected_color = color_dialog.GetColourData().GetColour()
            hex_color = selected_color.GetAsString(wx.C2S_HTML_SYNTAX)
            self.color_text.SetValue("Cor selecionada: {}".format(hex_color))
            if self.tipo==1:
                bdPreferences.update_back(hex_color)
            elif self.tipo==2:
                bdPreferences.update_card(hex_color)
            else:
                bdPreferences.update_textctrl(hex_color)

        color_dialog.Destroy()
        

