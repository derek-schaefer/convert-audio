#!/usr/bin/env python

# sudo apt-get install ffmpeg libavcodec-extra-53

import os
import sys
import re
import signal
import subprocess
import multiprocessing

QUALITY = '-aq 2' # 2-pass VBR
OVERWRITE = '-y'

def find_files(from_ext, to_ext, path):
    file_re = re.compile(r'^(.+)\.%s' % from_ext)
    files = []
    for f in os.listdir(path):
        match = file_re.match(f)
        if match:
            fname = match.groups()[0]
            from_file = '%s.%s' % (fname, from_ext)
            to_file = '%s.%s' % (fname, to_ext)
            files.append((from_file,to_file))
    return files

def convert(f):
    from_file = f[0]
    to_file = f[1]
    cmd = ['ffmpeg', OVERWRITE, '-i', from_file] + QUALITY.split() + [to_file]
    print 'Converting %s' % from_file
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGTERM)

def main():
    from_ext = sys.argv[1]
    to_ext = sys.argv[2]
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    try:
        pool.map(convert, find_files(from_ext, to_ext, os.getcwd()))
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()

if __name__ == '__main__':
    main()
