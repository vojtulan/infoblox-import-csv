import csv
import os
import re

print("Script has started ...")
print("Validating and repairing csv files ...")
regex = "([0-9a-fA-F]:?){12}"

czechChars = ["á", "č", "ď", "é", "ě", "í", "ň", "ó", "ř", "š", "ť", "ú", "ů", "ý", "ž","Á", "Č", "Ď", "É", "Ě", "Í", "Ň", "Ó", "Ř", "Š", "Ť", "Ú", "Ů", "Ý", "Ž"]
remap = ["a", "c", "d", "e", "e", "i", "n", "o", "r", "s", "t", "u", "u", "y", "z","A", "C", "D", "E", "E", "I", "N", "O", "R", "S", "T", "U", "U", "Y", "Z"]


def Translate(string):
    translatedString = ""
    charList = [char for char in string]
    for char in charList:
        isCharRemaped = False
        for czechCharIndex in range(0, len(czechChars) - 1):
            if char == czechChars[czechCharIndex]:
                translatedString += remap[czechCharIndex]
                isCharRemaped = True
                break

        if not isCharRemaped:
            translatedString += char

    return translatedString


headerHostAddress = "header-hostaddress;address*;_new_address;parent*;boot_file;boot_server;broadcast_address;configure_for_dhcp;configure_for_dns;deny_bootp;domain_name;domain_name_servers;ignore_dhcp_param_request_list;lease_time;mac_address;match_option;network_view;next_server;option_logic_filters;pxe_lease_time;pxe_lease_time_enabled;routers;use_for_ea_inheritance;view"
headerHostRecord = "header-hostrecord;fqdn*;_new_fqdn;addresses;aliases;cli_credentials;comment;configure_for_dns;_new_configure_for_dns;created_timestamp;creator_member;ddns_protected;disabled;enable_discovery;enable_immediate_discovery;ipv6_addresses;network_view;override_cli_credentials;override_credential;snmpv1v2_credential;snmpv3_credential;ttl;use_snmpv3_credential;view"
templateHostRecord = "hostrecord;P20325;;10.32.22.2;;;;FALSE;;;;FALSE;FALSE;TRUE;FALSE;;Default;;FALSE;;;;FALSE;"
templateHostAddress = "hostaddress;10.32.22.2;;P20325;;;;TRUE;FALSE;;;;;;00:00:00:00:00:07;MAC_ADDRESS;Default;;;;;;TRUE;"

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
#f = open("corrected.csv", "w",encoding='utf8')

print("Formatting ...")


templateHostAddressArray = templateHostAddress.split(";")
templateHostRecordArray = templateHostRecord.split(";")


r.write(headerHostRecord + "\n")
r.write(headerHostAddress + "\n")

for filename in os.listdir('csv'):
    print("File: ", filename)
    with open("./csv/" + filename, 'r',encoding='utf8') as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        hostRecordArray = []
        hostAddressArray = []
        for row in reader:
            #print(row)
            parts = row[2].split(".")
            
            ip = ""
            
            for piece in parts:
                #print(piece)
                if piece == "000":
                    piece = "0"
                    ip = ip + piece + "."
                    #print("IP:", ip)
                    continue

                elif piece.startswith('00'):
                    piece = piece[2:]
                    ip = ip + piece + "."
                    #print("IP:", ip)
                    continue

                elif piece.startswith('0'):
                    piece = piece[1:]
                    ip = ip + piece + "."
                    #print("IP:", ip)
                    continue

                else:
                    ip = ip + piece + "."
            
            ip = ip[:-1]
            hostAddress = templateHostAddressArray
            hostRecord = templateHostRecordArray
            
            hostAddress[1] = ip
            hostRecord[3] = ip
            
            if not row[0]:
                #change macaddress
                #print("jsme v podmince")
                hostAddress[14] = "00:00:00:00:00:00"
                hostAddress[15] = "RESERVED"
                hostAddress[7] = "FALSE"
                
            else:
                #change macaddress
                hostAddress[14] = row[0]
                hostAddress[15] = "MAC_ADDRESS"
                hostAddress[7] = "TRUE"
            
            
            clearSpaces = row[1].replace(" ","")
            hostRecord[1] = clearSpaces.replace("(","_")
            hostRecord[1] = hostRecord[1].replace(")","")
            hostRecord[1] = Translate(hostRecord[1])
            #TADY UPRAVUJ A PRIDAVEJ jen zkopiruj a uncomment
            #priklad - nahradis ? za underscore atd
            
            #hostRecord[1] = hostRecord[1].replace("/","TEST")
            
            #TADY UZ MI NA TO ZASE NESAHEJ
            hostAddress[3] = hostRecord[1]
            
            hostRecord = ";".join(hostRecord)
            hostAddress = ";".join(hostAddress)
            
            hostRecordArray += [hostRecord]
            hostAddressArray += [hostAddress]
        
        for i in hostRecordArray:
            r.write(i + "\n")
        for i in hostAddressArray:
            r.write(i + "\n")


print("Script has ended, check the newly created 'infobloxImport.csv' ")
            