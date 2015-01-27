#! /usr/bin/python

import sys, os
from distutils.core import setup, Extension, Command
from distutils.util import get_platform
import versioneer

versioneer.VCS = "git"
versioneer.versionfile_source = "python-src/curve25519/_version.py"
versioneer.versionfile_build = "curve25519/_version.py"
versioneer.tag_prefix = ""
versioneer.parentdir_prefix = "curve25519-donna-"
cmdclass = {}
cmdclass.update(versioneer.get_cmdclass())

ext_modules = [Extension("curve25519._curve25519",
                         ["python-src/curve25519/curve25519module.c",
                          "curve25519-donna.c"],
                         )]

short_description="Python wrapper for the Curve25519 cryptographic library"
long_description="""\
Curve25519 is a fast elliptic-curve key-agreement protocol, in which two
parties Alice and Bob each generate a (public,private) keypair, exchange
public keys, and can then compute the same shared key. Specifically, Alice
computes F(Aprivate, Bpublic), Bob computes F(Bprivate, Apublic), and both
get the same value (and nobody else can guess that shared value, even if they
know Apublic and Bpublic).

This is a Python wrapper for the portable 'curve25519-donna' implementation
of this algorithm, written by Adam Langley, hosted at
http://code.google.com/p/curve25519-donna/
"""

class Test(Command):
    description = "run tests"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def setup_path(self):
        # copied from distutils/command/build.py
        self.plat_name = get_platform()
        plat_specifier = ".%s-%s" % (self.plat_name, sys.version[0:3])
        self.build_lib = os.path.join("build", "lib"+plat_specifier)
        sys.path.insert(0, self.build_lib)
    def run(self):
        self.setup_path()
        import unittest
        test = unittest.defaultTestLoader.loadTestsFromName("curve25519.test.test_curve25519")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test)
        sys.exit(not result.wasSuccessful())
cmdclass["test"] = Test

class Speed(Command):
    description = "run benchmark suite"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def setup_path(self):
        # copied from distutils/command/build.py
        self.plat_name = get_platform()
        plat_specifier = ".%s-%s" % (self.plat_name, sys.version[0:3])
        self.build_lib = os.path.join("build", "lib"+plat_specifier)
        sys.path.insert(0, self.build_lib)
    def run(self):
        self.setup_path()
        from curve25519.test import test_speed
        test_speed.main()
cmdclass["speed"] = Speed

setup(name="curve25519-donna",
      version=versioneer.get_version(),
      description=short_description,
      long_description=long_description,
      author="Brian Warner",
      author_email="warner-pycurve25519-donna@lothar.com",
      url="http://code.google.com/p/curve25519-donna/",
      license="BSD",
      packages=["curve25519", "curve25519.test"],
      package_dir={"curve25519": "python-src/curve25519"},
      ext_modules=ext_modules,
      cmdclass=cmdclass,
      )
