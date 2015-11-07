# aml
Accounting Mini Language --- Small and simple expression language running on Python.

`aml` is a very small programming language running on top of Python. For the time being it allows only comparisons between literals and boolean combinations thereof. aml is ideal for exposing a powerful but safe interface to users who need to define business rules.

The grammar and parser utilise the [pypeg2](http://fdik.org/pyPEG/) library which must be installed for aml to work.

`aml` programs can be compiled programmatically. Compilation yields an object (essentially an AST). This object can then be evaluated. If there are any free variables they are looked up in a dictionary which can be passed to the evaluation function. Since the language is very simple, sufficient documentation can be given by example:

    >>> from aml import aml_compile, aml_evaluate
    >>> aml_evaluate(aml_compile('1 = 1'))
  	True
  	>>> aml_evaluate(aml_compile('1 = 0'))
  	False
  	>>> aml_evaluate(aml_compile('"1" = "1"'))
  	True
  	>>> aml_evaluate(aml_compile('foo = 1'), {'foo' : 1})
  	True
  	>>> aml_evaluate(aml_compile('foo = 1'), {'foo' : 1.00})
  	True
  	>>> aml_evaluate(aml_compile('foo = 2.24'), {'foo' : 2.24})
  	True
  	>>> aml_evaluate(aml_compile("'foo'" + '=' + '"foo"'))
  	True
  	>>> aml_evaluate(aml_compile('foo = "foo"'), {'foo' : 'foo'})
  	True
  	>>> aml_evaluate(aml_compile('true or 1=1 and 0=1'))
  	True
  	>>> aml_evaluate(aml_compile('(1=1)'))
  	True
  	>>> aml_evaluate(aml_compile('(true or 1=1) and 0=1'))
  	False
  	>>> aml_evaluate(aml_compile('1 > 1'))
  	False
  	>>> aml_evaluate(aml_compile('not 1 > 1'))
  	True
  	>>> aml_evaluate(aml_compile('1 != 1'))
  	False
  	>>> aml_evaluate(aml_compile('-2 = -2'))
  	True
