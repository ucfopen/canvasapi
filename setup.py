import re
from setuptools import setup

# get version number
with open('pycanvas/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='pycanvas',
    version=version,
    description='API wrapper for the Canvas LMS',
    url='https://github.com/ucfopen/PyCanvas',
    author='Techrangers (University of Central Florida)',
    author_email='pycanvas@example.com',
    license='MIT License',
    packages=['pycanvas'],
    include_package_data=True,
    install_requires=['requests'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha'
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License'
        'Operating System :: OS Independent'
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
