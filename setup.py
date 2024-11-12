import os
import urllib.request
import zipfile
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        # Download the zip file
        url = "https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/stewardship/forest-analysis-inventory/software/sindex_dll_v154.zip"
        zip_path = "sindex_dll_v154.zip"

        print("Downloading Sindex DLL...")
        urllib.request.urlretrieve(url, zip_path)

        # Extract the zip file into the correct package directory
        sindex_dir = os.path.join(os.path.dirname(__file__), 'sindex')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sindex_dir)

        # Clean up the zip file
        os.remove(zip_path)

        # Run the standard install process
        install.run(self)


setup(
    name='sindex',
    version='0.1.0',
    description='Python interface for interacting with the Sindex DLL for forestry calculations',
    author='Lukas G. Olson',
    author_email='olson@student.ubc.ca',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sindex': ['sindex64.dll'],  # Updated to reflect DLL directly in 'sindex' directory
    },
    install_requires=[
        # List any additional dependencies here if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows',
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
)