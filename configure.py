# project specific poobah

features = [
   ('povray', 'install povray', True)
   ]

def povray (enabled, out, log):
    out.write ('povray := %s\n' % ('povray' if enabled else ''))
    return enabled


