# Py-Zip-Creator
Python script to create/overwrite ZIP files based on a list of paths to files

This Python 3.x CLI script was made to create/overwrite a given ZIP file with a list of paths to files needed to archive.

## Parameters

    zip_creator.py [-h] [-V] file_list zip_file
    
    positional arguments:
      file_list        The files to be used in the operation, as a plain text file
                       (mandatory)
      zip_file         The ZIP file to archive the files into (mandatory)
    
    options:
      -h, --help       show this help message and exit
      -V, --overwrite  Allow overwritting existing ZIP file

## How to use

1. Download the contents of the repository to an empty folder of your choice.
2. Run the following commands:
    $ python -m venv env
    $ python -m pip install -r requirements.txt

   This will install PyInstaller, to be able to generate a binary executable.
3. (Optional) Run the following command to create a binary executable:
    $ pyinstaller -F zip_creator.py

   The result will be in the `dist` directory.
