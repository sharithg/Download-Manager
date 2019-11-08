# Copyright (C) 2019 Sharith Godamanna <sharithg@bu.edu>

import os
import shutil


def initialize_folder(cwd):
    
    os.chdir(cwd)

    time_dict = {}
    for f in os.listdir(cwd):
        time_dict.update({f:os.stat(f).st_mtime})


    return(sorted(time_dict.items(), key=lambda item: item[1],reverse=True))



def move_file(current, num_files, cwd, mvdir):

    i = 0
    for file in current:
        i += 1
        if i > num_files:
            break

        curr_file = file[0]
        print(' ')

        print("File ",i,": ",curr_file)
    
        rename = str(input("Rename this file? (Enter Yes or No): "))
        rename = rename[0].upper() + rename[1:]
        
        if rename == 'Yes':
            print(' ')
            new_name = str(input("Enter new name (include extention): "))
            os.rename(curr_file,new_name)
            print('Moving ',new_name,'...')
            shutil.move(os.path.join(cwd,new_name),mvdir)
        else:
            print('Moving ',curr_file,'...')
            shutil.move(os.path.join(cwd,curr_file),mvdir)
        
    
def main():
    print("Welcome to the Downloads Manager! Using this you can easily Manage \n your Downloads and move them to the desired folder")
    print(" ")
    print("Follow the instructions below...")
    print(" ")
    move_dir = str(input("Enter main directory to move Download File (ex: Desktop): "))
    cwd = os.path.expanduser("~/Downloads/")
    move_dir = move_dir[0].upper() + move_dir[1:]
    mvdir = os.path.expanduser("~/"+move_dir+"/")


    folder_name = str(input("Enter folder name: "))
    print("If folder exists, file will be moved, if not new folder will be crated")

    mvdir += folder_name

    print(' ')
    print("Files to be moved must be most recently downloaded files")
    num_files = int(input("Enter how many downloaded files to move: "))


    if not os.path.exists(mvdir):
        os.makedirs(mvdir)

    current = initialize_folder(cwd)
    del current[0]

    print("****************************************************")
    print(" ")
    move_file(current, num_files, cwd, mvdir)
    print(" ")
    print("****************************************************")
    

main()


        

