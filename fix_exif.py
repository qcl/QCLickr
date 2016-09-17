# -*- coding: utf-8 -*-
# Fix my date time info of photos taken by my new camera before I set the correct date time  

import pexif

path = '../../Desktop/2016.09.08新相機80D試拍/'
newPath = '../../Desktop/modified/'

needFixNumber = 43

for i in range(1, needFixNumber + 1):
    filePath = path + 'IMG_%04d.JPG' % (i)
    print 'read',filePath

    img = pexif.JpegFile.fromFile(filePath)
    print img

    exif = img.exif
    primary = img.exif.primary
    extendedExif = primary.ExtendedEXIF

    # yyyy:mm:dd hh:mm:ss
    time = primary.DateTime.split(':')

    print primary.DateTime
    shiftedM = int(time[3]) + 30
    shiftedTime = '2016:09:08 21:%02d:%s' % (shiftedM, time[4])
    print shiftedTime

    # modify
    primary.DateTime = shiftedTime
    extendedExif.DateTimeOriginal = shiftedTime
    extendedExif.DateTimeDigitized = shiftedTime

    # save it.
    fileNewPath = newPath + 'IMG_%04d.JPG' % (i)
    img.writeFile(fileNewPath)


