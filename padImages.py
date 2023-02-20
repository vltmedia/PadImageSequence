"""
Iterate through a directory and add images missing to the start and end of the sequence using a template file to pad with. Useful for filling in CG sequences to save time on rendering.

"""

import os
import glob
import shutil
import argparse

# setup the argument parser
parser = argparse.ArgumentParser(description='Add images to a directory')
parser.add_argument('-i', '--input', type=str, required=True, help='Source directory')
parser.add_argument('-o', '--output', type=str, required=True, help='Output directory')
parser.add_argument('-f', '--filenameTemplate',required=True,  help='The filename template to use. Use # for the frame number')
parser.add_argument('-t', '--template', type=str, required=True, help='Template image to pad with')
parser.add_argument('-s', '--startFrame', type=int, default=1000, help='Start Frame')
parser.add_argument('-e', '--endFrame', type=int, default=1120, help='End Frame')
parser.add_argument('-z', '--zPadding', type=int, default=4, help='How many 0s to pad with')

# parse the arguments
args = parser.parse_args()


class ImagePadding():
    def __init__(self, input, output, filenameTemplate, template, startFrame, endFrame, zPadding):
        self.files = []
        self.topPad = []
        self.bottomPad = []
        self.min = 0
        self.max = 10
        self.input = input
        self.output = output
        self.filenameTemplate = filenameTemplate
        self.template = template
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.zPadding = zPadding

    def parseNumber(self, fppath):
        # parse the zero padded number in the filename fppath
        fp = os.path.basename(fppath)
        splf = self.filenameTemplate.split("#")
        numba = fp.replace(splf[1], "").replace(splf[0], "")
        return int(numba)

    def getMinMax(self, files):
        # get the min and max frame numbers
        return min([f["number"] for f in files]), max([f["number"] for f in files])

    def getPaddingData(self):
        # get files that match the template
        self.files = [{"filepath":f, "number":self.parseNumber(f), "original" : True, "template":""} for f in  glob.glob(self.input + "/"+ self.filenameTemplate.replace("#","*")) ]
        self.min = self.getMinMax(self.files)[0]
        self.max = self.getMinMax(self.files)[1]
        if self.min > self.startFrame :
            topPad = self.min - self.startFrame  
        else:
            topPad = 0
        if self.max < self.endFrame :
            bottomPad = self.endFrame - self.max   
        else:
            bottomPad = 0
        topPadFiles = []
        bottomPadFiles = []

        for add in range(topPad):
            topPadFiles.append({"filepath":self.output + "/" +self.filenameTemplate.replace("#", str(self.startFrame+ add).zfill(self.zPadding)), "number":self.startFrame + add, "original" : False, "template":self.template})
        for add in range(bottomPad):
            bottomPadFiles.append({"filepath":self.output + "/" +self.filenameTemplate.replace("#", str(self.endFrame- add).zfill(self.zPadding)), "number":self.endFrame - add, "original" : False, "template":self.template})
            
        self.topPad = topPadFiles
        self.bottomPad = bottomPadFiles

    def processData(self):
        self.getPaddingData()
        
    def runPadding(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        for file in self.topPad:
            # copy the template file to the output directory with shutil
            shutil.copy(file["template"], file["filepath"])
        for file in self.bottomPad:
            shutil.copy(file["template"], file["filepath"])

if __name__ == "__main__":
    # run the script
    ip = ImagePadding(args.input, args.output, args.filenameTemplate, args.template, args.startFrame, args.endFrame, args.zPadding)
    ip.processData()
    ip.runPadding()
    f = 0

