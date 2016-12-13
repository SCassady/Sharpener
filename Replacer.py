import math
import re
import os


def GetAllDirectories(givenPath):
    tempDirectoryList = []
    for entry in os.scandir(givenPath):
        if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith('.cs'):
            scriptList.append(entry)
        elif not entry.name.startswith('.') and entry.is_dir():
            tempDirectoryList.append(entry)
            directoryList.append(entry)

    if len(tempDirectoryList) > 0:
        for directory in tempDirectoryList:
            GetAllDirectories(directory.path)

def LineNotCommented(line):
    # Check that '//' does not start the line.
    strippedList = list(line.lstrip())
    if strippedList[0] == '/' and strippedList[1] == '/':
        return False
    return True

def GetInlineComment(givenLine, chars):
    comment = ''
    if '//' in givenLine:
        afterSlashes = False
        for index in range(1, len(chars)):
            if chars[index] == '/' and chars[index-1] == '/':
                afterSlashes = True
                comment = comment + '//'
            elif afterSlashes:
                comment = comment + chars[index]
    return comment.rstrip('\n')

def AlreadyStyled(line):
    newSet = set(line)
    newSet.discard('\t')
    newSet.discard('\n')
    newSet.discard(' ')
    if len(newSet) == 1 and '{' in newSet:
        return True
    return False

path = os.getcwd()

scriptList = []
directoryList = []

GetAllDirectories(path + '/Test')

for directory in directoryList:
    subStrip = directory.path.lstrip(path)
    fullStrip = subStrip.lstrip('/Test/')
    try:
        os.mkdir(path + '/Results/' + fullStrip)
    except:
        print("Couldn't create new folder.")

for script in scriptList:
    fullPath = script.path
    relativeLocation = fullPath.lstrip(path)

    cleanLines = open(relativeLocation, 'r')

    result = open('Results/' + relativeLocation.lstrip('Tests/'),'w')

    for line in cleanLines:
        precedingSpaces = 0
        # charList = re.split(r"(\s+)", line)
        charList = list(line)
        wordList = line.split()

        if 'else if' in line and '{' in line and LineNotCommented(line):
            # print(charList)
            insideParens = ''
            openingParens = 0

            for char in charList:
                if char == '(':
                    openingParens += 1
                elif char == ')':
                    openingParens -= 1
                if openingParens > 0 and char != '\t' and char != '\n':
                    insideParens = insideParens + char

            inlineComment = GetInlineComment(line, charList)

            changedLine = line.rstrip('\n')
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip(inlineComment)
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip('{')
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip('else if ' + insideParens + ')')
            changedLine = changedLine.rstrip()

            if inlineComment != '':
                inlineComment = '    ' + inlineComment

            result.write(changedLine + '\n')

            precedingSpaces = len(str(line)) - len(str(line).lstrip())

            result.write('    ' * precedingSpaces + 'else if ' + insideParens + ')' + inlineComment + '\n')
            result.write('    ' * precedingSpaces + '{\n')
        elif 'else' in line and '{' in line and LineNotCommented(line):
            inlineComment = GetInlineComment(line, charList)

            changedLine = line.rstrip('\n')
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip(inlineComment)
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip('{')
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip('else')
            changedLine = changedLine.rstrip()

            if inlineComment != '':
                inlineComment = '    ' + inlineComment

            result.write(changedLine + '\n')

            precedingSpaces = len(str(line)) - len(str(line).lstrip())

            result.write('    ' * precedingSpaces + 'else' + inlineComment + '\n')
            result.write('    ' * precedingSpaces + '{\n')
        elif '{' in line and '}' not in line and LineNotCommented(line) and not AlreadyStyled(line):
            inlineComment = GetInlineComment(line, charList)

            changedLine = line.rstrip('\n')
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip(inlineComment)
            changedLine = changedLine.rstrip()
            changedLine = changedLine.rstrip('{')
            changedLine = changedLine.rstrip()

            if inlineComment != '':
                inlineComment = '    ' + inlineComment

            result.write(changedLine + inlineComment + '\n')

            precedingSpaces = len(str(line)) - len(str(line).lstrip())

            result.write('    ' * precedingSpaces + '{\n')
        else:
            result.write(line)

    print(relativeLocation + " processed.")
