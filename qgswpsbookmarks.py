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

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from . import version
from .wpslib.wpsserver import WpsServer
from .wpslib.processdescription import ProcessDescription

from .Ui_qgswpsbookmarks import Ui_Bookmarks

class Bookmarks(QDialog, QObject,  Ui_Bookmarks):
    """
    Class documentation goes here.
    """
    getBookmarkDescription = pyqtSignal(QTreeWidgetItem)
    bookmarksChanged = pyqtSignal()
    
    def __init__(self, fl,  parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent,  fl)
        self.setupUi(self)
        self.setWindowTitle('QGIS WPS-Client '+version())
        self.initTreeWPSServices()
        
    def initTreeWPSServices(self):
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(self.treeWidget.columnCount())
        itemList = []
        for process in ProcessDescription.getBookmarks():
           myItem = QTreeWidgetItem()
           myItem.setText(0, process.server.connectionName)
           myItem.setText(1,process.identifier)
           myItem.setText(2,process.server.server)
           itemList.append(myItem)
           self.myItem = myItem #FIXME: backwards compatibility
        self.btnOK.setEnabled(False)
        self.treeWidget.addTopLevelItems(itemList)        


    def on_treeWidget_itemDoubleClicked(self, item, column):
        self.getBookmarkDescription.emit(item)
        self.close()

    def on_btnConnect_clicked(self):
        self.close()

    def on_btnEdit_clicked(self):
         pass

    def on_btnRemove_clicked(self):
        if self.treeWidget.currentItem():
            self.removeBookmark(self.treeWidget.currentItem())

    def on_btnOK_clicked(self):
        self.getBookmarkDescription.emit(self.myItem)

    def on_btnClose_clicked(self):
         self.close()
         
    def removeBookmark(self, item):
        QMessageBox.information(None, '', item.text(0)+'@@'+item.text(1))
        server = WpsServer.getServer(item.text(0))
        process = ProcessDescription(server, item.text(1))
        process.removeBookmark()
        self.bookmarksChanged.emit()
        self.initTreeWPSServices()          
