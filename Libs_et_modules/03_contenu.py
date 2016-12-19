#!/usr/bin/env python
# encoding: utf-8

"""
Introduction à WxPython - 03_contenu.py

Le contenu comprend tous les objets graphiques permettant 
à l'utilisateur d'interagir avec le programme.

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

app = wx.App()

frame = MyFrame(None, title='Simple App', pos=(20, 20), size=(250, 200))
frame.Show()

app.MainLoop()

