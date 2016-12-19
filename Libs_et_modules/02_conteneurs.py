#!/usr/bin/env python
# encoding: utf-8

"""
Introduction à WxPython - 02_conteneurs.py

Les conteneurs délimitent l'espace où les objets
graphiques seront affichés.

"""
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
	wx.Frame.__init__(self, parent, title=title, pos=pos, size=size)
	self.panel = wx.Panel(self)
	self.panel.SetBackgroundColour("#FFFFFF")

app = wx.App()

frame = MyFrame(None, title='Simple App', pos=(20, 20), size=(250, 200))
frame.Show()

app.MainLoop()

