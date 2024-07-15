#!/usr/bin/env python3

import sys
import pathlib
import argparse

from typing import List
from zip_operation import FileEntry, ZippableFile


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "-V", "--overwrite", help="Allow overwritting existing ZIP file",
    action="store_true"
  )
  parser.add_argument("file_list", help="The files to be used in the operation, as a plain text file (mandatory)")
  parser.add_argument("zip_file", help="The ZIP file to archive the files into (mandatory)")
  return parser.parse_args()


def get_info_from_txt(file_path: str):
  fp = pathlib.Path(file_path)
  
  if not fp.exists() or not fp.is_file():
    print("ERROR: The input text file doesn't exist or is not a file!", file=sys.stderr)
    exit(-1)
  
  files = []
  
  with open(str(fp), "r", encoding="utf-8") as fhand:
    for line in fhand:
      line_elems = line.strip().split("|")
      files.append(
        FileEntry.build( line_elems[0].strip(), line_elems[1].strip() )
      )
  
  return files


def make_zip(zip_file: str, files_to_zip: List[FileEntry], overwrite: bool):
  zip_op = ZippableFile()
  zfp = pathlib.Path(zip_file)
  
  zip_op.add_file(files_to_zip, zfp)
  zip_op.run(overwrite)
  
  return zip_op


def main():
  args = parse_args()
  
  files_to_zip = get_info_from_txt(args.file_list)
  zip_result = make_zip(args.zip_file, files_to_zip, args.overwrite)
  
  for file in files_to_zip:
    print(str(file))
  
  print(zip_result)


if __name__ == "__main__":
  main()
