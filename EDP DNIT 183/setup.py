from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform=="win64":
    base="win64GUI"

executables = [Executable('edp.py', base=base, icon='icons/logo.ico')]

files = ['back/', 'banco/', 'front/', 'icons/','logo/','Img/', 'file_version_info.txt']
inc = ['os']
exc = []




setup(
    name = 'edp',
    version = '1.0.1',
    description = 'Ensaios Dinamicos para Pavimentacao',
    options = {'build_exe':{'include_files':files, 'packages': inc, 'excludes': exc}},
    executables = executables
)