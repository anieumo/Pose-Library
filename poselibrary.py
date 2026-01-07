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
        '''
        self.apply = QPushButton("apply", self)
        self.apply.clicked.connect(self.importAnim)
        self.save = QPushButton("save", self)
        self.save.clicked.connect(self.exportAnim)
        
        mainlayout = QVBoxLayout()
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.apply)
        
        
        self.layout2 = QVBoxLayout()
        self.layout1.addWidget(self.save)
        self.label = QLineEdit()
        self.layout1.addWidget(self.label)
        
        self.layout3 = QVBoxLayout()
        self.list_widget = QListWidget()
        self.layout1.addWidget(self.list_widget)
        
        mainlayout.addLayout(self.layout1)
        mainlayout.addLayout(self.layout2)
        mainlayout.addLayout(self.layout3)
        self.container1 = QWidget()
        self.container1.setLayout(mainlayout)
        '''
        main_layout = QHBoxLayout()

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
           
        container1 = QWidget()
        container1.setLayout(main_layout)    
        self.setCentralWidget(container1)
        
      
    def item_clicked(self, item):
        self.list_widget.data(Qt.UserRole)
        self.lineedit13.setText(Qt.UserRole, self.lineedit13.text())
        

    def selectall():
        jointslist = []
        jointslist.append('ctrl_hip')
        #all = pm.listRelatives('ctrl_hip')
        #selectalllist.append(all)
        jointslist.append('locator1')
        jointslist.append('locator2')
        jointslist.append('locator3')
        jointslist.append('locator4')
        jointslist.append('IKcontrol_IK_left_arm1')
        jointslist.append('IKcontrol_IK_left_leg1')
        jointslist.append('IKcontrol_IK_right_arm1')
        jointslist.append('IKcontrol_IK_right_leg1')

    def importAnim(self):
        text = self.list_widget.currentItem().text()
        filefolder = glob.glob('/Users/**/Documents/maya/projects/default/assets')
        fileloc = os.path.join(filefolder[0], text)
        print("filelocation: " + fileloc)
        with open(fileloc) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                #joints = cmds.select(key)
                print(key)
                translateX = cmds.setAttr(key + ".translateX",  value[0])
                translateY = cmds.setAttr(key + ".translateY",  value[1])
                #translateZ = cmds.setAttr(key + ".translateZ",  value[2])
                rotateX = cmds.setAttr(key + ".rotateX", value[3])
                rotateY = cmds.setAttr(key + ".rotateY", value[4])
                rotateZ = cmds.setAttr(key + ".rotateZ", value[5])
       
    def exportAnim(self):
       
        pm.playblast(viewer=True, format="image", frame=1, f="myMovie.mv")
      
        '''
        filefolder = "/Users/aniediumoren/Movies"
        files = os.listdir("/Users/aniediumoren/Movies")
  
        paths = [os.path.join("/Users/aniediumoren/Movies", basename) for basename in files]
        latest = max(paths, key=os.path.getctime)
        icon = QIcon(latest)
        size = QSize(300, 300)
        self.list_widget.setIconSize(size)
        '''
        filefolder = glob.glob("/Users/**/Documents/maya/projects/default/images/myMovie.mv.*")
        #/Users/aniediumoren/Documents/maya/projects/default/images/myMovie.mv.0000.png
        print(filefolder)
            
        latest = max(filefolder, key=os.path.getmtime)
        print(latest)
        
        icon = QIcon(latest)
        size = QSize(200, 200)
        self.list_widget.setIconSize(size)


        print(self.layout1.itemAt(1).widget().text())
        print(self.layout1.itemAt(3).widget().text())
        print(self.layout1.itemAt(5).widget().text())
        
        

        

        item = QListWidgetItem(icon, self.layout1.itemAt(1).widget().text())
        self.list_widget.addItem(item)
        item.setData(Qt.ToolTipRole, self.layout1.itemAt(3).widget().text())
        item.setData(Qt.UserRole, self.layout1.itemAt(5).widget().text())
        jointslist = cmds.ls(type="joint")
        joints = []
        values = []
        print(jointslist)
    
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
        print(res)
        #fix
       
        fil = glob.glob('/Users/**/Documents/maya/projects/default/assets')
        fileloc = os.path.join(fil[0], self.layout1.itemAt(1).widget().text())
        print("export filelocation:")
        with open(fileloc, 'w') as fp:
            json.dump(res, fp)
        
   
if __name__ == "__main__":
    app = QApplication.instance()

    window = MainWindow()
    window.show()

    app.exec_()