Click here for [a better version of pymake](https://github.com/modflowpy/pymake)
======

pymake
======

Automatic building of c and fortran source files. Automatically generates dependencies for all the files in a directory. Like a makefile for those not suckled on unix. 


Installation
------------
Download the pymake directory containing makebin.py and dag.py. 

The thinking is to keep a very simple core that is simple to customize for complicated projects, rather than try build a complicated do-it-all library which is complicated to customize.


Usage
-----
```sh
 python pymake/makebin.py -i src-dir/ -o pymake_bin
```
where `src-dir` holds all your .f, .f90, .c(pp), .h(pp) files
Similar projects
----------------

https://code.google.com/p/make-py/

http://benjamin.smedbergs.us/pymake/

https://github.com/mwtoews/MODFLOW-USG/tree/release/pymake

http://www.cmake.org/

