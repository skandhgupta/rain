#!/usr/bin/env python
# encoding: utf-8

APPNAME = 'myapp'
VERSION = '0.1'

top = '.'
out = 'build'

def options (opt):
    opt.load ('python')
    opt.parser.set_default ('prefix', 'build') 

def configure (conf):
    conf.load ('python')
    print (conf.env)

def build (bld):
    """
    bld (rule='python ../deps/virtualenv.py '\
            '--no-site-packages '\
            '--distribute '\
            '--extra-search-dir=../deps '\
            '--never-download '\
            '.')
    bld.add_group ()
    """
    povray_tar = bld.path.find_resource ('deps/povlinux-3.6.tgz')
    bld (rule=do_untar, source=povray_tar)# , cwd=bld.bldnode.abspath())
    # bld (rule=do_untar, source=povray_tar, cwd=bld.bldnode.abspath())
    # bld (rule='tar xvf ${SRC[0].abspath()}', source=povray_tar) # , cwd=bld.bldnode.abspath())

import tarfile
import os
from waflib import Utils

def do_untar (self):
    bldnod = self.generator.bld.bldnode
    blddir = bldnod.abspath ()

    srctar = self.inputs[0].abspath ()
    t = tarfile.open (srctar)
    t.extractall (blddir)
    t.close ()

    xdir = os.path.splitext (os.path.basename (srctar))[0]
    print (xdir)
    xnod = bldnod.find_dir (xdir)
    print (xnod)
    xnod.sig = Utils.h_file (xnod.abspath ())


