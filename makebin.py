#! /usr/bin/env python
"""
Make the binary executable for MODFLOW-USG.
"""
__author__ = "Christian D. Langevin"
__date__ = "March 20, 2014"
__version__ = "1.0.0"
__maintainer__ = "Christian D. Langevin"
__email__ = "langevin@usgs.gov"
__status__ = "Production"

# mja 
# remove ieee_arithmetic dependence in gwf2swr7_NWT.f and gsol7.f using http://stackoverflow.com/questions/17389958/is-there-a-standard-way-to-check-for-infinite-and-nan-in-fortran-90-95
# change T1 in gwf2swr7_NWT.f to real*4 -- TODO this probs isn't wise
# C  mja      DOUBLEPRECISION, INTENT(INOUT) :: T1
#         real*4 :: T1
# change to       DATA FORM/'UNFORMATTED'/ in openspec.inc
# then run this
# 

# check call:  ['gfortran', '-O2', '-o', '././MF_NWT', 'gwfsfrmodule_NWT.o', 'mhc7.o', 'gwf2bas7_NWT.o', 'gwf2lpf7.o', 'sip7_NWT.o', 'gwf2chd7.o', 'gwf2riv7_NWT.o', 'gwf2drn7_NWT.o', 'gwf2swt7.o', 'gmg7.o', 'gwf2bcf7.o', 'gsol7.o', 'obs2bas7.o', 'mach_mod.o', 'gwf2ghb7_NWT.o', 'gwf2str7.o', 'gwfuzfmodule_NWT.o', 'gwf2sub7_NWT.o', 'gwf2fhb7.o', 'gwf2evt7.o', 'gwf2hfb7_NWT.o', 'utl7.o', 'de47_NWT.o', 'gwf2ibs7.o', 'NWT1_ilupc_mod.o', 'obs2chd7.o', 'obs2riv7.o', 'gwf2drt7.o', 'parutl7.o', 'gwf2huf7.o', 'gwf2hydmod7.o', 'gwf2res7.o', 'modules.o', 'NWT1_xmdlib.o', 'pcg7_NWT.o', 'gwf2ets7.o', 'gwf2rch7.o', 'NWT1_module.o', 'gwf2upw1.o', 'obs2ghb7.o', 'NWT1_xmd.o', 'obs2drn7.o', 'gwf2wel7_NWT.o', 'gwf2mnw27_NWT.o', 'obs2str7.o', 'gwf2mnw17_NWT.o', 'hufutl7.o', 'gwf2swi27_NWT.o', 'gwf2lak7_NWT.o', 'gwf2swr7_NWT.o', 'NWT1_gmres.o', 'lmt7_NWT.o', 'gwf2uzf1_NWT.o', 'gwf2mnw2i7.o', 'gwf2gag7.o', 'MF_NWT.o', 'gwf2sfr7_NWT.o', 'NWT1_solver.o']


import os
import subprocess
import shutil
import sys
import getopt
from dag import order_source_files, order_c_source_files

def compilewin(srcfiles, fc, compileflags, target, makeclean, platform):
    """
    Make target on Windows OS
    """
    if 'ifort' in fc:
        cpvars = os.environ.get('IFORT_COMPILER13') + 'bin/compilervars.bat'
        #cpvars = 'C:/Program Files (x86)/Intel/Composer XE 2013/bin/compilervars.bat'
    f = open('compileusg.bat', 'w')
    line = 'call ' + '"' + os.path.normpath(cpvars) + '" ' + platform + '\n'
    f.write(line)

    #build object files
    for srcfile in srcfiles:
        cmd = fc + ' '
        for switch in compileflags:
            cmd += switch + ' '
        cmd += '-c' + ' '
        cmd += srcfile
        cmd += '\n'
        f.write(cmd)

    #build executable
    cmd = fc + ' '
    for switch in compileflags:
        cmd += switch + ' '
    cmd += '-o' + ' ' + target + ' ' + '*.obj' + '\n'
    f.write(cmd)
    f.close()

    #run the batch file
    subprocess.check_call(['compileusg.bat', ],)
    return

def compilemac(srcfiles, fc, compileflags, cc, cflags, target, makeclean): # mja 
    """
    Make target on Mac OS or Linux
    """
    syslibs = ['-lc']

    #build object files
    objfiles = []
    for srcfile in srcfiles:
        cmdlist = []
        if srcfile.endswith('.c') or srcfile.endswith('.cpp'):        #mja
            cmdlist.append(cc)      #mja
            for switch in cflags:       #mja
                cmdlist.append(switch)      #mja
        else:           #mja
            cmdlist.append(fc)
            for switch in compileflags:
                cmdlist.append(switch)
        cmdlist.append('-c')
        cmdlist.append(srcfile)
        print 'check call: ', cmdlist
        subprocess.check_call(cmdlist)
        srcname, srcext = os.path.splitext(srcfile)
        srcname = srcname.split(os.path.sep)[-1]
        objfiles.append(srcname + '.o')

    #build executable
    cmd = fc + ' '
    cmdlist = []
    cmdlist.append(fc)
    for switch in compileflags:
        cmd += switch + ' '
        cmdlist.append(switch)
    cmd += '-o' + ' ' + target + ' ' + '*.obj'
    cmdlist.append('-o')
    cmdlist.append(os.path.join('.',target))
    for objfile in objfiles:
        cmdlist.append(objfile)
    for switch in syslibs:
        cmdlist.append(switch)
    print 'check call: ', cmdlist
    subprocess.check_call(cmdlist)
    return

def main(argv):
    """
    Create the binary executable(s)
    """
    
    # mja
    inputdir = '../src'
    outputfile = 'pymade'
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print 'test.py -i <inputdir> -o <outputfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputdir> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputdir = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
    print 'Input file is "', inputdir
    print 'Output file is "', outputfile
    # end mja

    print "asdfasdfasdfasdf", os.listdir(os.path.abspath(inputdir))

    makeclean = True
    #targetpth = os.path.join('..', 'bin')
    targetpth = '.'  #put in current directory
    # target = os.path.join(targetpth, 'MF_NWT')
    target = outputfile #mja

    #remove the target if it already exists
    try:
        os.remove(target)
    except:
        pass    
    
    #copy the original source to a src directory
    # srcdir_origin = os.path.join('..', 'src')
    srcdir_origin = os.path.abspath(inputdir) # mja
    try:
        shutil.rmtree('pymake_tempdir_src')
    except:
        pass
    shutil.copytree(srcdir_origin, 'pymake_tempdir_src')
    srcdir_temp = os.path.join('.', 'pymake_tempdir_src')
        
    #create a list of all f and f90 source files
    templist = os.listdir(srcdir_temp)
    cfiles = [] # mja
    srcfiles = []
    for f in templist:
        if f.endswith('.f') or f.endswith('.f90'):
            srcfiles.append(f)
        elif f.endswith('.c') or f.endswith('.cpp'): #mja
            cfiles.append(f)    #mja


    srcfileswithpath = []
    for srcfile in srcfiles:
        s = os.path.join(srcdir_temp, srcfile)
        srcfileswithpath.append(s)


    cfileswithpath = [] #mja
    for srcfile in cfiles:  #mja
        s = os.path.join(srcdir_temp, srcfile)  #mja
        cfileswithpath.append(s)        #mja

    #order the source files using the directed acyclic graph in dag.py
    orderedsourcefiles = order_source_files(srcfileswithpath) + order_c_source_files(cfileswithpath) #mja

    platform = sys.platform
    # mja if platform.lower() == 'darwin':
    if platform.lower() == 'darwin' or platform.lower() == 'linux2': #mja
        fc = 'gfortran'
        compileflags = ['-O2']
        objext = '.o'
        
        cc = 'gcc' #mja
        cflags = ['-D_UF', '-O3'] #mja

        #need to change openspec.inc,this is for MODFLOW
        fname = os.path.join(srcdir_temp, 'openspec.inc')
        f = open(fname, 'w')
        f.write(
'''c -- created by makebin.py   
      CHARACTER*20 ACCESS,FORM,ACTION(2)
      DATA ACCESS/'STREAM'/
      DATA FORM/'UNFORMATTED'/
      DATA (ACTION(I),I=1,2)/'READ','READWRITE'/
c -- end of include file
'''
        )
        f.close()

        try:
            compilemac(orderedsourcefiles, fc, compileflags, cc, cflags, target, makeclean) # mja
        except:
            print 'Error.  Could not build target...'
       
    else:
        fc = 'ifort.exe'
        #production version compile flags
        compileflags = [
                       '-O2',
                       '-heap-arrays:0',
                       '-fpe:0',
                       '-traceback',
                       ]
        objext = '.obj'
        
        #create a 32-bit executable
        try:
            compilewin(orderedsourcefiles, fc, compileflags, target, makeclean,
                  'ia32')
        except:
            print 'Error.  Could not build 32-bit target...'

        #create a 64-bit executable
        try:
            compilewin(orderedsourcefiles, fc, compileflags, target+'_x64', 
                  makeclean, 'intel64')
        except:
            print 'Error.  Could not build 64-bit target...'
                  
    #clean things up
    if makeclean:
        print 'making clean...'
        filelist = os.listdir('.')
        delext = ['.mod', objext]
        for f in filelist:
            for ext in delext:
                if f.endswith(ext):
                    os.remove(f)
        shutil.rmtree(srcdir_temp)

    print 'Done...'
    return

if __name__ == "__main__":    
    main(sys.argv[1:])



    
