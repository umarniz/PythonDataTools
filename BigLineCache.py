
import os
from array import array

""" Builds a cache of line endings to allow jumping to a specific line 
    Creates a .cache file next to the file if a cache doesn't exists
    otherwise reads from the cache directly.
"""
def BuildCache(inputFilePath, forceRebuild):
    # Get file name from input file
    cacheFilePath, ext = os.path.splitext(inputFilePath)

    if not cacheFilePath:
        print "Could not build cache for empty input file"
        return None

    # Create a file with the same name and .cache extension
    cacheFilePath += ".cache"

    line_offset = array('I')

    if os.path.exists(cacheFilePath):
        ReadCache(cacheFilePath, line_offset)
    else:
        WriteCache(cacheFilePath, inputFilePath, line_offset)

    return line_offset

def ReadCache(outputFilePath, offsetArray):

    # Note: Not the best solution as now it gets impossible for an EOF to occur
    # Append array size as file header?

    cacheFileSize = os.path.getsize(outputFilePath)
    arrayItems = cacheFileSize / offsetArray.itemsize

    with open(outputFilePath, 'rb') as cacheF:
        try:
            offsetArray.fromfile(cacheF, arrayItems)
        except EOFError:
            print "Error reading cache. Unexpected end of file."

        cacheF.close()

def WriteCache(outputFilePath, inputFilePath, offsetArray):
    try:
        # Open as binary to include line endings when calculating line length
        with open(inputFilePath, 'rb') as inputFile:
            offset = 0

            for line in inputFile:
                offsetArray.append(offset)
                offset += len(line)

            with open(outputFilePath, 'wb') as cacheF:
                offsetArray.tofile(cacheF)
                cacheF.close()

            inputFile.close()
    except IOError as e:
        print "Error building cache for file " + inputFilePath + ". Error: " + str(e)
