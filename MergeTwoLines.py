# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MergeTwoLines
                                 A QGIS plugin
 merge two lines
                              -------------------
        begin                : 2018-05-25
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Takayuki Mizutani
        email                : mizutani@ecoris.co.jp
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math
import resources
import os.path




class MergeTwoLines:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MergeTwoLines_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MergeTwoLines')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MergeTwoLines')
        self.toolbar.setObjectName(u'MergeTwoLines')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MergeTwoLines', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):


        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/MergeTwoLines/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MergeTwoLines'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MergeTwoLines'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        self.merge()

    def distance(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)

    def merge(self):
        canvas = self.iface.mapCanvas()
        layer = canvas.currentLayer()
        if layer.wkbType() == 2:
            selected_features = layer.selectedFeatures()
            if len(selected_features) == 2:
                f0 = selected_features[0]
                f1 = selected_features[1]
                line0 = f0.geometry().asPolyline()
                line1 = f1.geometry().asPolyline()
                dist = [self.distance(li0, li1) for li0, li1 in
                        [(line0[-1], line1[0]), (line0[0], line1[-1]), (line0[0], line1[0]), (line0[-1], line1[-1])]]
                type = dist.index(min(dist))
                if type == 0:
                    pass
                elif type == 1:
                    line0.reverse()
                    line1.reverse()
                elif type == 2:
                    line0.reverse()
                elif type == 3:
                    line1.reverse()
                line = line0 + line1[1:]
                geom = QgsGeometry.fromPolyline(line)
                layer.beginEditCommand("Feature merged")
                settings = QSettings()
                disable_attributes = settings.value("/qgis/digitizing/disable_enter_attribute_values_dialog", False,
                                                    type=bool)
                if disable_attributes:
                    layer.changeGeometry(f0.id(), geom)
                    layer.deleteFeature(f1.id())
                    layer.endEditCommand()
                else:
                    dlg = self.iface.getFeatureForm(layer, f0)
                    if dlg.exec_():
                        layer.changeGeometry(f0.id(), geom)
                        layer.deleteFeature(f1.id())
                        layer.endEditCommand()
                    else:
                        layer.destroyEditCommand()
                self.iface.mapCanvas().refresh()
            else:
                self.iface.messageBar().pushMessage("Warning", "Select two feature!",
                                               level=QgsMessageBar.WARNING)
        else:
            self.iface.messageBar().pushMessage("Warning", "Only Support LineString.",
                                           level=QgsMessageBar.WARNING)


    def log(self,msg):
        QgsMessageLog.logMessage(msg, 'MyPlugin',QgsMessageLog.INFO)