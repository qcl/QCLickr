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
    files.sort()
    print('there is %d files in source dir' % (len(files)))
    files = list(filter(lambda x: len(x) > 5 and x[-5:] in ['.heic', 'HEIC'], files))
    print('and %d files are HEIC file' % (len(files)))
    totalHEIC = len(files)
    count = 1
    for filename in files:
        print('[ %d / %d ]' % (count, totalHEIC))
        count += 1
        
        filepath = os.path.join(sourceDir, filename)
        filename, ext = os.path.splitext(filename)

        #print(filename)
        targetPath = os.path.join(targetDir, '%s.%s' % (filename, 'jpg'))

        if os.path.exists(targetPath):
            print('%s is already there' % (targetPath))
            continue

        convertHeicToJpg(filepath, targetPath)


def convertHeicToJpg(sourcePath, targetPath):
    print('convert %s to %s' % (sourcePath, targetPath))
    subprocess.run(['convert', sourcePath, targetPath])

if __name__ == '__main__':
    print('Convert .heic to .jpg in a dir')

    if len(sys.argv) > 2:
        convert(sys.argv[1], sys.argv[2])
    else:
        print('Usage: $ python3 copyHEICtoJPG.py [dir_contains_heic] [target_result_dir]')


