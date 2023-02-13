from setuptools import setup, find_namespace_packages


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="spy-utilities",
    description="Command-line utilities for the Spectral Python (SPy) library.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/wairas/spy-utilities",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
    ],
    license='MIT License',
    install_requires=[
        "spectral",
        "matplotlib",
        "numpy",
        "scipy",
    ],
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    entry_points={
        "console_scripts": [
            "spy-envi_info=spy_utils.envi_info:sys_main",
            "spy-envi_to_grayscale=spy_utils.envi_to_grayscale:sys_main",
            "spy-envi_to_mat=spy_utils.envi_to_mat:sys_main",
            "spy-envi_to_rgb=spy_utils.envi_to_rgb:sys_main",
        ]
    },
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
)
