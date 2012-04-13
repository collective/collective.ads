from setuptools import setup, find_packages
import os

try:
    # Try reading the version.txt from the product.
    versionfile = open(os.path.join("collecitve", "ads", "version.txt"))
    version = versionfile.read().strip()
    versionfile.close()
except IOError:
    # fallback
    version = '1.0'

setup(name='collective.ads',
      version=version,
      description="Plone Ads",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone Ads',
      author='Four Digits',
      author_email='maarten@fourdigits.nl',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
