"""
    RTLOC - Manager Lib

    setup.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Frederic Mes <fred@rtloc.com>

"""

from setuptools import setup, Extension

setup(name="api_examples2",
      version="0.0.3",
      description="rtloc api examples",
      author="Frederic Mes @ RTLOC",
      author_email="jasper@rtloc.com",
      packages=["parsers", "parsers.uart", "parsers.uart.python", "parsers.socket", "parsers.socket.Python"],
      include_package_data=True,
      python_requires=">=3.6",
      install_requires=[])
