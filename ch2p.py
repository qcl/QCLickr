# -*- coding: utf-8 -*-

import os, sys, subprocess

def convert(sourceDir, targetDir):
    print('prepare convert .heic in %s to %s' % (sourceDir, targetDir))

    if not os.path.exists(sourceDir) or not os.path.isdir(sourceDir):
        print('cannot find source path')
        return

    if not os.path.exists(targetDir) or not os.path.isdir(targetDir):
        print('cannot find target path')
    # TODO if target path didn't exist, create one.

    files = os.listdir(sourceDir)
    for filename in files:
        
        filepath = os.path.join(sourceDir, filename)
        filename, ext = os.path.splitext(filename)

        if ext not in ['.heic', '.HEIC']:
            # skip
            continue

        #print(filename)
        targetPath = os.path.join(targetDir, '%s.%s' % (filename, 'png'))

        if os.path.exists(targetPath):
            print('%s is already there' % (targetPath))
            continue

        convertHeicToPng(filepath, targetPath)


def convertHeicToPng(sourcePath, targetPath):
    print('convert %s to %s' % (sourcePath, targetPath))
    #FIXME for now, it won't bring EXIF info from heic to png
    #subprocess.run(['convert', sourcePath, targetPath])

if __name__ == '__main__':
    print('Convert .heic to .png in a dir')

    if len(sys.argv) > 2:
        convert(sys.argv[1], sys.argv[2])
    else:
        print('Usage: $ python3 ch2p.py [dir_contains_heic] [target_result_dir]')


