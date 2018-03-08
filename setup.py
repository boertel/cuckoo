from setuptools import setup, find_packages


def get_requirements(env):
    with open('requirements-{}.txt'.format(env)) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


install_requires = get_requirements('base')
dev_requires = get_requirements('dev')
test_requires = get_requirements('test')

version = {}
with open('cuckoo/version.py') as fp:
    exec(fp.read(), version)

setup(
    name='cuckoo',
    version=version['__version__'],
    packages=find_packages(),
    license='Apache 2.0',
    entry_points={
        'console_scrips': ['cuckoo=cuckoo.cli:main'],
    },
    extras_require={
        'dev': dev_requires,
        'tests': test_requires,
    },
    install_requires=install_requires + dev_requires + test_requires,
)
