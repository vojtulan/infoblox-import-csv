import csv
import os
import re 

print("Script has started ...")
print("Validating and repairing csv files ...")
regex = "([0-9a-fA-F]:?){12}"

#check macaddress bad format missing
for filename in os.listdir('csv'):
    #with open("./csv/" + filename, "r+") as csvFile:
    os.rename("./csv/" + filename, "./csv/" + "temp" + filename)
    f = open("./csv/" + "temp" + filename, "r",encoding='utf8')
    a = open("./csv/" + filename, "a",encoding='utf8')
    for row in f:
        if not re.match(regex, row) and not row.startswith(";"):
            row = ";" + row
        
        a.write(row) 

    f.close()
    a.close()
    
    os.remove("./csv/" + "temp" + filename)

r = open("infobloxImport.csv", "w",encoding='utf8')
f = open("corrected.csv", "w",encoding='utf8')


print("Formatting ...")
with open("template.csv") as infoblox_Template:
    reader = csv.reader(infoblox_Template, delimiter=';')
    row = ""
    row1 = ""
    row2 = ""
    dataq = ""
    array = []
    for row in reader:
        array.append(row)
    firstLine = array[0]
    r.write(";".join(array[0]) + "\n")
    r.write(";".join(array[1]) + "\n")
    print(array[0])
    print(array[1])


for filename in os.listdir('csv'):
    print("File: ", filename)
    with open("./csv/" + filename, 'r',encoding='utf8') as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        for row in reader:
            #print(row[0])
            parts = row[2].split(".")
            print(parts)
            ip = ""

            for piece in parts:
                print(piece)
                if piece == "000":
                    piece = "0"
                    ip = ip + piece + "."
                    print("IP:", ip)
                    continue

                elif piece.startswith('00'):
                    piece = piece[2:]
                    ip = ip + piece + "."
                    print("IP:", ip)
                    continue

                elif piece.startswith('0'):
                    piece = piece[1:]
                    ip = ip + piece + "."
                    print("IP:", ip)
                    continue

                else:
                    ip = ip + piece + "."

            print("IPFULL:", ip)
            ip = ip[:-1]
            #print(ip)
            correctedRow = row[0] + ";" + row[1] + ";" + ip + "\n"
            f.write(correctedRow)

            row1 = array[2]
            row2 = array[3]

            if row[0] == "":
                #change macaddress
                row2[14] = "00:00:00:00:00:00"
                row2[15] = "RESERVED"
                

            else:
                #change macaddress
                row2[14] = row[0]
                row2[15] = "MAC_ADDRESS"

            #print(row1[1].replace(" ",""))
            row1[1] = row[1].replace(" ","") 
            #change name
            #row1[1] = row[1]
            #change IP
            row1[3] = ip
            #change IP
            row2[1] = ip
            #change name
            row2[3] = row[1].replace(" ","")
            #add mac address
            

            newLine1 = ";".join(row1)
            newLine2 = ";".join(row2)
            newline1 = newLine1.encode("utf8")
            newline2 = newLine2.encode("utf8")
            r.write(newLine2 + "\n")
            dataq = dataq + newLine1 + "\n"
        
        r.write(dataq)



print("Script has ended, check the newly created 'infobloxImport.csv' ")