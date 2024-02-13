"""Anticheat for Fr-client
"""
import psutil
from threading import Thread
from utils import apiGet
from tkinter import messagebox
from time import sleep

banlist_name = {i.lower().strip() for i in apiGet('AntiCheat/banlist/name').split('\n') if i != '' and not i.startswith('#')}
banlist_cmdline = {i.lower().strip() for i in apiGet('AntiCheat/banlist/cmdline').split('\n') if i != '' and not i.startswith('#')}
allowlist = {i.lower().strip() for i in apiGet('AntiCheat/banlist/allowlist') if i != '' and not i.startswith('#')}


def anticheat():
    """Starts the anticheat process.
    """
    global ac_thread
    ac_thread:Thread = Thread(target=ac).start()
    

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
    "anticheat.exe",
    "python.exe",
    "powertoys.monacopreviewhandler.exe",
    "trustedinstaller.exe",
    "igfxem.exe",
    "nvbackend.exe",
    "searchapp.exe"
}


def ac():
    while True:
        for i in psutil.process_iter():
            try:
                if i.pid < 300: continue
                if i.name().lower() in allowed_exes: continue
                if i.name().lower() in allowlist: continue
                print(f'Checking: {i.name()}')
                for name in allowlist:
                    if name in i.name().lower(): continue
                for cmdline in allowlist:
                    if cmdline in ' '.join(i.cmdline()).lower(): continue
                
                for name in banlist_name:
                    if name in i.name().lower():
                        i.terminate()
                        print(f'Found {i.name()} [{name}]')
                        messagebox.showinfo('Fr-client AntiCheat',f'Disallowed process detected!\
                            \nProcess: {i.name()}\
                            \nFilter: {name}\
                            \n\nPlease report this if {i.name()} should not be disallowed!')

                for cmdline in banlist_cmdline:
                    if cmdline in ' '.join(i.cmdline()).lower():
                        i.terminate()
                        print(f'Found {i.name()} [{name}]')
                        messagebox.showinfo('Fr-client AntiCheat',f'Disallowed process detected!\
                            \nCommand: {' '.join(i.cmdline())}\
                            \nFilter: {cmdline}\
                            \n\nPlease report this if {i.name()} should not be disallowed!')
            except: continue
        sleep(2)





if __name__ == '__main__':
    anticheat()


    while True: ...










__all__ = [anticheat]
