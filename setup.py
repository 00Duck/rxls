from setuptools import setup, find_packages

setup(name='rxls',
      version='1.0.0',
      description='Send REST data to ServiceNow using spreadsheets',
      url='https://github.com/00Duck/rxls',
      author='Blake Duckworth',
      author_email='blake@example.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests',
          'pandas'
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['rxls=rxls.main:main'],
      })
