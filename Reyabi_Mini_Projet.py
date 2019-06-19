# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Mini_Projet_Zone
                                 A QGIS plugin
 Ce Mini projet consiste a créer un buffer d'un kilometrage définie 
                              -------------------
        begin                : 2019-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Reyabi Souhail
        email                : souhailereyabi@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Reyabi_Mini_Projet_dialog import Mini_Projet_ZoneDialog
import os.path
import  sys
import resources
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path
from qgis.core import *
import qgis.utils
import os.path
from qgis.gui import QgsMapCanvas

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsMessageLog
from PyQt4.QtGui import *
from PyQt4.Qt import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis import *
from qgis.gui import QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import QFileInfo
from PyQt4.QtXml import QDomDocument
from qgis.gui import *
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis import *
from qgis.core import *
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import *
from PyQt4.QtCore import *


# Initialize Qt resources from file resources.py
import resources


class Mini_Projet_Zone:
    """QGIS Plugin Implementation."""
    
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Mini_Projet_Zone_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Reyabi_Mini_Projet')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Mini_Projet_Zone')
        self.toolbar.setObjectName(u'Mini_Projet_Zone')

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
        return QCoreApplication.translate('Mini_Projet_Zone', message)


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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Mini_Projet_ZoneDialog()
        self.dlg.pushButton.clicked.connect(self.recuperer)
        self.dlg.pushButton_6.clicked.connect(self.zomm)
        self.dlg.pushButton_2.clicked.connect(self.buff)
        self.dlg.pushButton_3.clicked.connect(self.zoneAffected)
        self.dlg.pushButton_5.clicked.connect(self.resultat_final)
        self.dlg.pushButton_4.clicked.connect(self.export_Data)
        self.dlg.pushButton_8.clicked.connect(self.extent_Layer)
        self.dlg.pushButton_9.clicked.connect(self.Actualiser)
        self.dlg.pushButton_10.clicked.connect(self.add_point)
        self.dlg.pushButton_7.clicked.connect(self.method_2)
        self.dlg.pushButton_11.clicked.connect(self.sauvegader_projet)
        self.dlg.pushButton_12.clicked.connect(self.Restaurer_Projet)
        self.dlg.pushButton_13.clicked.connect(self.importer_Shapefile)
        self.dlg.tableWidget.currentItemChanged.connect(self.Zoom_l)



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
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Mini_Projet_Zone/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            layer.setProviderEncoding('utf-8')
            layer.dataProvider().setEncoding('utf-8')
                

        


    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Reyabi_Mini_Projet'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
    def recuperer(self):
        self.dlg.comboBox_2.clear()
        
        layer=None
        nameL=self.dlg.comboBox.currentText ()
        layerid=[]
        layerifo=[]
        layercc="Derogation"
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() ==nameL:
                layer = lyr
                break
        if layer.name()=='Derogation':       
            feat=layer.getFeatures()
            for ft in feat:
                attrs = ft.attributes()
                layerid.append(str(ft.id()))
            self.dlg.comboBox_2.addItems(layerid)
        else :
            feat=layer.getFeatures()
            for ft in feat:
                attrs = ft.attributes()
                layerid.append(str(ft.id()))
            self.dlg.comboBox_2.addItems(layerid)     
        self.dlg.pushButton_6.setEnabled(True)
    def Zoom_l(self):
        canvas = self.iface.mapCanvas()
        cLayer = self.FindLayerByName(self.dlg.comboBox.currentText())
        self.iface.setActiveLayer(cLayer)
        cLayer.removeSelection()
        indexes = self.dlg.tableWidget.selectionModel().selectedRows()
        ligneSelectionnee=0
        for index in sorted(indexes):
            ligneSelectionnee=index.row()
        print self.dlg.tableWidget.item(ligneSelectionnee,0).text()
        expression= "\"Identifiant\"="+self.dlg.tableWidget.item(ligneSelectionnee,1).text()
        expr = QgsExpression( expression)
        it = cLayer.getFeatures( QgsFeatureRequest( expr ) )
        ids = [i.id() for i in it]
        cLayer.setSelectedFeatures( ids )
        canvas.zoomToSelected(cLayer)
    def zomm(self):
        layer=None
        nameL=self.dlg.comboBox.currentText()
        idl=self.dlg.comboBox_2.currentText()
        layerid=[]

        layerifo=[]
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()==nameL:
                layer=lyr
                break
        feat=layer.getFeatures()
        canvas=qgis.utils.iface.mapCanvas()
        cLayer=canvas.currentLayer()
        cLayer=layer
        cLayer.removeSelection()
        cLayer.select(int(idl))
        canvas.zoomToSelected(cLayer)
        prov=cLayer.dataProvider()
        i=0
        for f in cLayer.getFeatures():
            if f.id()==int(idl):
                feat = QgsFeature()
                try:
                    pt = f.geometry().centroid().asPoint()
                    self.dlg.label_6.setText(str(pt.x()))
                    self.dlg.label_8.setText(str(pt.y())) 
                    self.dlg.pushButton_2.setEnabled(True)                  
                except :
                    QMessageBox.critical(None, "Verifie", "cette zone n'exist pas ")
      
                    return False

    def FindLayerByName(self,NameLayer):
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
           if lyr.name() == NameLayer:
               layer = lyr
               break
        return layer

    def buff(self):
        x=float(self.dlg.label_6.text())
        y=float(self.dlg.label_8.text())
        pt=QgsPoint(x,y)
        nameL=self.dlg.comboBox.currentText()
        idl=self.dlg.comboBox_2.currentText()
        layerid=[]
        layerifo=[]

            
        
        
         
        
       
        try:
            layer = QgsVectorLayer('Point?crs=EPSG:26191', 'point' , 'memory')
            bufferr=QgsVectorLayer('Polygon?crs=EPSG:26191', 'polyf' , 'memory')
            prov = layer.dataProvider()  
            provv= bufferr.dataProvider()
            buffer_nb=float(self.dlg.lineEdit.text())
            myPoint = QgsGeometry.fromPoint(pt)
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPoint(pt))
            prov.addFeatures([feat])
            layer.updateExtents()
            

        except:
            QMessageBox.critical(None, "Verifie", "Entrez la distance !!!")
            return False



        features = layer.getFeatures()
        for feat in features:
            inAttr = feat.attributes() # Input attributes
            inGeom = feat.geometry() # Input geometry
            bf_inGeom = inGeom.buffer(buffer_nb,30)
            poly=bf_inGeom.asPolygon()
            drawn_area = bf_inGeom.area()
            inAttr.append(drawn_area)
            outGeom = QgsFeature()
            outGeom.setGeometry(QgsGeometry.fromPolygon(poly)) # Output geometry
            outGeom.setAttributes(inAttr) # Output attributes
            provv.addFeatures([outGeom])
 
        QgsMapLayerRegistry.instance().addMapLayers([bufferr])
        QgsMapLayerRegistry.instance().addMapLayers([layer])
        self.dlg.pushButton_3.setEnabled(True)      

    def zoneAffected(self):
        self.dlg.tableWidget.setColumnCount(6)
        self.dlg.tableWidget.setRowCount(1)
        layer_grp=[]
        zone_intersection=[]
        layer_inter=None
        intersection_l=None
        inetrs=[]
        surface=0
        compteur=0
        fr=0
        pv=0
        i=0
        a=[]
        b=[]
        d=[]
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() =='polyf':
                layerbuffer=lyr
                break
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() !='polyf':
                if lyr.name() !='point':
                    layer_inter=lyr
                    layer_grp.append(lyr)
        for inter in layer_grp:
            for poly_feature in inter.getFeatures():
                for vl in layerbuffer.getFeatures():
                    try:
                        if inter.name()!='Derogation':
                            c=str(poly_feature["COMMUNE"])
                        else:
                            c=str(poly_feature["Commune"])

                        if poly_feature.geometry().intersects(vl.geometry()):
                            intersection_l=poly_feature.geometry().intersection(vl.geometry())
                            print  intersection_l.area()
                            surface+=intersection_l.area()
                            if inter.name()=='Derogation':
                                compteur=compteur+1
                            if inter.name()=='Foret':
                                fr=1
                            if inter.name()=='Prive':
                                pv=1            
                            self.dlg.tableWidget.insertRow(i+1)
                            self.dlg.tableWidget.setItem(i,0, QTableWidgetItem(inter.name()))
                            self.dlg.tableWidget.setItem(i,1, QTableWidgetItem(str(poly_feature.id())))
                            if inter.name()!='Derogation':
                                self.dlg.tableWidget.setItem(i,2, QTableWidgetItem(str(poly_feature["COMMUNE"])))
                            else:
                                self.dlg.tableWidget.setItem(i,2, QTableWidgetItem(str(poly_feature["Commune"])))
                                
                            self.dlg.tableWidget.setItem(i,3, QTableWidgetItem(str(intersection_l.area())))
                            self.dlg.tableWidget.setItem(i,4, QTableWidgetItem(str(surface)))
                            self.dlg.tableWidget.setItem(i,5, QTableWidgetItem(str(intersection_l.length())))  
                            zone_intersection.append(poly_feature)
                            self.dlg.label_11.setText(str(surface)+" m²") 
                            i=i+1
                            self.dlg.pushButton_4.setEnabled(False)
                            self.dlg.pushButton_5.setEnabled(True)

                    except:
                        print ''
        if compteur < 6 :
            if pv == 0:
                if fr==0:
                    self.dlg.label_16.setText("Accepte")
                    self.dlg.label_18.setText("Toutes les conditions acceptee")
                else:
                    self.dlg.label_16.setText("Refuse")
                    self.dlg.label_18.setText("il intersect avec un espace vert")
            else:
                self.dlg.label_16.setText("Refuse")
                self.dlg.label_18.setText("il intersect avec un une zone prive")
                if fr==1:
                    self.dlg.label_18.setText("il intersect avec un une zone prive et espace vert")
        else:
            self.dlg.label_16.setText("Refuse")
            self.dlg.label_18.setText("Le nombre de derogation est depassee dans cette zone")
            if fr==1 and pv==1:
                self.dlg.label_18.setText("aucune conditions est respectee")
            if fr==1:
                self.dlg.label_18.setText("intersection avec un espace vert et le nombre de derogation est depasse")
            if pv==1:
                self.dlg.label_18.setText("intersection avec un zone prive et le nombre de derogation est depasse")
                            
                        
                        
        canvas = self.iface.mapCanvas()
        canvas. zoomScale(60000)  
    def resultat_final(self):
        layer_grp=[]
        zone_intersection=[]
        layer_inter=None
        intersection_l=None
        inetrs=[]
        Wkt=[]
        poly=[]
        i=1
        pt_l=QgsVectorLayer()
        fet = QgsFeature()
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() =='point':
                pt_l=lyr
                break
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() =='polyf':
                layerbuffer=lyr
                break
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() !='polyf':
                if lyr.name() !='point':
                    layer_inter=lyr
                    layer_grp.append(lyr)

        temp2=QgsVectorLayer("Polygon?crs=EPSG:26191","zone_final", "memory")
        pr = temp2.dataProvider()
        field = QgsField("id", QVariant.String) 
        field1 = QgsField("nom_zone", QVariant.String)
        field2 = QgsField("Commune", QVariant.String)
        field3 = QgsField("surface", QVariant.String)
        pr.addAttributes([field])
        pr.addAttributes([field1])
        pr.addAttributes([field2])
        pr.addAttributes([field3])
        temp2.updateFields()
        for inter in layer_grp:
            for poly_feature in inter.getFeatures():
                for vl in layerbuffer.getFeatures():
                    try:
                        if poly_feature.geometry().intersects(vl.geometry()):
                            intersection_l=poly_feature.geometry().intersection(vl.geometry())
                            zone_intersection.append(intersection_l)


                            poly.append(poly_feature)
                            if inter.name()!='Derogation':
                                temp   = QgsVectorLayer("Polygon?crs=EPSG:26191",inter.name()+":"+str(poly_feature["COMMUNE"])+" ID :"+str(poly_feature.id()), "memory")
                                pr = temp.dataProvider()
                                field = QgsField("id", QVariant.String) 
                                field1 = QgsField("nom_zone", QVariant.String)
                                field2 = QgsField("Commune", QVariant.String)
                                field3 = QgsField("surface", QVariant.String)
                                pr.addAttributes([field])
                                pr.addAttributes([field1])
                                pr.addAttributes([field2])
                                pr.addAttributes([field3])
                                idx=str(poly_feature.id())
                                namez=inter.name()
                                namecommune=str(poly_feature["COMMUNE"])
                                surfacen=str(intersection_l.area())
                                temp.updateFields()
                               

                            else:
                                temp = QgsVectorLayer("Polygon?crs=EPSG:26191",inter.name()+":"+str(poly_feature["Commune"])+" ID :"+str(poly_feature.id()), "memory")
                                pr = temp.dataProvider()
                                field = QgsField("id", QVariant.String) 
                                field1 = QgsField("nom_zone", QVariant.String)
                                field2 = QgsField("Commune", QVariant.String)
                                field3 = QgsField("surface", QVariant.String)
                                pr.addAttributes([field])
                                pr.addAttributes([field1])
                                pr.addAttributes([field2])
                                pr.addAttributes([field3])
                                idx=str(poly_feature.id())
                                namez=inter.name()
                                namecommune=str(poly_feature["Commune"])
                                surfacen=str(intersection_l.area())
                                

                                #pr.setAttribute('Commune',str(poly_feature["Commune"]))
                                #pr.setAttribute('surface',str(intersection_l.area()))
                                temp.updateFields()


                                
                            
                            geom = QgsGeometry()
                            geom = QgsGeometry.fromWkt(intersection_l.exportToWkt())
                            feat = QgsFeature()
                            feat.setGeometry(geom)
                            feat.setAttributes([idx,namez,namecommune,surfacen])
                            temp.dataProvider().addFeatures([feat])
                            temp2.dataProvider().addFeatures([feat])
                            temp2.commitChanges()
                            temp.commitChanges()
                            for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                                if lyr.name()!='zone_final':
                                    QgsMapLayerRegistry.instance().addMapLayer(temp2)
                            #QgsMapLayerRegistry.instance().addMapLayer(temp)
                        
                    except:
                        print '' 

        canvas = self.iface.mapCanvas()
        canvas. zoomScale(60000)   
        zone_names=[]
        commune_names=[]
        for lyr  in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='zone_final':
                for wx in lyr.getFeatures():
                    zone_names.append(wx["nom_zone"])
                    commune_names.append(wx["Commune"])
        
         
        commune_names=list(set(commune_names))
        zone_names=list(set(zone_names))
        print commune_names
        print zone_names

        identifiant =""
        nouveau_nom=""
        nouveau_commune=""
        nouveau_surface=""
        


        for comm in commune_names:
                for nom in zone_names:
                    for wxx in temp2.getFeatures():
                        if wxx["nom_zone"]==nom:
                            if wxx["Commune"]==comm:
                                tp2=QgsVectorLayer("Polygon?crs=EPSG:26191",nom+" :"+comm+"", "memory")
                                pr=tp2.dataProvider()     
                                field = QgsField("id", QVariant.String)     
                                field1 = QgsField("nom_zone", QVariant.String)
                                field2 = QgsField("Commune", QVariant.String)
                                field3 = QgsField("surface", QVariant.String)
                                tp2.dataProvider().addAttributes([field])
                                tp2.dataProvider().addAttributes([field1])
                                tp2.dataProvider().addAttributes([field2])
                                tp2.dataProvider().addAttributes([field3])
                                tp2.updateFields()
                                for wx in temp2.getFeatures():
                                    if wx["nom_zone"]==nom:
                                        if wx["Commune"]==comm:
                                            identifiant=wx["id"]
                                            nouveau_nom=str(wx["nom_zone"])
                                            nouveau_commune=wx["Commune"]
                                            nouveau_surface=wx["surface"]
                                            geom = QgsGeometry()
                                            geom=QgsGeometry.fromWkt(wx.geometry().exportToWkt())
                                            feat.setGeometry(geom)
                                            feat.setAttributes([identifiant])
                                            feat.setAttributes([nouveau_nom])
                                            feat.setAttributes([nouveau_commune])
                                            feat.setAttributes([nouveau_surface])
                                            pr.addFeatures([feat])
                                            tp2.commitChanges()
                                            tp2.updateFields()
                                    
                    QgsMapLayerRegistry.instance().addMapLayer(tp2)
               

        x=float(self.dlg.label_6.text())
        y=float(self.dlg.label_8.text())
        pt=QgsPoint(x,y)
        laxor=QgsVectorLayer('Point?crs=EPSG:26191', "l'emplacement choisi" , 'memory')
        prov = laxor.dataProvider()  
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPoint(pt))
        prov.addFeatures([feat])
        laxor.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayer(laxor)

        self.dlg.pushButton_4.setEnabled(True)
        canvas = self.iface.mapCanvas()
        canvas. zoomScale(1000)
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='polyf':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())

        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='Prive':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='Public':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='Foret':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())      
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():      
            if lyr.name()=='Derogation':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='Collectif':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='Communal':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=='point':
                QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())

    def export_Data(self):
        
        el_renderer = self.iface.mapCanvas().mapRenderer()
        composition = QgsComposition(el_renderer) 
        composition.setPlotStyle(QgsComposition.Print)
        lst=[]
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values(): 
            if lyr.name()!="zone_final":
                lst.append(lyr.id())  # add ID of every layer
        
        el_renderer.setLayerSet(lst)
        el_renderer.setOutputSize(QSize(composition.paperWidth(), composition.paperHeight()), composition.printResolution())
        composer_map = QgsComposerMap(composition, 9,15,190,80)
        composer_map.setNewExtent(el_renderer.extent())
        composer_map.setFrameEnabled(True)
        composition.addComposerMap(composer_map)
        composition.addItem(composer_map)
        legend = QgsComposerLegend(composition)
        legend.model().setLayerSet(el_renderer.layerSet())
        legend.setItemPosition(240, 0, 0,0)
        legend.setFrameEnabled(True)
        composition.addItem(legend)
        composerLabel=QgsComposerLabel(composition)
        composerLabel.setText("La zone final determiner par le buffer")
        composerLabel.setFont(QFont("Times",22, QFont.SansSerif))

        composerLabel.adjustSizeToText()          
        composerLabel.setItemPosition(70, 0, 0,0)

        composerLabel.setFrameEnabled(True)
        composition.addItem(composerLabel)
        item = QgsComposerScaleBar(composition)
        item.setStyle('Numeric') # optionally modify the style
        item.setComposerMap(composer_map)
        item.setItemPosition(10,14,20,0)
        item.applyDefaultSize()
        composition.addItem(item)
       # map is an instance of QgsLayoutItemMap
        table = QgsComposerAttributeTable(composition)
        table.setComposerMap(composer_map)
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name()=="zone_final":
                table.setVectorLayer(lyr)
                table.setMaximumNumberOfFeatures(lyr.featureCount())
                table.setItemPosition(90,160,80,0)
                

        composition.addItem(table)
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Resultat_derogation.pdf")
        printer.setPaperSize(QSizeF(composition.paperWidth(), composition.paperHeight()), QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setColorMode(QPrinter.Color)
        printer.setResolution(composition.printResolution())
        pdfPainter = QPainter(printer)
        paperRectMM = printer.pageRect(QPrinter.Millimeter)
        paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
        composition.render(pdfPainter, paperRectPixel, paperRectMM)
        pdfPainter.end()

    

    def extent_Layer(self):
        try:
            valeur=float(self.dlg.lineEdit_2.text())
            canvas = self.iface.mapCanvas()
            canvas. zoomScale(valeur) 

        except :
            QMessageBox.critical(None, "Erreur", " Entrez un nombre !!!")

    def Actualiser(self):
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())

        layer =self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\COLLECTIF.shp", "Collectif", "ogr")
        layer2=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\Derogation_central_13_avril.shp", "Derogation", "ogr")
        layer3=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_COMMUNAL.shp", "Communal", "ogr")
        layer4=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_FORESTIER.shp", "Foret", "ogr")
        layer6=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMIANE_PRIVE_ETAT.shp", "Prive", "ogr")
        layer5=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_PUBLIC.shp", "Public", "ogr")
   
        layers = self.iface.legendInterface().layers()
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        QgsMapLayerRegistry.instance().addMapLayer(layer2)
        QgsMapLayerRegistry.instance().addMapLayer(layer3)
        QgsMapLayerRegistry.instance().addMapLayer(layer4)
        QgsMapLayerRegistry.instance().addMapLayer(layer6)
        QgsMapLayerRegistry.instance().addMapLayer(layer5)
        self.dlg.pushButton_2.setEnabled(False)
        self.dlg.pushButton_6.setEnabled(False)
        self.dlg.pushButton_4.setEnabled(False)
        self.dlg.pushButton_3.setEnabled(False)
        self.dlg.pushButton_5.setEnabled(False)
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.comboBox.addItems(layer_list)
    def method_2(self):
        self.dlg.lineEdit_3.setEnabled(True)
        self.dlg.lineEdit_4.setEnabled(True)
    def add_point(self):
        try:
            x=float(self.dlg.lineEdit_3.text())
            y=float(self.dlg.lineEdit_4.text())
            pt=QgsPoint(x,y)
        except:
            QMessageBox.critical(None, "Erreur", " Entrez des valeurs numériques")
            return False   
        layer_grp=[]
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() !='polyf':
                if lyr.name() !='point':
                    layer_inter=lyr
                    layer_grp.append(lyr)
        
       
        nameL=self.dlg.comboBox.currentText()
        
       
        layer = QgsVectorLayer("Point?crs=EPSG:26191", 'Point' , 'memory')
        prov = layer.dataProvider()
        myPoint = QgsGeometry.fromPoint(pt)
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPoint(pt))
        prov.addFeatures([feat])
        layer.updateExtents()
        #QgsMapLayerRegistry.instance().addMapLayers([layer])
        
        self.dlg.pushButton_2.setEnabled(True)
        self.dlg.label_6.setText(str(pt.x()))
        self.dlg.label_8.setText(str(pt.y()))
       
     
    def sauvegader_projet(self):
        qid = QInputDialog()
        title = "Entrez le nom de votre projet"
        label = "le nom:" 
        mode = QLineEdit.Normal    
        text, ok = QInputDialog.getText(qid, title, label, mode)
        if text !="":
            try:
                print "hello my name is zere9"
                project = QgsProject.instance()
                project.write()
# ... or to a new file
                mypath='C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Projets\SR_'+text+'.qgs'
                project.write(QFileInfo(mypath))
                QMessageBox.information(None, "information", " Succes!!")

            except:    
                QMessageBox.critical(None, "Erreur", " Fichier non sauvegardé")
                return False 

                            
    def Restaurer_Projet(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.qgs)")
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles() 
        try:    
            project = QgsProject.instance()
            project.read(QFileInfo(filenames[0]))
            QMessageBox.information(None, "information", " l'importer Votre projet est reussite")

        except:
            QMessageBox.critical(None, "Erreur", "impossible d'importer Votre projet")
    
    def importer_Shapefile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.shp)")
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            layer =self.iface.addVectorLayer(filenames[0],filenames[0], "ogr")
            layers = self.iface.legendInterface().layers()
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            QMessageBox.information(None, "information", " l'importation est reussite")

        



    def run(self):
        self.dlg.pushButton_2.setEnabled(False)
        self.dlg.pushButton_6.setEnabled(False)
        self.dlg.pushButton_4.setEnabled(False)
        self.dlg.pushButton_3.setEnabled(False)
        self.dlg.pushButton_5.setEnabled(False)


        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            QgsMapLayerRegistry.instance().removeMapLayer(lyr.id())

        layer =self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\COLLECTIF.shp", "Collectif", "ogr")
        layer2=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\Derogation_central_13_avril.shp", "Derogation", "ogr")
        layer3=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_COMMUNAL.shp", "Communal", "ogr")
        layer4=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_FORESTIER.shp", "Foret", "ogr")
        layer6=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMIANE_PRIVE_ETAT.shp", "Prive", "ogr")
        layer5=self.iface.addVectorLayer("C:\Users\RET\.qgis2\python\plugins\Mini_Projet_Zone\Couches\DOMAINE_PUBLIC.shp", "Public", "ogr")
   
        layers = self.iface.legendInterface().layers()
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        QgsMapLayerRegistry.instance().addMapLayer(layer2)
        QgsMapLayerRegistry.instance().addMapLayer(layer3)
        QgsMapLayerRegistry.instance().addMapLayer(layer4)
        QgsMapLayerRegistry.instance().addMapLayer(layer6)
        QgsMapLayerRegistry.instance().addMapLayer(layer5)

        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.comboBox.addItems(layer_list)

         
        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


        # See if OK was pressed


        
        