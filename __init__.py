# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Mini_Projet_Zone
                                 A QGIS plugin
 Ce Mini projet consiste a créer un buffer d'un kilometrage définie 
                             -------------------
        begin                : 2019-06-08
        copyright            : (C) 2019 by Reyabi Souhail
        email                : souhailereyabi@gmail.com
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
    """Load Mini_Projet_Zone class from file Mini_Projet_Zone.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Reyabi_Mini_Projet import Mini_Projet_Zone
    return Mini_Projet_Zone(iface)
