# Download Manager

Python program that manages Downloads

This is a Python program which manages a users Downloads easily.

Have you ever downloaded a bunch of files and have to copy and paste them into the desired foler? (ex lecture notes which need to be moved from Downloads into Desktop/LectureNotes).

In Mac you are not allowed to Cut and paste the folders, so the user has to copy, paste, and the move to trash, which is a process. Additionaly, if you want to rename your file, you have to go one by one and rename each file.

Luckily the os library in Python allows for direct access to files and folders, so i tried to make this process easier by creating this program. Below i will explain each function and main lines of code which do this task.

## **Function 1: main()**

---

### **Gets the user input for which directory they want to move the downloads folder to. Ex: if you want to move the contents from the Downloads folder into a folder in the Desktop.**

### Input Prompt

```Python
move_dir = str(input("Enter main directory to move Download File (ex: Desktop): "))
cwd = os.path.expanduser("~/Downloads/")
move_dir = move_dir[0].upper() + move_dir[1:]
mvdir = os.path.expanduser("~/"+move_dir+"/")
```

### Output

![](markdown-images/output1.png)

- <code>move_dir: </code> A variable that holds the directory where the Download file must go.
- <code>cwd (current working directory): </code> Stores the path of the Download directory, this is fixed as we are moving files from Downloads to external directories.

How do we get this path?

```Python
cwd = os.path.expanduser("~/Downloads/")
```

- <code>os.path.expanduser</code> method in Python is used to expand an initial path component ~( tilde symbol) or ~user in the given path to user’s home directory. From [Geeks for Geeks](https://www.geeksforgeeks.org/python-os-path-expanduser-method/).

So <code>cwd</code> becomes:

```Python
cwd = '/Users/[username]/Downloads/'
```

This is important to understand as in the next line we concatenate <code>move_dir</code> into the <code>os.path.expanduser</code> so the user can choose a custom directory, rather than being restricted to one, like Documents.

```Python
mvdir = os.path.expanduser("~/"+move_dir+"/")
```

Quick: If you are wondering what this line does:

```Python
move_dir = move_dir[0].upper() + move_dir[1:]
```

It allows the user to enter either "Documents" or "documents" as the <code>os.path.expanduser</code> will only allow for the directory name with caps.

---

## **Gets the user input for which folder they want to move the Downloads file into.**

```Python
folder_name = str(input("Enter folder name: "))
print("If folder exists, file will be moved, if not new folder will be crated")

mvdir += folder_name

if not os.path.exists(mvdir):
    os.makedirs(mvdir)
```

<code>folder_name</code> is concatenated with <code>mvdir</code> to specify the folder in the Directory to move the Download file into.

The if statement:

```Python
if not os.path.exists(mvdir):
```

Checks is the path exists, if not it uses the os function <code>os.makedirs(mvdir)</code> and creates a new folder in the directory with the name <code>folder_name</code>

<code>os.makedir</code> vs <code>os.makedirs</code>:

- <code>os.makedir(path)</code>:
  Creates folder in current working directory names <code>path</code>

- <code>os.makedirs(path)</code>:
  Similar to <code>makedir</code>, but makes all intermediate-level directories needed to contain the leaf directory.

Information from [docs.python](https://docs.python.org/3/library/os.html)

## **Call a function to initialize the Downloads directory files, and calls another function to move the files**

```Python
current = initialize_folder(cwd)
del current[0]

print(' ')
print("Files to be moved must be most recently downloaded files")
num_files = int(input("Enter how many downloaded files to move: "))
print("****************************************************")
print(" ")

move_file(current, num_files, cwd, mvdir)

print(" ")
print("****************************************************")
```

The line:

<code>current = initialize_folder(cwd)</code>

Calls the function <code>initialize_folder</code> and assigns its return value into current.

What this function does will be explained in detail later, but for now we can think of it as a function that returns a list of sorted dictionaries (by timne) that contain each file in Downloads name, and a time. The time is how recently the file was modified, i.e how recently it was downloaded.

Note: <code>del current[0]</code> deletes the first element of the list of dictionaries. This is done beacuse the first item is ".DS_Store" which is a hidden file, however, it still shows up in the list and is always the first item. So we delete it from our list.

The line:

<code>move_file(current, num_files, cwd, mvdir)</code>

What this function does will be explained in detail later, but for now we can think of it as a function that moves the files into the desired folder.

## **Function 2: initialize_folder(cwd)**

---

### **Move all files in Downoalds into a dictionary**

```Python
os.chdir(cwd)

time_dict = {}
for f in os.listdir(cwd):
    time_dict.update({f:os.stat(f).st_mtime})
```

The parameter passed to <code>initialize_folder</code> is cwd, which is the current working directory, or: "~/Downloads" in Mac.

- <code>os.chdir</code>: This changes the current working directory into the file name passed into it, in this case cwd, which is the Downloads directory.

- <code>time_dict = {}</code> - initializes a empy dictionary to be populated

Loop throgh each file in Downloads:

```Python
for f in os.listdir(cwd):
    time_dict.update({f:os.stat(f).st_mtime})
```

- <code>os.listdir(cwd)</code> returns a list of all the files in Downloads.

Next we update the dictionary with <code>f</code> (the current file), and the last modified time.

- The last modified time is got by the function <code>os.stat(f).st_mtime</code>. <code>os.stat(f)</code> returns many statistics about the file, all of these can be seen here:
  [Tutorialspoint - os.stat](https://www.tutorialspoint.com/python/os_stat.htm).

we want the most recent modification time so we specify this by adding <code>.st_mtime</code>.

### **Return the sorted list of dictionaries**

Now we have a list populated by the a dictionary filename and most recent modification time, however, the way the files are iterated through in the Downloads folder depends on how they are stored in the OS. They are not sorted by most recent modification time, so we have to return a sorted dictionary list.

```Python
return(sorted(time_dict.items(), key=lambda item: item[1],reverse=True))
```

The built in function in Python <code>sorted()</code> returns a sorted list. It uses a sorting algorithm called TimeSort, which was bult specifically for Python. It has a worst case runtime of around
_<code>O(nlog(n))</code>_ which is quite efficient.
More information at [Wikipedia](https://en.wikipedia.org/wiki/Timsort).

## **Function 3: move_file(current, num_files, cwd, mvdir)**

---

### **Move the files and ask the user if they want to change the file name**

```Python
i = 0
for file in current:
    i += 1
    if i > num_files:
        break
```

This is the loop part which loops through the first <code>i</code> elements of the dictionary which is stored in <code>current</code>. The code exits the loop when <code>i > num_files</code> which is when it looped through the first <code>num_files</code> elements in the list.

```Python
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
```

This part is where we rename and actually move the file. We set <code>curr_file</code> to be <code>file[0]</code> to access the file name, and next ask the user for the desired file name. If the user says 'Yes' we we get the name and use <code>os.rename()</code> to rename the file.

- Python method <code>rename(src,dst)</code> renames the file or directory src to dst. If dst is a file or directory (already present), OSError will be raised.
  From [Tutorialspoint](https://www.tutorialspoint.com/python/os_rename.htm).

After renaming the file, we move the file using the function <code>shutil.move()</code>.

- shutil.move() method Recursively moves a file or directory (source) to another location (destination) and returns the destination. From [Geeks for Geeks](https://www.geeksforgeeks.org/python-shutil-move-method/).

Inside the move function you might have noticed a join function, this joins the new name to current working directory so when we move it it will move the exact file. You might be thinking, why do we have to use a join function? cant we just concatenate the two strings?

There is a good [StackOverflow](https://stackoverflow.com/questions/13944387/why-use-os-path-join-over-string-concatenation) answer which addresses this.

- <code>os.path.join()</code> method in Python join one or more path components intelligently. This method concatenates various path components with exactly one directory separator (‘/’) following each non-empty part except the last path component. If the last path component to be joined is empty then a directory seperator (‘/’) is put at the end. From [Geeks for Geeks](https://www.geeksforgeeks.org/python-os-path-join-method/).
