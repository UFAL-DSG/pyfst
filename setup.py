import sys
import os
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import yaml
import pystache


templates = [
    ('fst/_fst.pyx.tpl', 'fst/types.yml', 'fst/_fst.pyx'),
    ('fst/libfst.pxd.tpl', 'fst/types.yml', 'fst/libfst.pxd'),
]


class pre_build_ext(build_ext):

    def run(self):
        '''Before building the C++ extension apply the
        templates substitution'''
        print('running pre_build_ext')
        try:
            for templ_name, dic_name, result in templates:
                with open(dic_name, 'r') as d:
                    with open(templ_name, 'r') as t:
                        with open(result, 'w') as r:
                            dic = yaml.load(d)
                            tmpl = t.read()
                            r.write(pystache.render(tmpl, dic))
                            print('Created template %s' % result)
            build_ext.run(self)
        except Exception as e:
            # how to handle bad cases!
            print(e)
            raise e


INC, LIB = [], []
fstdir = os.environ['FST']
assert os.path.isdir(fstdir)
assert os.path.isdir(os.path.join(fstdir, 'include'))
extra_compile_args = ['-std=c++11', '-I{fstdir}/include'.format(fstdir=fstdir)]
extra_link_args = ['-L{}/lib'.format(fstdir), '-L{}/lib/fst'.format(fstdir)]

if sys.platform == 'darwin':
    extra_compile_args.append('-stdlib=libstdc++')
    extra_link_args.append('-stdlib=libstdc++')
    # MacPorts
    if os.path.isdir('/opt/local/lib'):
        INC.append('/opt/local/include')
        LIB.append('/opt/local/lib')


ext_modules = [
    Extension(name='fst._fst',
              extra_compile_args=extra_compile_args,
              extra_link_args=extra_link_args,
              sources=['fst/_fst.pyx'],
              language='c++',
              include_dirs=INC,
              libraries=['fst'],
              library_dirs=LIB,
              )
]


long_description = """
pyfst
=====

A Python interface for the OpenFst_ library.

.. _OpenFst: http://www.openfst.org

- Documentation: http://pyfst.github.io (Original docs)
- Source code: https://github.com/UFAL-DSG/pyfst (Forked)
- Original:    https://github.com/vchahun/pyfst

Example usage::

    import fst

    t = fst.Transducer()

    t.add_arc(0, 1, 'a', 'A', 0.5)
    t.add_arc(0, 1, 'b', 'B', 1.5)
    t.add_arc(1, 2, 'c', 'C', 2.5)

    t[2].final = 3.5

    t.shortest_path() # 2 -(a:A/0.5)-> 1 -(c:C/2.5)-> 0/3.5

"""

setup(
    name='pyfst',
    cmdclass={'build_ext': pre_build_ext},
    version='0.2.3dev',
    url='http://pyfst.github.io',
    author='Victor Chahuneau, Ondrej Platek',
    description='A Python interface to OpenFst.',
    long_description=long_description,
    classifiers=['Topic :: Text Processing :: Linguistic',
                 'Programming Language :: Cython',
                 'Programming Language :: C++',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research'],
    packages=['fst'],
    ext_modules=ext_modules,
    test_suite='nose.collector',
    install_requires=['cython>=0.21', 'pystache>=0.5', 'pyyaml>=3.11'],
    tests_require=['nose>=1.0'],
)
