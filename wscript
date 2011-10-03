#!/usr/bin/env python
# encoding: utf-8

APPNAME = 'myapp'
VERSION = '0.1'

def options (opt):
    opt.load ('python')
    opt.parser.set_default ('prefix', 'build') 

def configure (conf):
    conf.load ('python')
    print (conf.env)

def build (bld):
    bld (rule='python ../deps/virtualenv.py '\
            '--no-site-packages '\
            '--distribute '\
            '--extra-search-dir=../deps '\
            '--never-download '\
            '.')
    bld.add_group ()
