modules = {
    'tk':'tk' # tkinter
}

# install modules
for module in modules:
    try:
        __import__(module)
        print(f'{module} is already installed')
    except ImportError:
        print(f'Installing {modules[module]}')
        import subprocess
        subprocess.call(['pip', 'install', modules[module]])
        __import__(module)
    finally:
        globals()[module] = __import__(module)