# This is a sample Python script.
import importlib
import subprocess
import json

# run npm install -g snyk to install snyk globally (requires node.js)
# run 'snyk auth' to login before we start

def get_packages():
    with open('requirements_small.txt') as f:
        plines = f.readlines()
        # pkgs=[]
        # for pline in plines:
        #     package = pline.split("==")
        #     pkgs.append(pline)
    return plines


def package_install(pkg):
        subprocess.run(["pip", "install", "--force-reinstall", "-v", pkg], shell=True)
        subprocess.run(['pip', 'freeze', '>', 'actual_requirements.txt'], shell=True)


def package_check_snyk():
    try:
        print("test")
        result = subprocess.run(['snyk', 'test', "--file=actual_requirements.txt", "--package-manager=pip", '--json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                shell=True)
        vulnerabilities = json.loads(result.stdout.decode('utf8'))['vulnerabilities']
        return vulnerabilities
    except KeyError:
        print("shit it went wrong, no vulnerabilities")
        # print('{} is not installed and has to be installed'.format(p))
        # subprocess.call([sys.executable, '-m', 'pip', 'install', p])

def package_uninstall(pkg):
    try:
        s = importlib.import_module(pkg)
        print('{} has to be uninstalled'.format(pkg))
        subprocess.run(["pip", "uninstall", pkg], shell=True)
    except ImportError:
        print('{} is already uninstalled'.format(pkg))
    finally:
        subprocess.run(['pip', 'freeze', '>', 'actual_requirements.txt'], shell=True)
        print('{} is properly uninstalled'.format(pkg))

if __name__ == '__main__':
    all_vulnerabilities = []
    pkgs = get_packages()[:10]
    for pkg in pkgs:
        print(pkg)
        package_install(pkg)
        vuls = package_check_snyk()
        all_vulnerabilities.append(vuls)
        package_uninstall(pkg)
    print('Security Check packages')
    print(all_vulnerabilities)

