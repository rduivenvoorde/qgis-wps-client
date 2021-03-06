# -*- coding: utf-8 -*-
"""
 /***************************************************************************
   QGIS Web Processing Service Plugin
  -------------------------------------------------------------------
 Date                 : 09 November 2009
 Copyright            : (C) 2009 by Dr. Horst Duester
 email                : horst dot duester at kappasys dot ch

  ***************************************************************************
  *                                                                         *
  *   This program is free software; you can redistribute it and/or modify  *
  *   it under the terms of the GNU General Public License as published by  *
  *   the Free Software Foundation; either version 2 of the License, or     *
  *   (at your option) any later version.                                   *
  *                                                                         *
  ***************************************************************************/
"""
from __future__ import absolute_import
# Import the PyQt and the QGIS libraries
from builtins import object
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from .QgsWpsDockWidget import QgsWpsDockWidget
from . import version
from .doAbout import DlgAbout
from .apicompat.sipv2.compat import pystring
import os

SEXTANTE_SUPPORT = False
try:
    from sextante.core.Sextante import Sextante
    from wps.sextantewps.WpsAlgorithmProvider import WpsAlgorithmProvider
    SEXTANTE_SUPPORT = True
except ImportError:
    pass

# initialize Qt resources from file resources.py
from . import resources_rc


DEBUG = False

# Our main class for the plugin
class QgsWps(object):
  MSG_BOX_TITLE = "WPS Client"
  
  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface  

    #Initialise the translation environment
    self.plugin_dir = os.path.dirname(__file__)
    language = QSettings().value('locale/userLocale', QLocale().name())
    if language and len(language) >= 2:
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'wps_{}.qm'.format(language))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

  ##############################################################################

  def initGui(self):
 
    # Create action that will start plugin configuration
     self.action = QAction(QIcon(":/plugins/wps/images/wps-add.png"), "WPS-Client", self.iface.mainWindow())
     self.action.triggered.connect(self.run)
     
     self.actionAbout = QAction("About", self.iface.mainWindow())
     self.actionAbout.triggered.connect(self.doAbout)
         
    # Add toolbar button and menu item
     self.iface.addToolBarIcon(self.action)
     
     if hasattr(self.iface,  "addPluginToWebMenu"):
         self.iface.addPluginToWebMenu("WPS-Client", self.action)
         self.iface.addPluginToWebMenu("WPS-Client", self.actionAbout)
     else:
         self.iface.addPluginToMenu("WPS", self.action)
         self.iface.addPluginToWebMenu("WPS", self.action)

     
     self.myDockWidget = QgsWpsDockWidget(self.iface)
     self.myDockWidget.setWindowTitle('WPS')
     self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.myDockWidget)
     self.myDockWidget.show()

     if SEXTANTE_SUPPORT:
         self.provider = WpsAlgorithmProvider(self.myDockWidget)
     else:
         self.provider = None

     if self.provider:
        try:
            Sextante.addProvider(self.provider, True) #Force tree update
        except TypeError:
            Sextante.addProvider(self.provider)



  ##############################################################################

  def unload(self):
     if hasattr(self.iface,  "addPluginToWebMenu"):
         self.iface.removePluginWebMenu("WPS-Client", self.action)
         self.iface.removePluginWebMenu("WPS-Client", self.actionAbout)
     else:
         self.iface.removePluginToMenu("WPS", self.action)      
         self.iface.removePluginToMenu("WPS", self.actionAbout)
         
     self.iface.removeToolBarIcon(self.action)
    
     if self.myDockWidget:
         self.myDockWidget.close()
        
     self.myDockWidget = None

     if self.provider:
        Sextante.removeProvider(self.provider)

##############################################################################

  def run(self):  
    if self.myDockWidget.isVisible():
        self.myDockWidget.hide()
    else:
        self.myDockWidget.show()
        
  def doAbout(self):
      self.dlgAbout = DlgAbout()
      self.dlgAbout.show()

