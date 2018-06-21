from setuptools import find_packages, setup

setup(
    name='actuator-demo',
    version='0.1',
    long_description=open('README.md').read(),
    url='https://github.com/steersbob/actuator-demo',
    author='Bob Steers',
    author_email='steers.bob@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
    ],
    keywords='brewing brewpi brewblox embedded plugin service',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'brewblox-service~=0.10',
        'brewblox-devcon-spark',
    ],
    python_requires='>=3.6',
    extras_require={'dev': ['tox', 'pipenv']}
)
