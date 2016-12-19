#!/usr/bin/env python
# encoding: utf-8

"""
Introduction à WxPython - 01_mainloop.py

Une application wx minimale. Le passage du contrôle
de la boucle d'exécution à WxPython.

"""
import wx

app = wx.App()
frame = wx.Frame(None, title='Simple App', size=(250, 200))
frame.Show()

app.MainLoop()

