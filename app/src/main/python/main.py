import faulthandler
faulthandler.enable()

import logcat
import subprocess, os, sys, traceback, time, email, tarfile
from distutils.version import StrictVersion

def tar_version(path):
    with tarfile.open(path) as tar:
        info_members = [member for member in tar.getmembers() if os.path.basename(member.name) == 'PKG-INFO']
        info_member = min(info_members, key=lambda member: len(member.name))
        info = tar.extractfile(info_member).read()
    return email.message_from_bytes(info)['Version']

INSTALL_PHRASES = [b'Successfully installed']
UNINSTALL_PHRASES = [b'Successfully uninstalled', b'as it is not installed']

def execute(command, kill_phrases=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    killed = False
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

        #XXX until next version of pip
        if kill_phrases is not None and any(phrase in nextline for phrase in kill_phrases):
            time.sleep(2)
            process.kill()
            killed = True
            break

    output = process.communicate()[0]
    exitCode = process.returncode

    if exitCode == 0 or killed:
        return output
    else:
        raise subprocess.CalledProcessError(command, exitCode)

exe_dir = os.environ['NATIVELIBS']
exe = os.path.join(exe_dir, 'libpython3.7m.so')
lib_dir = os.path.join(os.environ['PYTHONHOME'], 'lib')
bin_dir = os.path.join(os.environ['PYTHONHOME'], 'bin')

if os.environ['PATH']:
    os.environ['PATH'] += ':'
os.environ['PATH'] += exe_dir + ":" + bin_dir
os.environ['LD_LIBRARY_PATH'] = lib_dir

python_links = ['python', 'python3', 'python3.7']
for link in python_links:
    try:
        full = os.path.join(bin_dir, link)
        os.unlink(full)
        os.symlink(exe, full)
    except OSError:
        pass

#TODO offline initialization
try:
    import pip
except ImportError:
    import ensurepip
    ensurepip._main()
    import pip

try:
    try:
        import requests
    except ImportError:
        print('installing requests setuptools wheel')
        execute([exe, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel', 'requests'], kill_phrases=INSTALL_PHRASES)
        import requests
except Exception:
    pass #optional packages

upgrade = False
tar = os.path.join(os.environ['TMP'], 'appy.tar.gz')
try:
    import appy
    existing_version = StrictVersion(appy.__version__)
    available_version = StrictVersion(tar_version(tar))
    print(f'versions - existing: {existing_version}, available: {available_version}')
    if existing_version != available_version:
        upgrade = True
        raise ImportError('outdated version')
except Exception as e:
    print('error importing appy: ', traceback.format_exc())
    print('installing appy')
    execute([exe, '-m', 'pip', 'uninstall', 'appy' ,'--yes'], kill_phrases=UNINSTALL_PHRASES)
    execute([exe, '-m', 'pip', 'install', os.path.join(os.environ['TMP'], 'appy.tar.gz')], kill_phrases=INSTALL_PHRASES)
    import appy