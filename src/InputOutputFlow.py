'''
Sep 06, 2023
author: Anahita Seresti
The goal of this script is to take the vessel in several time steps and plot
in and out flow
'''
import vtk
import numpy as np
import glob
import argparse
import matplotlib.pyplot as plt
from utilities import ReadVTUFile, vtk_to_numpy, WriteVTUFile
class InOutFlow():
    def __init__(self,args):
        self.Args = args
    def sphereClipp(self,R,C,section,inout):
        # definning the vtk sphere object for clipping 
        Sphere = vtk.vtkSphere()
        Sphere.SetCenter(C)
        Sphere.SetRadius(R*0.8)
        # Setting the clipper on the input section
        clipper = vtk.vtkClipDataSet()
        clipper.SetInputData(section)
        clipper.SetClipFunction(Sphere)
        clipper.InsideOutOn()
        clipper.Update()
        # Writing the section as a VTU format
        WriteVTUFile(f"./clipper/{inout}.vtu", clipper.GetOutput())
        # Returning Averaged Pixel Magnitude and Averaged Velocity Magnitude across teh cross section
        array1 = clipper.GetOutput().GetPointData().GetArray(0)
        array1 = vtk_to_numpy(array1)
        PixelMag = np.average(array1)
        array2 = clipper.GetOutput().GetPointData().GetArray(1)
        array2 = vtk_to_numpy(array2)
        print(array2)
        return PixelMag, array2

    def main(self):
        # Read VTU files inside the given folder and store them in a dictionary
        filenames = glob.glob(f"{self.Args.InputFolder}/*.vtu")
        filenames = sorted(filenames)
        N = len(filenames)
        InputMesh = {i:ReadVTUFile(filenames[i]) for i in range(N)}
        # Getting the length of the vessel
        min_val = InputMesh[0].GetBounds()[4]
        max_val = InputMesh[0].GetBounds()[5]
        print(min_val, max_val)
        # Slicing with a plane in Z axis
        normal = (0., 0., 1.)
        plane = vtk.vtkPlane()
        plane.SetNormal(normal)
        interval = (max_val - min_val)/20
        #print(interval)
        plane.SetOrigin(0., 0., min_val + 7*interval)
        slicer = vtk.vtkExtractGeometry()
        slicer.SetExtractInside(1)
        slicer.ExtractBoundaryCellsOn()
        slicer.SetImplicitFunction(plane)
        # Calculating in-flow
        inflow = []
        for item in InputMesh:
            slicer.SetInputData(InputMesh[item])
            slicer.Update()
            slicer = slicer.GetOutput()
            Rx = slicer.GetBounds()[1] - slicer.GetBounds()[0]
            CenterX = (slicer.GetBounds()[1] + slicer.GetBounds()[0])/2
            CenterY = (slicer.GetBounds()[3] + slicer.GetBounds()[2])/2
            CenterZ = (slicer.GetBounds()[5] + slicer.GetBounds()[4])/2
            C = (CenterX, CenterY, CenterZ)
            [PixelMag, VelocityArray] = InOutFlow(self.Args).sphereClipp(abs(Rx),C,slicer,"inflow")
            array_ = slicer.GetPointData().GetArray(0)
            array_ = vtk_to_numpy(array_)
            inflow.append(np.average(array_))
            print(PixelMag, array_)
            print(VelocityArray)
            exit(1)
        outflow = []
        plane.SetOrigin(0., 0., max_val - 7*interval)
        for item in InputMesh:
            slicer.SetInputData(InputMesh[item])
            slicer.Update()
            array_ = slicer.GetOutput().GetPointData().GetArray(0)
            array_ = vtk_to_numpy(array_)
            outflow.append(np.average(array_))
        outflow = np.array(outflow)
        plt.plot(inflow, 'green')
        plt.figure(1)
        plt.title(f"inflow at z = {round((min_val + interval)*100)/100}")
        plt.figure(2)
        plt.plot(outflow, 'red')
        plt.title(f"outflow at z = {round((max_val - interval)*100)/100}")
        plt.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-InputFolder", "--InputFolder", type=str, required=True, dest="InputFolder", help="Folder containing vtk files")
    args = parser.parse_args()
    InOutFlow(args).main()