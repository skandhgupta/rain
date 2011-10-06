# project specific poobah

features = [
   ('povray', 'install povray', True),
   ('python-dev', 'python development files', True),
   ('gevent', 'install gevent', True)
   ]

def enable_in_makefile (out, feature, enabled):
    out.write ('%s := %s\n' % (feature, feature if enabled else ''))
    return enabled

def povray (enabled, out, log):
    return enable_in_makefile (out, 'povray', enabled)

def gevent (enabled, out, log):
    return enable_in_makefile (out, 'gevent', enabled)

def python_dev (enabled, out, log):
    if not enabled:
        return False
    frag = """
    #include <Python.h>
    int main () { return 0; }
    """
    from subprocess import Popen, PIPE, STDOUT
    cc = Popen ('cc -x c `python-config --include` - -o /dev/null',
            shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    cc.stdin.write (frag)
    cc.stdin.close ()
    if cc.wait () != 0:
        log ('\nERROR: Python.h not found. Please install the python-dev package.')
        raise Exception
    return True

