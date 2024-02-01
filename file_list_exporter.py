import os

path = './'
output_file = 'file_list.txt'
encoding = 'utf-8'

if not os.path.isdir(path):
    print("The specified path does not exist or is not a directory.")
    exit()

filepaths = []
for root, dirs, files in os.walk(path):
    for file in files:
        filepath = os.path.abspath(os.path.join(root, file))
        filepaths.append(filepath)

if len(filepaths) == 0:
    print("No files found in the specified path.")
    exit()

with open(output_file, 'w', encoding=encoding) as f:
    for filepath in filepaths:
        f.write(filepath+'\n')
