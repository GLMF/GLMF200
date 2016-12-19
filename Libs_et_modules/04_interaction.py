#!/usr/bin/env python
# encoding: utf-8

"""
Introduction à WxPython - 04_interaction.py

Illustration de l'interaction entre la manipulation des objets
à l'écran et les fonctionnalités du programme.

"""
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
	wx.Frame.__init__(self, parent, title=title, pos=pos, size=size)
	self.panel = wx.Panel(self)
	self.panel.SetBackgroundColour("#FFFFFF")
	label = wx.StaticText(self.panel, label="Allo GLMF", pos=(90,40))
	choices = ["white", "red", "green", "blue", "yellow"]
	choose = wx.Choice(self.panel, choices=choices, pos=(85,70))
	choose.SetSelection(0)
	choose.Bind(wx.EVT_CHOICE, self.changeBackColour)

    def changeBackColour(self, evt):
	self.panel.SetBackgroundColour(evt.GetString())

app = wx.App()

frame = MyFrame(None, title='Simple App', pos=(20, 20), size=(250, 200))
frame.Show()

app.MainLoop()

