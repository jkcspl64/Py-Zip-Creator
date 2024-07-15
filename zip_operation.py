#!/usr/bin/env python3

import pathlib
import zipfile

from typing import List


class FileEntry:
  def __init__(self):
    self.src: pathlib.Path = None
    self.dst: pathlib.Path = None
    self.replace = False
  
  def __str__(self):
    src_exists_txt = "EXISTS" if self.src_exists() else "MISSING"
    return f"FileEntry|{src_exists_txt}|{str(self.src)}|{str(self.dst)}"
  
  def src_exists(self):
    return self.src.exists() and self.src.is_file()
  
  @staticmethod
  def build(src_file: str, dst_dir: str):
    resp = FileEntry()
    resp.src = pathlib.Path(src_file)
    resp.dst = pathlib.Path(dst_dir)
    return resp


class ZippableFile:
  def __init__(self):
    self.files: List[FileEntry] = []
    self.dst = None
    self.ready = False
    self.done = False
    self.is_successful = False
    self.overwritten = False
    self.detail = ""
  
  def __str__(self):
    file_name = "None" if not self.dst else str(self.dst)
    overwrite = "OVERWRITE" if self.overwritten else "CREATE"
    str_template = f"Zip|{overwrite}|{file_name}|" + "{}"
    
    if not self.ready:
      return str_template.format("NOT READY")
    elif not self.done:
      return str_template.format("READY")
    else:
      status = "OK" if self.is_successful else "ERROR"
      oper_info = f"{status}|{self.detail}"
      return str_template.format(oper_info)
  
  def add_file(self, file_entries: List[FileEntry], zfp: pathlib.Path):
    self.files = file_entries
    self.dst = zfp
    self.ready = True
  
  def run(self, overwrite=False):
    if not self.ready:
      self.detail = "File not added to object"
      return
    
    zippable_files = [e for e in self.files if e.src_exists()]
    
    try:
      if len(zippable_files) == 0:
        raise IOError("No files are available to ZIP")
      
      if not self.dst.parent.exists() or not self.dst.parent.is_dir():
        raise IOError("Destination dir. doesn't exist or is not a directory")
      
      if not overwrite and self.dst.exists():
        raise IOError("File exists in destination directory")
      elif self.dst.exists():
        self.overwritten = True
      
      with zipfile.ZipFile(str(self.dst), "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zip_fhand:
        for file in zippable_files:
          dst_name_in_zip = pathlib.Path(file.dst.relative_to(".") / file.src.name)
          zip_fhand.write(str(file.src), str(dst_name_in_zip))
      
      self.is_successful = True
      self.detail = "OK"
    except (IOError, OSError) as e:
      self.detail = str(e)
      self.overwritten = False
    finally:
      self.done = True
