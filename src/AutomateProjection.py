'''
Sep 11, 2023
author: Anahita A. Seresti
The goal of this script is to take a folder containing the VTI images and another one containing
the VTU mesh segmented from the images on SimVascular and projects the images into the mesh using
ProjectImageToMesh script.
The script is developed for MR Flow Assessment solely. In this project the image dataset is divided
into five subsets and there is only one segmentation for each subset.
'''
from ProjectImageToMesh import ImageAnalysisProjectImageToMesh
import argparse
import glob
import os
class AutomateProjection():
    def __init__(self,args):
        self.Args = args
    def main(self):
        ImageFileNames = glob.glob(f'{self.Args.InputImageFolder}/*.vti')
        ImageFileNames = sorted(ImageFileNames)
        NImage = len(ImageFileNames)
        MeshFileName = glob.glob(f'{self.Args.InputMeshFolder}/*.vtu')
        MeshFileName = sorted(MeshFileName)
        NMesh = len(MeshFileName)
        NSubset = NImage/NMesh
        counter = 0
        for Image in ImageFileNames:
            self.Args.InputFileName1 = Image
            self.Args.InputFileName2 = MeshFileName[int(counter/NSubset)]
            print(f"***** Projecting {Image} into {MeshFileName[int(counter/NSubset)]}")
            projection = ImageAnalysisProjectImageToMesh(self.Args)
            projection.Main()
            counter += 1
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script takes a folder containing vti images and a folder containing vtu meshes to extract the image dataset on vtu meshes")
    parser.add_argument("-InputImageFolder", "--InputImageFolder", required= True, dest="InputImageFolder", type=str, help="Input the folder containing the vti format of 4DFlow MRI")        
    parser.add_argument("-InputMeshFolder", "--InputMeshFolder", required=True, dest="InputMeshFolder", type=str, help="Input the volumetric mesh segmented from 4DFlow Datasets")
    args = parser.parse_args()
    AutomateProjection(args).main()