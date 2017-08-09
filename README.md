# pyfst

Python interface to [OpenFst](http://openfst.org)

Documentation: http://pyfst.github.io

[![Build Status](https://travis-ci.org/UFAL-DSG/pyfst.png?branch=master)](https://travis-ci.org/UFAL-DSG/pyfst)

## Installation

1. Install OpenFst 1.3.4 pached with [c++11 patch from Kaldi](http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.3.4.tar.gz)
2. Install requirements ``sudo pip install --upgrade pyyaml pystache cython``
3. Build the fork using `setup.py`

```bash
# Change for your setting needed only if openfst is not in PYTHONPATH
export FST=your/path/to/openfst  
# Build it locally
LIBRARY_PATH=$FST/lib:$FST/lib/fst CPLUS_INCLUDE_PATH=$FST/include \
    python setup.py build_ext --inplace
# or install system wide
LIBRARY_PATH=$FST/lib:$FST/lib/fst CPLUS_INCLUDE_PATH=$FST/include \
    sudo -E python setup.py install

# In both case for further usage set LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$FST/lib:$FST/lib/fst:$LD_LIBRARY_PATH
```

## Basic Usage

```python
import fst

t = fst.Transducer()

t.add_arc(0, 1, 'a', 'A', 0.5)
t.add_arc(0, 1, 'b', 'B', 1.5)
t.add_arc(1, 2, 'c', 'C', 2.5)

t[2].final = 3.5

t.shortest_path() # 2 -(a:A/0.5)-> 1 -(c:C/2.5)-> 0/3.5 
```

The pyfst API is [IPython notebook](http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html)-friendly: the transducers objects are [automatically drawn](http://nbviewer.ipython.org/3835477/) using [Graphviz](http://www.graphviz.org).

## Docker

There is also a Dockerfile so that you can build pyfst and run it within
a Docker image.

Build:

```bash
docker build -t pyfst .
```

Run:

```bash
docker run -p 8888:8888 -v `pwd`/notebooks:/notebooks -it pyfst sh -c "jupyter notebook --ip=0.0.0.0 /notebooks"
```

Jupyter notebooks will be available at http://localhost:8888/tree on your host machine. 

Python examples are in `/pyfst/examples`. You can run them as follows:
```bash
docker run -it pyfst python /pyfst/examples/basic.py
```



## License

Copyright:

- 2013 Victor Chahuneau
- 2013 Ondrej Platek
- 2016 Filip Jurcicek

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
