import vtk
import numpy as np
from utilities import vtk_to_numpy, numpy_to_vtk
from pathlib import Path
from glob import glob
import argparse
from utilities import *
class ImageAnalysisProjectImageToMesh():
	def __init__(self,Args):
		self.Args=Args
	def Main(self):
		OutputFileName = f"{Path(self.Args.InputFileName1).stem}{Path(self.Args.InputFileName2).suffix}"
		#Read the source data
		print ("--- Loading the source data: %s"%self.Args.InputFileName1)
		if self.Args.InputFileName1[-4:]==".vti":
			SourceData=ReadVTIFile(self.Args.InputFileName1)
		elif self.Args.InputFileName1[-4:]==".vtu":
			SourceData=ReadVTUFile(self.Args.InputFileName1)     
		elif self.Args.InputFileName1[-4:]==".vtp":
			SourceData=ReadVTPFile(self.Args.InputFileName1) 
		else:
			print ("Input file format not detected. Exiting...")
			exit(1)
		print ("--- Loading the target volume/surface mesh: %s"%self.Args.InputFileName2)         
		if self.Args.InputFileName2[-4:]==".vtu":
			TargetData=ReadVTUFile(self.Args.InputFileName2)
		elif self.Args.InputFileName2[-4:]==".vtp":
			TargetData=ReadVTPFile(self.Args.InputFileName2)
		else:
			print ("Target mesh format not detected. Exiting...")
			exit(1)	
		print ("--- Create a probe filter to interpolate source to target")
		ProbeFilter=vtk.vtkProbeFilter()
		ProbeFilter.SetInputData(TargetData)
		ProbeFilter.SetSourceData(SourceData)
		ProbeFilter.PassPointArraysOn()
		ProbeFilter.Update()
		ProbeOutput=ProbeFilter.GetOutput()
		print ("--- Write the output file in the same format as target data")
		WriteVTUFile(OutputFileName,ProbeOutput)		
if __name__=="__main__":
        #Description
	parser = argparse.ArgumentParser(description="This script will extract the image intensities and interpolate them onto a volumetric mesh.")
	parser.add_argument('-InputFileName1', '--InputFileName1', type=str, required=True, dest="InputFileName1",help="File name of the source data")
	#parser.add_argument('-ArrayName', '--ArrayName', type=str, required=False, dest="scalars",help="The array name that contains the image intensitites.")
	#Input filename of the coronary segmented surface.
	parser.add_argument('-InputFileName2', '--InputMesh', type=str, required=True, dest="InputFileName2",help="File name of the input mesh/surface on which to project from the source data")
	#parser.add_argument('-OutputFileName', '--OutputFileName', type=str, required=False, dest="OutputFileName",help="File name in which to store the image intensitites.")
	args=parser.parse_args()
	ImageAnalysisProjectImageToMesh(args).Main()

