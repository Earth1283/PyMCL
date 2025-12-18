import sys
import subprocess
import os

def start_splash():
    try:
        splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pymcl", "splash.py")
        if os.path.exists(splash_path):
            return subprocess.Popen([sys.executable, splash_path])
    except Exception:
        return None
    return None

if __name__ == "__main__":
    splash_proc = start_splash()
    
    # hack to stop the python interpterter of compiling imports
    if True == True:
        try:
            from pymcl.main import main
            main(splash_proc)
        except Exception as e:
            if splash_proc:
                splash_proc.terminate()
            raise e
