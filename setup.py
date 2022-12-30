from setuptools import setup

setup(name='osm2pgsql_tuner',
      version='0.0.6',
      description='The osm2pgsql-tuner project recommends an osm2pgsql command based on available system resources and the size of the input PBF file.',
      url='https://github.com/rustprooflabs/osm2pgsql-tuner',
      author='RustProof Labs',
      author_email='support@rustprooflabs.com',
      license='MIT',
      packages=['osm2pgsql_tuner'],
      zip_safe=False)