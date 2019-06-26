#!/usr/bin/python3

import PySimpleGUI as sg  

sg.ChangeLookAndFeel('GreenTan')

print = sg.EasyPrint 

layout = [[sg.Text('Stamp numbers will be added automatically. Only put "Exhibit" in Line 3. Make sure you have numbered the original docs.')],      
            [sg.Text('Folder to be stamped (docs numbered 001, 002, ..)', size=(30, 2)), sg.InputText(), sg.FolderBrowse()],      
            [sg.Text('Folder to save stamped docs:', size=(30, 2)), sg.InputText(), sg.FolderBrowse()],      
            [sg.Text('1st line of stamp:', size=(30, 2)), sg.InputText()],
            [sg.Text('2nd line of stamp:', size=(30, 2)), sg.InputText()],
            [sg.Text('3rd line of stamp:', size=(30, 2)), sg.InputText()],
            [sg.Checkbox('Stamp all pages of pdf', size=(25,1), default=False)],
            [sg.Submit(), sg.Cancel()]] 


import fitz
import subprocess
from os import listdir
from os.path import isdir, isfile, join


window = sg.Window('Inputs', layout)
        
event, value_list = window.Read()  
input_path = value_list[0]      
output_path = value_list[1]
line_one = value_list[2]
line_two = value_list[3]
line_three = value_list[4]
stampall = value_list[5]
maxstring = max((len(line_one)), (len(line_two)),(len(line_three) + 4))
leftwidth = maxstring*7+26

from fitz.utils import getColor

yellow  = getColor("darkgoldenrod")
black   = getColor("black")
white   = getColor("white")
red     = getColor("red")
wood    = getColor("wheat2")
wood2 = getColor("wheat3")

#print("Enter full path to the file to be stamped:")

#input_path = input()

print("Stampall selected:", stampall)
print("Max length:", maxstring)

# stamps_path = input()

#print("\n Enter the full path to the OUTPUT folder:")

#output_path = input()

print("To be stamped folder: ", input_path, '\n' \
        #"Stamps file/folder: ", stamps_path, '\n' \
        "Output folder: ", output_path, '\n')

input_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

print("Input Files: ", input_files, '\n')


for i in input_files:

    doc = fitz.open(f"{input_path}/{i}")

    text = [f"{line_one}", f"{line_two}", f"{line_three} {i[:3]}"]                       

    if stampall == True:

        for page in doc:    

            r1 = fitz.Rect(page.rect.width - leftwidth, page.rect.height - 65, page.rect.width - 25, page.rect.height - 20) # directly define rectangle using page.rect
    
            # p2 = fitz.Point(page.rect.width - 25, page.rect.height - 25)      

            page.drawRect(r1, color=black, fill=white, overlay=True) # Draw first to give properties

            rc = page.insertTextbox(r1, text, color = black, align=1, fontname="Courier", border_width=2) 

        doc.save(f"{i}")

    else: 
    
        page = doc[0]

        text = [f"{line_one}", f"{line_two}", f"{line_three} {i[:3]}"]

            #r1 = fitz.Rect(400,750,550,800)   # rectangle (x0, y0, x1, y1) in pixels, bottom right For upper right try fitz.Rect(450,20,550,120)
    
        r1 = fitz.Rect(page.rect.width - leftwidth, page.rect.height - 65, page.rect.width - 25, page.rect.height - 20) 
    
            # p2 = fitz.Point(page.rect.width - 25, page.rect.height - 25)      

        page.drawRect(r1, color=black, fill=white, overlay=True) # Draw first to give properties

        rc = page.insertTextbox(r1, text, color = black, align=1, fontname="Courier", border_width=2) #Default : align=TEXT_ALIGN_LEFT (0) ; border_width=1 TEXT_ALIGN_CENTER 

    doc.save(f"{i}")                 

# Check usage for doc.name Runtime error: cannot open file 'stamped-/home/xxx/xxx/Original.pdf': No such file or directory


output_files = [f for f in listdir(".") if isfile(join(".", f))]
print("Stamped files:")
for f in output_files:
    if f[-3:] == "pdf":
        print(f)

def output(output_path):
    for f in output_files:
        if f[-3:] == "pdf":
            cmd = ["move", f, output_path]
            p = subprocess.run(cmd, stdout=subprocess.PIPE)

output(output_path)

while True:      
    event, values = window.Read()      
    if event is None or event == 'Cancel':      
        break

# a1 = page.addFreetextAnnot(r1, text, fontname="Ti", color=black) #Another method for doing the same thing, but you can't choose alignment

# a1.update(fontsize=10)

#rc = page.insertTextbox(r1, text, fontsize = 12, # choose fontsize (float)
#                  fontname = "Times-Roman",       # a PDF standard font
#                   fontfile = None,                # could be a file on your system
#                   align = 1)                      # 0 = left, 1 = center, 2 = right



#for page in doc: # loop function for doing all pages

#FAQ : 

# Blank box : check text length
# Inverted stamp : try rescanning the pdf or print to file pdf again



