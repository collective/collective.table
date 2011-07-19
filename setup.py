from setuptools import setup, find_packages
import os

version = '0.2dev'

setup(name='collective.table',
      version=version,
      description="Table-like content for Plone",
      long_description=open("README").read() + "\n" +
          open(os.path.join("docs", "FUTURE.txt")).read() + "\n" +
          open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='plone table data',
      author='Jarn AS',
      author_email='info@jarn.com',
      url='http://svn.plone.org/svn/collective/collective.table',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'collective.js.datatables',
      ],
      extras_require={
          'test': [
              'mock',
              'plone.app.testing',
              'selenium',
           ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
