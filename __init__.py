# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MergeTwoLines
                                 A QGIS plugin
 merge two lines
                             -------------------
        begin                : 2018-05-25
        copyright            : (C) 2018 by Takayuki Mizutani
        email                : mizutani@ecoris.co.jp
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MergeTwoLines class from file MergeTwoLines.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .MergeTwoLines import MergeTwoLines
    return MergeTwoLines(iface)
