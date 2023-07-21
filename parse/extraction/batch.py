import os, sys, subprocess, shutil
import subprocess as sp

# files=os.listdir(os.getcwd())
# os.chdir('/home/intern/Dyna/data/sel4_10k/2020/1389/')
files = ['test_file_2020in1389.txt']

total=0
sucMDA=0
sucQuant=0
fina=0

sucMDAlist=[]
sucQuantlist=[]
finalist=[]
faillist=[]

approx_total=len(files)

for file in files:
    print("processing: ", file)
    if file.endswith(".txt"):
        # a valid file.
        total+=1
        print("progress... ", float(total)/float(approx_total)*100, " %")

        respond = sp.run(["perl", "extract.pl", file], capture_output=True, text=True)
    
    respond = respond.stdout.split('\n')
    
    if "Invalid Item 7: Financial statements found. " in respond:
        fina+=1
        finalist.append(file)
    if "mdaFile outputted." in respond:
        sucMDA+=1
        sucMDAlist.append(file)
    if "quant outputted" in respond:
        sucQuant+=1
        sucQuantlist.append(file)

# all files into faillist. 
for x in files:
    if ".txt" in x:
        faillist.append(x)
# remove financial statements ones. 
for x in finalist:
    if x in faillist:
        faillist.remove(x)
# remove MDA ones.
for x in sucMDAlist:
    if x in faillist:
        faillist.remove(x)
# remove Quant ones.
for x in sucQuantlist:
    if x in faillist:
        faillist.remove(x)
    
try:
    os.mkdir("sucMDA")
    os.mkdir("sucQuant")
    os.mkdir("fail")
    os.mkdir("fina")
    # in fail and fina, it's most probable to improve. 
    # prepare two folders to contain file for further improvements. 
    os.mkdir("fail/ori")
    os.mkdir("fina/ori")
except:
    pass

# Will use test.txt as example below. 

print("processing MDA files...")
for file in sucMDAlist:
    splitor = file.rsplit('.', 1) # file = test.txt
    name = splitor[0] # name = test
    filehtml = name+".html" # filehtml = test.html
    filemda = file+"_mda" # filemda = test.txt_mda

    # copy html into sucMDA.
    shutil.copy(file, "sucMDA/"+filehtml) # sucMDA/test.html
    # move mda
    os.rename(filemda, "sucMDA/"+filemda) # sucMDA/test.txt_mda

print("processing Quantitative files...")
for file in sucQuantlist:
    splitor = file.rsplit('.', 1) # file = test.txt
    name = splitor[0] # name = test
    filequant = file+"_quant" # filequant = test.txt_quant

    # move quant
    os.rename(filequant, "sucQuant/"+filequant) # sucQuant/test.text_quant

# Only output plain text. 
print("processing Financial statements files...")
for file in finalist:
    splitor=file.rsplit('.', 1)
    name=splitor[0]
    filehtml=name+".html" # test.html
    fileplaintext=file+"_plaintext" # test.txt_plaintext

    # copy plaintext. 
    shutil.copy(file+"_plaintext", "fina/"+file+"_plaintext")
    # copy original text under fail/ori.
    shutil.copy(file, "fina/ori/"+file)
    # copy html. 
    shutil.copy(file, "fina/"+filehtml)

print("processing Fail files...")
for file in faillist:
    splitor = file.rsplit('.', 1)
    name = splitor[0]
    filehtml = name+".html" # test.html
    fileplaintext=file+"_plaintext" # test.txt_plaintext

  # copy plaintext
    shutil.copy(fileplaintext, "fail/"+fileplaintext)
    # copy html
    shutil.copy(file, "fail/"+filehtml)
    # copy original text
    shutil.copy(file, "fail/ori/"+file)

with open('result', 'w', encoding='utf-8') as fh:
    fh.write(f"Total files: {total}\n")
    fh.write("    # all files with .txt ending.\n")
    fh.write(f"mda: {sucMDA}\n")
    fh.write("    # all mda. only consider mda in item 6 or item 7. \n")
    fh.write(f"quantitative: {sucQuant}\n")
    fh.write("    # all quant. only consider Item 7A quant. \n")
    fh.write(f"financial statements: {fina}\n")
    fh.write("    # item 7 is finan but item 6 is not MDA. \n")
    fh.write("    # improvements may be found here \n")
    fh.write(f"Fail files: {len(faillist)}\n")
    fh.write("    # fail cases.. \n")
    fh.write("    # improvements may be found here \n")
    fh.write("\n\n")
    passFile = total - len(faillist)
    fh.write("Pass rate = "+str(float(passFile)/float(total)*100)+"\n")
    fh.write("passfiles = total - fail = "+str(passFile)+"\n")
    # fh.write("MDA rate = MDA files / passfiles = "+str(float(sucMDA)/float(passFile)*100)+"\n")


print("Done. Refer to result for more info.")
