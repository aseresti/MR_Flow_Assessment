'''
Sept 05, 2023
author: Anahita Seresti
The goal of the script is to take a folder of vtk format images 
and convert them to a vti format images all at once.
'''

import glob
import os
from pathlib import Path
import argparse

class ConvertVTKtoVTI():
    def __init__(self,args):
        self.Args = args
    def main(self):
        filenames = glob.glob(f'{self.Args.InputFolder}/*.vtk')
        filenames = sorted(filenames)
        count = 1
        for file in filenames:
            print(f"--- converting image number: {count}")
            ofile = Path(file).stem
            os.system(f"vmtkimagewriter -ifile {file} -ofile ./{ofile}.vti")
            count = count + 1
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="script takes a folder containing vtk images")
    parser.add_argument("-InputFolder", "--InputFolder", type=str, required=True, dest="InputFolder", help="Folder containing vtk files")
    args = parser.parse_args()
    ConvertVTKtoVTI(args).main()