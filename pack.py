import os, sys, shutil
sys.path.insert(1,"./COMTool/")
from COMTool import version, i18n
import zipfile
import shutil

linux_out = "comtool_ubuntu_v{}.tar.xz".format(version.__version__)
macos_out = "comtool_macos_v{}.dmg".format(version.__version__)
windows_out = "comtool_windows_v{}.zip".format(version.__version__)

def zip(out, path):
    out = os.path.abspath(out)
    cwd = os.getcwd()
    os.chdir(os.path.dirname(path))
    with zipfile.ZipFile(out,'w', zipfile.ZIP_DEFLATED) as target:
        for i in os.walk(os.path.basename(path)):
            for n in i[2]:
                target.write(os.path.join(i[0],n))
    os.chdir(cwd)

def pack():
    # update translate
    i18n.main("finish")

    if os.path.exists("COMTool/__pycache__"):
        shutil.rmtree("COMTool/__pycache__")

    os.chdir("COMTool")
    if sys.platform.startswith("win32"):
        cmd = 'pyinstaller --hidden-import babel.numbers  --add-data="assets;assets" --add-data="locales;locales" --add-data="../README.MD;./" -i="assets/logo.ico" -w Main.py -n comtool'
    elif sys.platform.startswith("darwin"):
        cmd = 'pyinstaller --hidden-import babel.numbers --add-data="assets:assets" --add-data="locales:locales" --add-data="../README.MD:./" -i="assets/logo.icns" -w Main.py  -n comtool'
    else:
        cmd = 'pyinstaller --hidden-import babel.numbers --add-data="assets:assets" --add-data="locales:locales" --add-data="../README.MD:./" -i="assets/logo.png" -w Main.py  -n comtool'

    os.system(cmd)

    os.chdir("..")
    if sys.platform.startswith("darwin"):
        if os.path.exists("./COMTool/dist/comtool 0.0.0.dmg"):
            os.remove("./COMTool/dist/comtool 0.0.0.dmg")
            
        os.system('npm install --global create-dmg && create-dmg ./COMTool/dist/comtool.app ./COMTool/dist')
        shutil.copyfile("./COMTool/dist/comtool 0.0.0.dmg", macos_out)
    elif sys.platform.startswith("win32"):
        zip(windows_out, "COMTool/dist/comtool")
    else:
        cmd = "cd COMTool/dist && tar -Jcf {} comtool/ && mv {} ../../ && cd ../..".format(linux_out, linux_out)
        os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        os_name = sys.argv[1]
        if os_name == "ubuntu-latest":
            print(linux_out)
        elif os_name == "windows-latest":
            print(windows_out)
        elif os_name == "macos-latest":
            print(macos_out)
        else:
            sys.exit(1)
    else:
        pack()

