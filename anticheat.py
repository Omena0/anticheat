"""Anticheat for Fr-client
"""
import psutil
from threading import Thread
from utils import apiGet
from tkinter import messagebox
from time import sleep

banlist_name = {i.lower().strip() for i in apiGet('AntiCheat/banlist/name').split('\n') if i != '' and not i.startswith('#')}
banlist_cmdline = {i.lower().strip() for i in apiGet('AntiCheat/banlist/cmdline').split('\n') if i != '' and not i.startswith('#')}
allowlist = {i.lower().strip() for i in apiGet('AntiCheat/banlist/allowlist').split('\n') if i != '' and not i.startswith('#')}


def anticheat():
    """Starts the anticheat process.
    """
    global ac_thread
    ac_thread = Thread(target=ac)
    ac_thread.start()
    

def isAlive():
    return ac_thread.is_alive()


allowed_exes = {
    "svchost.exe",
    "msmpeng.exe",
    "vmcompute.exe",
    "regsrvc.exe",
    "runtimebroker.exe",
    "vmms.exe",
    "vmmem",
    "winlogon.exe",
    "wininit.exe",
    "logonui.exe",
    "services.exe",
    "ctfmon.exe",
    "explorer.exe",
    "csrss.exe",
    "smss.exe",
    "conhost.exe",
    "lsaiso.exe",
    "audiodg.exe",
    "applicationframehost.exe",
    "dllhost.exe",
    "taskhostw.exe",
    "searchindexer.exe",
    "spotify.exe",
    "code.exe",
    "msedgewebview2.exe",
    "textinputhost.exe",
    "anticheat.py",
    "main.exe",
    "anticheat",
    "python.exe",
    "powertoys.monacopreviewhandler.exe",
    "trustedinstaller.exe",
    "igfxem.exe",
    "nvbackend.exe",
    "searchapp.exe"
}

def terminate(proc:psutil.Process,filter,exe,command=False):
    proc.terminate()
    print(f'Found {proc.name()} [{filter}]')
    Thread(target=msgbox,args=[command,exe,proc,filter]).start()
    
def msgbox(command,exe,proc,filter):
    messagebox.showinfo('Fr-client AntiCheat', f'Disallowed process detected!\
        \n{'Command'if command else 'Executable'}: {exe}\
        \nFilter: {filter}\
        \n\nPlease report this if {proc.name()} should allowed!')


def ac():
    while True:
        for proc in psutil.process_iter():
            try:
                if proc.pid < 300: continue
                name_lower = proc.name().lower()
                cmdline_lower = ' '.join(proc.cmdline()).lower()
                if name_lower in allowed_exes: continue
                if any(i for i in allowlist if i in cmdline_lower): continue
                print(f'Checking: {proc.name()}')

                for name in banlist_name:
                    if name in name_lower:
                        terminate(proc,name,name_lower,False)

                for cmdline in banlist_cmdline:
                    if cmdline in cmdline_lower:
                        terminate(proc,cmdline,cmdline_lower,True)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            #sleep(0.1)
        #sleep(2)





if __name__ == '__main__':
    anticheat()


    while True: ...










__all__ = [anticheat,isAlive]
