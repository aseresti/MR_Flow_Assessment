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
from math import sqrt, pi
from utilities import ReadVTUFile, vtk_to_numpy, WriteVTUFile
class InOutFlow():
    def __init__(self,args):
        self.Args = args
    def sphereClipp(self,R,C,section):
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
        #WriteVTUFile(f"./clipper/{inout}.vtu", clipper.GetOutput())
        # Returning Averaged Pixel Magnitude and Averaged Velocity Magnitude across teh cross section
        array1 = clipper.GetOutput().GetPointData().GetArray("MagnitudeSequence")
        array1 = vtk_to_numpy(array1)
        PixelMag = np.average(array1)
        array2 = clipper.GetOutput().GetPointData().GetArray("Velocity")
        array2 = vtk_to_numpy(array2)
        VelocityMag = np.array([sqrt(item[0]**2+item[1]**2+item[2]**2) for item in array2])
        VelocityMag = np.average(VelocityMag)
        return PixelMag, VelocityMag
    def main(self):
        # Read VTU files inside the given folder and store them in a dictionary
        filenames = glob.glob(f"{self.Args.InputFolder}/*.vtu")
        filenames = sorted(filenames)
        N = len(filenames)
        InputMesh = {i:ReadVTUFile(filenames[i]) for i in range(N)}
        # Getting the length of the vessel
        min_val = InputMesh[0].GetBounds()[4]
        max_val = InputMesh[0].GetBounds()[5]
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
        inflowMag = []
        inflowVel = []
        for item in InputMesh:
            slicer.SetInputData(InputMesh[item])
            slicer.Update()
            slicer_ = slicer.GetOutput()
            Rx = (slicer_.GetBounds()[1] - slicer_.GetBounds()[0])/2
            Area = pi*pow(Rx,2)
            CenterX = (slicer_.GetBounds()[1] + slicer_.GetBounds()[0])/2
            CenterY = (slicer_.GetBounds()[3] + slicer_.GetBounds()[2])/2
            CenterZ = (slicer_.GetBounds()[5] + slicer_.GetBounds()[4])/2
            C = (CenterX, CenterY, CenterZ)
            [PixelMag, VelocityMag] = InOutFlow(self.Args).sphereClipp(abs(Rx),C,slicer_)
            inflowMag.append(Area*PixelMag)
            inflowVel.append(Area*VelocityMag)
        outflowMag = []
        outflowVel = []
        plane.SetOrigin(0., 0., max_val - 6*interval)
        for item in InputMesh:
            slicer.SetInputData(InputMesh[item])
            slicer.Update()
            slicer_ = slicer.GetOutput()
            Rx = (slicer_.GetBounds()[1] - slicer_.GetBounds()[0])/2
            Area = pi*pow(Rx,2)
            CenterX = (slicer_.GetBounds()[1] + slicer_.GetBounds()[0])/2
            CenterY = (slicer_.GetBounds()[3] + slicer_.GetBounds()[2])/2
            CenterZ = (slicer_.GetBounds()[5] + slicer_.GetBounds()[4])/2
            C = (CenterX, CenterY, CenterZ)
            [PixelMag, VelocityMag] = InOutFlow(self.Args).sphereClipp(abs(Rx),C,slicer_)
            outflowMag.append(Area*PixelMag)
            outflowVel.append(Area*VelocityMag)
        #outflow = np.array(outflow)
        plt.figure(1)
        plt.plot(inflowMag, 'green')
        plt.plot(outflowMag, 'red')
        plt.legend([f"inflow at z = {round((min_val + 7*interval)*100)/100}",f"outflow at z = {round((max_val - 6*interval)*100)/100}"])
        plt.title("Pixel Magnitude Across the Cross Section: Wall Excluded")
        plt.figure(2)
        plt.plot(inflowVel, 'green')
        plt.plot(outflowVel, 'red')
        plt.legend([f"inflow at z = {round((min_val + 7*interval)*100)/100}",f"outflow at z = {round((max_val - 6*interval)*100)/100}"])
        plt.title("Velocity Magnitude Across the Cross Section: Wall Included")
        plt.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-InputFolder", "--InputFolder", type=str, required=True, dest="InputFolder", help="Folder containing vtk files")
    args = parser.parse_args()
    InOutFlow(args).main()