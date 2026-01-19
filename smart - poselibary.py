import maya.cmds as cmds
import json
import os
import sys
from collections import OrderedDict
import pymel.core as pm
import glob

from PySide2.QtWidgets import QWidget, QLabel, QFormLayout, QSizePolicy, QGridLayout, QPushButton, QListView, QHBoxLayout, QStackedLayout, QFileDialog, QLineEdit, QListWidget, QListWidgetItem
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPixmap, QIcon
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        selection = pm.selected()[0].longName()
        topnode = selection.split('|')[1]
        self.setWindowTitle(topnode + "'s Pose Library")
        
        # Create a horizontal layout for the first section
        self.layout1 = QFormLayout()
        self.layout1.addRow("Name of saved pose:", QLineEdit())
        self.layout1.addRow("Description:", QLineEdit())
        self.layout1.addRow("Aurthor:", QLineEdit())
        
        self.layout1.addRow(QHBoxLayout())
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.exportAnim)
        self.layout1.addWidget(self.save)
        
        # Create another horizontal layout for the second section
        layout2 = QHBoxLayout()
        self.list_widget = QListWidget()
        layout2.addWidget(self.list_widget)
        self.list_widget.setViewMode(QListView.IconMode)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_widget.itemClicked.connect(self.item_clicked)
      
        layout3 = QHBoxLayout()
        self.apply = QPushButton("Apply to Rig", self)
        self.apply.clicked.connect(self.importAnim)
        layout3.addWidget(self.apply)

        # Add the sub-layouts to the main layout
        main_layout.addLayout(self.layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(layout3)

        # Create a QWidget
        widget = QWidget()
        widget.setLayout(main_layout)
        
        #Set layouts  
        container1 = QWidget()
        container1.setLayout(main_layout)    
        self.setCentralWidget(container1)
        
        #Fill with skeleton's poses
        filefolder = glob.glob(os.path.join("/Users/**/Documents/maya/projects/default/movies/", topnode))
        for name in glob.glob(os.path.join("/Users/**/Documents/maya/projects/default/movies/", topnode, "*")):
    
            icon = QIcon(name)
            size = QSize(200, 200)
            self.list_widget.setIconSize(size)
            item = QListWidgetItem(icon, os.path.basename(name))
            self.list_widget.addItem(item) 
            
    #Set up logic for clicking on object     
    def item_clicked(self, item):
        currentitem = self.list_widget.currentItem()
        
    def importAnim(self):
        #Find current item in saved folders
        text = self.list_widget.currentItem().text()
        filefolder = glob.glob('/Users/**/Documents/maya/projects/default/assets')
        fileloc = os.path.join(filefolder[0], text)
        
        #Set attributes with json
        with open(fileloc) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
               
                translateX = cmds.setAttr(key + ".translateX",  value[0])
                translateY = cmds.setAttr(key + ".translateY",  value[1])
                translateZ = cmds.setAttr(key + ".translateZ",  value[2])
                rotateX = cmds.setAttr(key + ".rotateX", value[3])
                rotateY = cmds.setAttr(key + ".rotateY", value[4])
                rotateZ = cmds.setAttr(key + ".rotateZ", value[5])
       
    def exportAnim(self):
        #Put all of characters playblast in character file
        selection = pm.selected()[0].longName()
        charactername = selection.split('|')[1]
 
        playblastDirname = glob.glob("/Users/**/Documents/maya/projects/default/movies/")   
        playblastOutputPath = str(os.path.join(playblastDirname[0], charactername, self.layout1.itemAt(1).widget().text() + ".png"))

        pm.playblast(viewer=True, format="image", frame=1, cf=playblastOutputPath)
        
        #Create icon from new playblast file  
        playblastFile = glob.glob(os.path.join(playblastDirname[0]))
        icon = QIcon(playblastOutputPath)
        size = QSize(200, 200)
        self.list_widget.setIconSize(size)
        
        item = QListWidgetItem(icon, self.layout1.itemAt(1).widget().text() + ".png")
        self.list_widget.addItem(item)
        item.setData(Qt.ToolTipRole, self.layout1.itemAt(3).widget().text())
        item.setData(Qt.UserRole, self.layout1.itemAt(5).widget().text())
        
        #Select all controls by name
        pm.select('ctrl_hip', replace=True)
        all = pm.listRelatives('ctrl_hip', typ='transform', ad=True)
        pm.select(all, add=True)
        pm.select('locator1', add=True)
        pm.select('locator2', add=True)
        pm.select('locator3', add=True)
        pm.select('locator4', add=True)
        pm.select('IKcontrol_IK_left_arm1', add=True)
        pm.select('IKcontrol_IK_left_leg1', add=True)
        pm.select('IKcontrol_IK_right_arm1', add=True)
        pm.select('IKcontrol_IK_right_leg1', add=True)
        jointslist = pm.ls( selection=True )
        jointslist = [str(node) for node in jointslist]
        
        #Export these controls translates and rotates
        joints = []
        values = []
    
        for ctrl in jointslist:
            translateX = cmds.getAttr(ctrl + ".translateX")
            translateY = cmds.getAttr(ctrl + ".translateY")
            translateZ = cmds.getAttr(ctrl + ".translateZ")
            rotateX = cmds.getAttr(ctrl + ".rotateX")
            rotateY = cmds.getAttr(ctrl + ".rotateY")
            rotateZ = cmds.getAttr(ctrl + ".rotateZ")
            listt = []
            listt.append(int(translateX))
            listt.append(int(translateY))
            listt.append(int(translateZ))
            listt.append(int(rotateX))
            listt.append(int(rotateY))
            listt.append(int(rotateZ))
            values.append(listt)
            joints.append(ctrl)
        res = {}
  
        for key in joints:
            for value in values:
                res[key] = value
                values.remove(value)
                break
       
        exportAnimDirname = glob.glob('/Users/**/Documents/maya/projects/default/assets')
        exportAnimFile = os.path.join(exportAnimDirname[0], self.layout1.itemAt(1).widget().text())
        with open(exportAnimFile, 'w') as fp:
            json.dump(res, fp)
        
#If no skeleton is selected dont open app
if not pm.selected():
    print("Please select a skeleton root")
         
else:
    #Search for top node of selected it
    selection = pm.selected()[0].longName()
    selection.split('|')[1]
 
    app = QApplication.instance()

    window = MainWindow()
    window.show()

    app.exec_()
