#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  Collection of all auxiliary utilities.
"""
import sys
import os
import time
import datetime
import pytz
import re
import shutil
import errno
import stat
import subprocess
import cPickle as pickle
import urllib2
import html5lib


def doc4url(url):
    builder = html5lib.getTreeBuilder('lxml')
    parser  = html5lib.HTMLParser(builder, namespaceHTMLElements = False)
    try:
        doc     = parser.parse(urllib2.urlopen(url).read())
    except:
        return None
    root    = doc.getroot()
    return root


def data2pickle(data, filename):
    lfile = open(filename, "w")
    p = pickle.Pickler(lfile)
    p.dump(data)
    lfile.close()

def pickle2data(filename):
    lf = open(filename, 'r')
    data  = pickle.load(lf)
    lf.close()
    return data

def file_is_ok(filepath):
    """
      Simple checks — file ``filepath`` exists and has nonzero size.
    """
    return os.path.exists(filepath) and os.stat(filepath).st_size>0

def touch(fname, times = None):
    with file(fname, 'a'):
        os.utime(fname, times)


def need_update(target, source, update_time = None):
    """
     Simple refresh condition for target file
    """
    if not os.path.exists(source):
        return False
    source_time = os.stat(source).st_mtime
    if update_time:
        source_time = max(update_time, source_time)
    res = not file_is_ok(target) or     os.stat(target).st_mtime < source_time
    if res:
        pass

    return res

def date822(date):
    date = datetime.timedelta(seconds=secs)

    if not date.tzinfo:
        date = pytz.timezone(settings.TIME_ZONE).localize(date)
    return date.strftime('%a, %d %b %Y %H:%M:%S %z')

def transaction(target, source, action, update_time = None):
    """
      Simple and lazy transactional refresh mechanism.
      If source refreshed:
        target = action(source)
    """
    if not need_update(target, source, update_time):
        return

    directory, nameext = os.path.split(target)
    tmp  = os.path.join(directory, "~~" + nameext)
    createdir(directory)
    res_act = action(tmp, source)
    if res_act and file_is_ok(tmp):
        if os.path.exists(target):
            bak = os.path.join(directory, "~~~~" + nameext)
            if os.path.exists(bak):
                os.unlink(bak)
            os.rename(target, bak)
            hidefile(bak)
        shutil.move(tmp, target)

def createdir(dirpath):
    """
     Create directory with parent directories.
    """
    if not os.path.exists(dirpath):
        print "Try to create ", dirpath
        try:
            os.mkdir(dirpath)
        except OSError:
            (path, dir_) = os.path.split(dirpath)
            if dir_ != "":
                createdir(path)
                os.mkdir(dirpath)

def hash4string(str, salt=None):
    import hashlib
    m = hashlib.sha1()   # Perfectionist can use sha224.
    m.update(str)
    return m.hexdigest()[:16]


def hash4file(filepath, salt=None):
    """
     Get some HashDigest for file without reading it entirely into memory.
    """
    import hashlib
    # pylint: disable-msg=E1101
    m = hashlib.sha1()   # Perfectionist can use sha224.

    if filepath:
        block_size = 2**16     # Perfectionist can tune.
        lf = open(filepath,"r")
        while True:
            data = lf.read(block_size)
            if not data:
                break
            m.update(data)
        lf.close()
    if salt:
        m.update(salt)
    return m.hexdigest()[:16]


def unicodeanyway(astr):
    """
     Try to guess input encoding and decode input «bytes»-string to unicode string.
    """
    str_ = astr
    for encoding in "utf-8", "windows-1251", "cp866", "koi-8":
        try:
            str_ = unicode(astr.decode(encoding))
            break
        except:
            # pylint: disable-msg=W0702
            pass
    return str_


def dateanyway(sdate):
    """
     Try to guess string date format
    """
    date = None
    for datetime_format in ['%Y-%m-%d %H:%M:%S',
                            '%Y/%m/%d %H:%M:%S',
                            '%d %b %Y %H:%M:%S',
                            '%H:%M:%S.%f',
                            '%H:%M:%S',
                            '%M:%S.%f',
                            '%M:%S']:
        try:
            date = datetime.datetime.strptime(sdate.strip(), datetime_format)
            break
        except ValueError:
            pass
    if date:
        return date
    raise Exception("Cannot guess date format for %s " % sdate)

def handle_remove_readonly(func, path, exc):
    """
    To kill read-only files.
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise

def removedirorfile(p, olderthan=None):
    """
      Try to silently remove file or recursively remove directory,
      ignoring errors and warnings.
    """
    def _onerror(func, path, exc_info):
        """
        Make readonly files writeable and try to resume deletion.
        """
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise exc_info

    if type(p) == type([]):
        for pp in p:
            removedirorfile(pp)
    else:
        if not os.path.exists(p):
            return
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=False, onerror=_onerror)
        else:
            needremove = True
            if olderthan:
                dt  = os.stat(p).st_ctime
                needremove = dt < olderthan
            if needremove:
                os.unlink(p)

def install_if_asked():
    """
      Analize input params, and if
      parameter is 'install'
      make a bat-file in PATH
      that call this python script
    """
    if len(sys.argv)>1 and sys.argv[1] == "install":
        # pylint: disable-msg=W0612
        script = sys.argv[0]
        path, nameext = os.path.split(sys.argv[0])
        if path == "":
            path = os.getcwd()
            script = os.path.join(path, nameext)
        name, ext = os.path.splitext(nameext)
        batfile = r'c:\\app\\bin\\' + name + '.bat'
        lf = open(batfile , "w")
        ls = """rem bat-wrapper for script %(script)s
c:\\app\docstruct\\python27\\python %(script)s %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9
""" % vars()
        lf.write(ls)
        lf.close()
        print batfile, "installed..."
        sys.exit(0)

def get_run_dir():
    """
      Get home directory for runned python script
    """
    rundir = os.path.split(sys.argv[0])[0]
    return rundir

def get_tools_dir():
    """
      Get  directory for auxiliary tools and utilities
    """
    toolsdir = os.path.abspath(os.path.join(get_run_dir(),"../tools"))
    toolsdir_shortcut_file = os.path.join(toolsdir , 'toolsdir.txt')
    if os.path.exists(toolsdir_shortcut_file):
        toolsdir = file2string(toolsdir_shortcut_file)

    return toolsdir

def get_prog_output(scmd):
    """
      Run command,  grab and return its output.
    """
    #proc = subprocess.Popen(scmd.split(),
    #                        stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE)
    #res = proc.communicate()
    progin, progout = os.popen4(scmd)
    sout = progout.read()
    progout.close()
    #sout = res[0]
    return sout




def get_prog_output_with_log(scmd):
    """
      Run command,  grab and return its output.
    """
    progin, progout = os.popen4(scmd)
    soutlines = []
    while True:
        line = progout.readline()
        if line:
            print unicodeanyway(line).encode("utf8"),
            soutlines.append(line)
        else:
            break
    progout.close()
    return "\n".join(soutlines)

def no_empty_lines(filename):
    """
    Удаляет пустые строки из файла.
    """
    text = file2string(filename)

    noemptylines = re.compile(r"^\s*\n", re.MULTILINE)
    newtext = re.sub(noemptylines, "", text )
    string2file(newtext, filename)

def string2file(string, filepath, encoding='utf-8'):
    """
      Write given string to the file
    """
    unhidefile(filepath)
    afile = open(filepath, 'w')
    ustring = unicodeanyway(string)
    afile.write(ustring.encode(encoding))
    afile.close()

def file2string(filepath):
    """
    Считать файл и вернуть его содержимое одной строкой
    """
    lfile = open(filepath, "r")
    lstr = lfile.read()
    lfile.close()
    return lstr

def struct2file(struct, filepath):
    """
    Сериализовать Python-структуру в виде отформатированного Python-кода
    """
    from pprint import pprint
    lfile = open(filepath, "w")
    pprint(struct, lfile)
    lfile.close()

def replace_substrings(source, trans):
    """
      For each dictonary entry `trans`
      preform string replacement.
    """
    res = source
    for from_str, to_str in trans.items():
        if from_str:
            res = res.replace(from_str, to_str)
    return res

def copytree(src, dst):
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                copytree(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
        except EnvironmentError, why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise EnvironmentError, errors

def time2ms(timeframe):
    basetime = datetime.datetime.strptime('0:00.0', '%M:%S.%f')
    if timeframe.find('.')<0:
        timeframe += '.0'
    delta_ = dateanyway(timeframe) - basetime
    ms_ = delta_.seconds*1000 + delta_.microseconds/1000
    #curframe = int((delta_.seconds + delta_.microseconds/1000000.0) * 25.0 )
    return ms_

def compare_by_creation_time(file1, file2):
    """
      compare two files by creation time.
      if creation time equals, comparing modification time.
    """
    if not os.path.exists(file1) or not os.path.exists(file2):
        return 0
    res = int((os.stat(file1).st_ctime - os.stat(file2).st_ctime) * 1000)
    if not res:
        res = int((os.stat(file1).st_mtime - os.stat(file2).st_mtime) * 1000)
    return res


def search_file(thefilename, search_path):
    """
    Find file in given path. Comparing case unsensitive.
    """
    for root, _dirnames, filenames in os.walk(search_path):
        if thefilename.lower() in [f.lower() for f in filenames]:
            return os.path.join(search_path, root, thefilename)
    return None


def hidefile(filepath):
    try:
        import win32con, win32api
        win32api.SetFileAttributes(filepath, win32con.FILE_ATTRIBUTE_HIDDEN)
    except:
        pass

def unhidefile(filepath):
    try:
        import win32con, win32api
        win32api.SetFileAttributes(filepath, win32con.FILE_ATTRIBUTE_NORMAL)
    except:
        pass


def is_debug():
    for debugmod in ['dbgp._client', 'pydevd', 'rpyc']:
        if debugmod in sys.modules:
            return True

    return False