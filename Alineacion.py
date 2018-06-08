from __main__ import vtk, qt, ctk, slicer #Se cargan las diferentes librerias

import logging
import os
import unittest
import math
import numpy as np
from slicer.ScriptedLoadableModule import*


##Esta clase ayuda a que la interfaz aparezca en los modulos de slicer.
class Alineacion:
    def __init__(self,parent):
        parent.title = "Registro de volumenes"
        parent.categories = ["Imagenes"]
        parent.contributors = ["Daniel Gomez",
                               "Isabel Lopez",
                               "Andres Lopez"]
        
        parent.helpText = """Esta interfaz permite seleccionar el tipo de registro a realizar a todas los volumenes usando como volumen fijo el primer
    volumen del 4D, ademas indica cuales volumenes tienen un movimiento mayor a 4 mm en cualquier direccion. """

        parent.acknowledgementText = """
        """
        self.parent = parent

        
## Esta clase son los botones para los registros
class AlineacionWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()
                 

  def setup(self):
    # button
    self.alineacionCollapsibleButton = ctk.ctkCollapsibleButton() #cabezal del lugar donde estan las opciones
    self.alineacionCollapsibleButton.text = "Operaciones" # nombre del cabezal
    self.layout.addWidget(self.alineacionCollapsibleButton)
    # Layout within the laplace collapsible button
    self.alineacionFormLayout = qt.QFormLayout(self.alineacionCollapsibleButton)
    #The volume selector
    self.inputFrame = qt.QFrame(self.alineacionCollapsibleButton)
    self.inputFrame.setLayout(qt.QHBoxLayout())
    self.alineacionFormLayout.addWidget(self.inputFrame)
    self.inputSelector = qt.QLabel("Volumen 4D: ", self.inputFrame)
    self.inputFrame.layout().addWidget(self.inputSelector)
    self.inputSelector = slicer.qMRMLNodeComboBox(self.inputFrame)
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputFrame.layout().addWidget(self.inputSelector)

   #Boton para Alineacion rigida
    alineacionButton = qt.QPushButton(" Aplicar Rigido")#Nombre del boton
    alineacionButton.toolTip = "Aplicar alineacion rigida."#Mensaje que sale si se coloca el cursor encima del boton
    self.alineacionFormLayout.addWidget(alineacionButton)
    alineacionButton.connect('clicked(bool)', self.rigido) #Permite dar click y dirigirse a la funcion correspondiente
   # buttonfiltro
    self.alineacionCollapsibleButton = ctk.ctkCollapsibleButton() #cabezal del lugar donde estan las opciones
    self.alineacionCollapsibleButton.text = "Aplicacion del filtro" # nombre del cabezal
    self.layout.addWidget(self.alineacionCollapsibleButton)
    # Layout within the laplace collapsible button
    self.alineacionFormLayout = qt.QFormLayout(self.alineacionCollapsibleButton)
    #The volume selector
    self.inputFrame = qt.QFrame(self.alineacionCollapsibleButton)
    self.inputFrame.setLayout(qt.QHBoxLayout())
    self.alineacionFormLayout.addWidget(self.inputFrame)
    self.inputSelector3 = qt.QLabel("Volumen: ", self.inputFrame)
    self.inputFrame.layout().addWidget(self.inputSelector3)
    self.inputSelector3 = slicer.qMRMLNodeComboBox(self.inputFrame)
    self.inputSelector3.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector3.addEnabled = False
    self.inputSelector3.removeEnabled = False
    self.inputSelector3.setMRMLScene( slicer.mrmlScene )
    self.inputFrame.layout().addWidget(self.inputSelector3)
   #Boton para filtro
    filtroButton = qt.QPushButton(" Aplicar Filtro")#Nombre del boton
    filtroButton.toolTip = "Aplicar alineacion rigida."#Mensaje que sale si se coloca el cursor encima del boton
    self.alineacionFormLayout.addWidget(filtroButton)
    filtroButton.connect('clicked(bool)', self.filtro) #Permite dar click y dirigirse a la funcion correspondiente



# button
    self.alineacionCollapsibleButton = ctk.ctkCollapsibleButton() #cabezal del lugar donde estan las opciones
    self.alineacionCollapsibleButton.text = "Seleccion ROI" # nombre del cabezal
    self.layout.addWidget(self.alineacionCollapsibleButton)
    # Layout within the laplace collapsible button
    self.alineacionFormLayout = qt.QFormLayout(self.alineacionCollapsibleButton)
    #The volume selector
    self.inputFrame = qt.QFrame(self.alineacionCollapsibleButton)
    self.inputFrame.setLayout(qt.QHBoxLayout())
    self.alineacionFormLayout.addWidget(self.inputFrame)
    self.inputSelector4 = qt.QLabel("ROI: ", self.inputFrame)
    self.inputFrame.layout().addWidget(self.inputSelector4)
    self.inputSelector4 = slicer.qMRMLNodeComboBox(self.inputFrame)
    self.inputSelector4.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector4.addEnabled = False
    self.inputSelector4.removeEnabled = False
    self.inputSelector4.setMRMLScene( slicer.mrmlScene )
    self.inputFrame.layout().addWidget(self.inputSelector4)

    #The volume selector
    self.inputFrame2 = qt.QFrame(self.alineacionCollapsibleButton)
    self.inputFrame2.setLayout(qt.QHBoxLayout())
    self.alineacionFormLayout.addWidget(self.inputFrame2)
    self.inputSelector2 = qt.QLabel("Volumen: ", self.inputFrame2)
    self.inputFrame2.layout().addWidget(self.inputSelector2)
    self.inputSelector2 = slicer.qMRMLNodeComboBox(self.inputFrame2)
    self.inputSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector2.addEnabled = False
    self.inputSelector2.removeEnabled = False
    self.inputSelector2.setMRMLScene( slicer.mrmlScene )
    self.inputFrame2.layout().addWidget(self.inputSelector2)

   #Boton para Roi
    alineacionButton = qt.QPushButton(" Aplicar ROI")#Nombre del boton
    alineacionButton.toolTip = "Aplicar alineacion rigida."#Mensaje que sale si se coloca el cursor encima del boton
    self.alineacionFormLayout.addWidget(alineacionButton)
    alineacionButton.connect('clicked(bool)', self.region) #Permite dar click y dirigirse a la funcion correspondiente
#INTENSIDAD Vs TIEMPO
    #BOTON
    self.alineacionCollapsibleButton = ctk.ctkCollapsibleButton() #cabezal del lugar donde estan las opciones
    self.alineacionCollapsibleButton.text = "Graficar" # nombre del cabezal
    self.layout.addWidget(self.alineacionCollapsibleButton)
    # LAYOUT
    self.alineacionFormLayout = qt.QFormLayout(self.alineacionCollapsibleButton)


    self.inputFrame = qt.QFrame(self.alineacionCollapsibleButton)
    self.inputFrame.setLayout(qt.QHBoxLayout())
    self.alineacionFormLayout.addWidget(self.inputFrame)
    self.inputSelector5 = qt.QLabel("Volgraficar: ", self.inputFrame)
    self.inputFrame.layout().addWidget(self.inputSelector5)
    self.inputSelector5 = slicer.qMRMLNodeComboBox(self.inputFrame)
    self.inputSelector5.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector5.addEnabled = False
    self.inputSelector5.removeEnabled = False
    self.inputSelector5.setMRMLScene( slicer.mrmlScene )
    self.inputFrame.layout().addWidget(self.inputSelector5)
    #BOTON GRAFICAR TIEMPO
    alineacionButton = qt.QPushButton(" Graficar")#Nombre del boton
    alineacionButton.toolTip = " Graficar."#Mensaje que sale si se coloca el cursor encima del boton
    self.alineacionFormLayout.addWidget(alineacionButton)
    alineacionButton.connect('clicked(bool)', self.grafTiempo)
    # Add vertical spacer
    self.layout.addStretch(2)

    # Set local var as instance attribute
    self.alineacionButton = alineacionButton

    
    
    
			#Funcion para alineacion afin
  def rigido(self):
        
        escena = slicer.mrmlScene; #Se recupera la escena cargada
        volumen4D = self.inputSelector.currentNode()
        imagenvtk4D = volumen4D.GetImageData()
        
        extract1 = vtk.vtkImageExtractComponents()
        extract1.SetInputData(imagenvtk4D)
        imagen_fija = extract1.SetComponents(0)  
        extract1.Update()
        #Matriz de transformacion
        ras2ijk = vtk.vtkMatrix4x4()
        ijk2ras = vtk.vtkMatrix4x4()

        #Se solicita al volumen original que devuelva las matrices
        volumen4D.GetRASToIJKMatrix(ras2ijk)
        volumen4D.GetIJKToRASMatrix(ijk2ras)

        #Se crea un volumen nuevo
        volumenFijo = slicer.vtkMRMLScalarVolumeNode();
        #Se asignan las transformaciones
        volumenFijo.SetRASToIJKMatrix(ras2ijk)
        volumenFijo.SetIJKToRASMatrix(ijk2ras)
        #Se asigna el volumen 3D 
        volumenFijo.SetAndObserveImageData(extract1.GetOutput())
        escena.AddNode(volumenFijo)
        
        numero_imagenes = volumen4D.GetNumberOfFrames()
        valor1=[];# vector donde se guarda los valores de LR despues aplicar la transformada rigida
        valor2=[];# vector donde se guarda los valores de PA despues aplicar la transformada rigida
        valor3=[];# vector donde se guarda los valores de IS despues aplicar la transformada rigida
        vecvolmay=[]; # vector que muestra el frame, los volumenes que tienen un movimiento mayor a 4 mm
        valor1.append(0)
        valor2.append(0)
        valor3.append(0)
       

              
       
       #En esta parte se evaluan todos los volumenes moviles
        for i in range(0, numero_imagenes, 1):
			#extraer la imagen movil
            extract2 = vtk.vtkImageExtractComponents()
            extract2.SetInputData(imagenvtk4D)
            imagen_movil = extract2.SetComponents(i)
            extract2.Update()

            
            
            #Se crea un volumen movil, y se realiza el mismo procedimiento que con el fijo
            volumenMovil = slicer.vtkMRMLScalarVolumeNode();

            volumenSalida = slicer.vtkMRMLScalarVolumeNode();
            escena.AddNode(volumenSalida)
            volumenMovil.SetRASToIJKMatrix(ras2ijk)
            volumenMovil.SetIJKToRASMatrix(ijk2ras)
            volumenMovil.SetAndObserveImageData(extract2.GetOutput())
            escena.AddNode(volumenMovil)
            
            
            #Se crea la transformada para alinear los volumenes
            transformadaSalida = slicer.vtkMRMLLinearTransformNode() 
            transformadaSalida.SetName('Transformada de registro rigido'+str(i)) #se le da un nombre especifico a la transformada
            slicer.mrmlScene.AddNode(transformadaSalida)
            
            
            

            parameters = {}
            parameters['fixedVolume'] = volumenFijo.GetID()
            parameters['movingVolume'] = volumenMovil.GetID()
            parameters['transformType'] = 'Rigid' #Se coloca segun lo que se quiera hacer si rigido, afin o bspline
            parameters['outputTransform'] = transformadaSalida.GetID()
            parameters['outputVolume'] = volumenSalida.GetID()

            cliNode = slicer.cli.run( slicer.modules.brainsfit,None,parameters, wait_for_completion=True)
            slicer.util.saveNode(volumenSalida,'volumenrigido'+str(i+1)+'.nrrd') #se guarda el volumen registrado en la carpeta de documentos


    # Este for se hace con el fin de ver los volumenes que tienen un desplazamiento mayor a 4 mm con respecto al fijo
        for i in range (0,numero_imagenes):
            nodo = escena.GetNodesByName('Transformada de registro rigido'+str(i))
            nodo = nodo.GetItemAsObject(0)
            matriztransformada=nodo.GetMatrixTransformToParent() # Se obtiene la matriz de transformacion
      
      # se obtiene para cada frame la ubicacion en las 3 direcciones
            valor1inicial=matriztransformada.GetElement(0,3) #se agrega el valor en la posicion 0 3 de la transformada valor que corresponde a LR
            valor2inicial=matriztransformada.GetElement(1,3)#se agrega el valor en la posicion 0 3 de la transformada valor que corresponde a PA
            valor3inicial=matriztransformada.GetElement(2,3)#se agrega el valor en la posicion 0 3 de la transformada valor que corresponde a IS
            valor1.append(valor1inicial)
            valor2.append(valor2inicial)
            valor3.append(valor3inicial)
      # Si la posicion en cualquier direccion de un volumen es mayor a 4mm respecto al del primer frame se obtiene un vector con su posicion
            if ((abs(valor1[i])>4) or (abs(valor2[i])>4) or (abs(valor3[i])>4)):
              vecvolmay.append(i)  

        print("Los volumenes con los que se mueve mas de 4mm son")
        print("Volumen")
        print(vecvolmay)
        if (len(vecvolmay)==0): # Si no hay alguni no se muestra nada
          print("Ningun volumen se movio mas de 4mm")
    

  def filtro(self):
        
        escenafiltro = slicer.mrmlScene; #Se recupera la escena cargada
        volumen4Dfiltro = self.inputSelector3.currentNode()
        imagenvtk4Dfiltro = volumen4Dfiltro.GetImageData()
        numero_imagenes = volumen4Dfiltro.GetNumberOfFrames()
        for i in range(0, numero_imagenes, 1):
            #extraer la imagen movil
            extract2 = vtk.vtkImageExtractComponents()
            extract2.SetInputData(imagenvtk4Dfiltro)
            extract2.SetComponents(i)
            extract2.Update()	
            filtroGaussiano = vtk.vtkImageGaussianSmooth()

            filtroGaussiano.SetStandardDeviation(1,1,1)
            filtroGaussiano.SetInputData(extract2.GetOutput())
            filtroGaussiano.Update();

            ras2ijk = vtk.vtkMatrix4x4()
            ijk2ras = vtk.vtkMatrix4x4()

            volumen4Dfiltro.GetRASToIJKMatrix(ras2ijk)
            volumen4Dfiltro.GetIJKToRASMatrix(ijk2ras)

            volSalida = slicer.vtkMRMLScalarVolumeNode()
            volSalida.SetAndObserveImageData(filtroGaussiano.GetOutput())

            volSalida.SetRASToIJKMatrix(ras2ijk)
            volSalida.SetIJKToRASMatrix(ijk2ras)
            slicer.mrmlScene.AddNode(volSalida)
            
            slicer.util.saveNode(volSalida,'filtrado'+str(i+1)+'.nrrd') #se guarda el volumen registrado en la carpeta de documentos
            print("ya filtre"+str(i))
 
  def region(self):
        escena = slicer.mrmlScene; #Se recupera la escena cargada
        volumen4D = self.inputSelector4.currentNode()
        imagenvtk4D = volumen4D.GetImageData()
        
        extract1 = vtk.vtkImageExtractComponents()
        extract1.SetInputData(imagenvtk4D)
        imagen_fija = extract1.SetComponents(0)  
        extract1.Update()
        #Matriz de transformacion
        ras2ijk = vtk.vtkMatrix4x4()
        ijk2ras = vtk.vtkMatrix4x4()

        #Se solicita al volumen original que devuelva las matrices
        volumen4D.GetRASToIJKMatrix(ras2ijk)
        volumen4D.GetIJKToRASMatrix(ijk2ras)

        #Se crea un volumen nuevo
        volumenFijo = slicer.vtkMRMLScalarVolumeNode();
        #Se asignan las transformaciones
        volumenFijo.SetRASToIJKMatrix(ras2ijk)
        volumenFijo.SetIJKToRASMatrix(ijk2ras)
        #Se asigna el volumen 3D 
        volumenFijo.SetAndObserveImageData(extract1.GetOutput())
        escena.AddNode(volumenFijo)
		
        escena = slicer.mrmlScene; #Se recupera la escena cargada
        volumen4D = self.inputSelector2.currentNode()
        imagenvtk4D = volumen4D.GetImageData()
        numero_imagenes = volumen4D.GetNumberOfFrames()
		
		
        for i in range(0, numero_imagenes, 1):
		
            extract2 = vtk.vtkImageExtractComponents()
            extract2.SetInputData(imagenvtk4D)
            imagen_movil = extract2.SetComponents(i)
            extract2.Update()
            #Matriz de transformacion
            ras2ijk = vtk.vtkMatrix4x4()
            ijk2ras = vtk.vtkMatrix4x4()

        #Se solicita al volumen original que devuelva las matrices
            volumen4D.GetRASToIJKMatrix(ras2ijk)
            volumen4D.GetIJKToRASMatrix(ijk2ras)
            #Se crea un volumen movil, y se realiza el mismo procedimiento que con el fijo
            volumenMovil = slicer.vtkMRMLScalarVolumeNode();
            
            vol = slicer.vtkMRMLScalarVolumeNode();
            vol.SetName('salida') 
            escena.AddNode(vol)

            volumenMovil.SetRASToIJKMatrix(ras2ijk)
            volumenMovil.SetIJKToRASMatrix(ijk2ras)
            volumenMovil.SetAndObserveImageData(extract2.GetOutput())
            escena.AddNode(volumenMovil)
         #parametros para la operacion de registro
            parameters = {}
            parameters['inputVolume1'] = volumenFijo.GetID() #dos volumenes de la escena, uno de ellos debe ser la mascara creada en el EDITOR
            parameters['inputVolume2'] = volumenMovil.GetID()
            parameters['outputVolume'] = vol;
            cliNode = slicer.cli.run( slicer.modules.multiplyscalarvolumes,None,parameters, wait_for_completion=True)
            slicer.util.saveNode(vol,'roi'+str(i+1)+'.nrrd') #se guarda el volumen registrado en la carpeta de documentos
		   

  def grafTiempo(self):
    # Switch to a layout (24) that contains a Chart View to initiate the construction of the widget and Chart View Node
    lns = slicer.mrmlScene.GetNodesByClass('vtkMRMLLayoutNode')
    lns.InitTraversal()
    ln = lns.GetNextItemAsObject()
    ln.SetViewArrangement(24)
    vectorintensidad=[]
    # Get the Chart View Node
    cvns = slicer.mrmlScene.GetNodesByClass('vtkMRMLChartViewNode')
    cvns.InitTraversal()
    cvn = cvns.GetNextItemAsObject()

# Create an Array Node and add some data
    dn = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
    a = dn.GetArray()
    a.SetNumberOfTuples(27)
	
	#Volumen
    escena = slicer.mrmlScene; #Se recupera la escena cargada
    volumen4D = self.inputSelector5.currentNode()
    imagenvtk4D = volumen4D.GetImageData()
    numero_imagenes = volumen4D.GetNumberOfFrames()
		
		
    for i in range(0, numero_imagenes, 1):
		
        extract2 = vtk.vtkImageExtractComponents()
        extract2.SetInputData(imagenvtk4D)
        imagen_movil = extract2.SetComponents(i)
        extract2.Update()
        #Matriz de transformacion
        ras2ijk = vtk.vtkMatrix4x4()
        ijk2ras = vtk.vtkMatrix4x4()

        #Se solicita al volumen original que devuelva las matrices
        volumen4D.GetRASToIJKMatrix(ras2ijk)
        volumen4D.GetIJKToRASMatrix(ijk2ras)
        #Se crea un volumen movil, y se realiza el mismo procedimiento que con el fijo
        volumenMovil = slicer.vtkMRMLScalarVolumeNode();
            
        volumenMovil.SetRASToIJKMatrix(ras2ijk)
        volumenMovil.SetIJKToRASMatrix(ijk2ras)
        volumenMovil.SetAndObserveImageData(extract2.GetOutput())
        escena.AddNode(volumenMovil)
        z=slicer.util.arrayFromVolume(volumenMovil)
        m=np.mean(z[:])

        vectorintensidad.append((m/15000)-1)
        
	
        
    for i in range(0,numero_imagenes):
            a.SetComponent(i, 0, i*11.11)
            a.SetComponent(i, 1, vectorintensidad[i])
            a.SetComponent(i, 2, 0)



    # Create a Chart Node.
    cn = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

    # Add the Array Nodes to the Chart. The first argument is a string used for the legend and to refer to the Array when setting properties.
   

    # Set a few properties on the Chart. The first argument is a string identifying which Array to assign the property. 
    # 'default' is used to assign a property to the Chart itself (as opposed to an Array Node).
    cn.SetProperty('default', 'title', 'intesidad vs tiempo')
    cn.SetProperty('default', 'xAxisLabel', 'Tiempo(s)')
    cn.SetProperty('default', 'yAxisLabel', 'Intensidad')

    # Tell the Chart View which Chart to display
    cvn.SetChartNodeID(cn.GetID())


      

    
   

    
   


