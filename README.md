### py2j.vim

###### A vim plugin that can convert Python code into Java code.

---------------

Hmmm, I have a great ideal, but currently it has only one function.

---------------

#### Requirements

* A Python interpreter that can be found in $PATH

#### Features

* Converting Python classes into Java POJO

#### Usage

##### POJO converting

* step 1: write a Python class
* step 2: select it in visual-line mode
* step 3: use the function Py2Pojo via mapped key. Defaul: \<leader\>jp

The Python class should looks like:

```Python
# The class name is the name of the POJO.
# Each attribute have a string value that contains the Java type.

class Pojo:

    attr0 = 'int'
    attr1 = 'String'
    attr2 = 'List<int>'
```

--------------

#### License & Copyright

Void License and Void Copyright. Just do what you want to do.
