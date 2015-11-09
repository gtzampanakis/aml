# aml
Accounting Mini Language --- Small and simple expression language running on Python.

`aml` is a very small programming language running on top of Python. Currently it allows only comparisons between literals and boolean combinations thereof. `aml` is ideal for exposing a powerful but safe interface to users who need to define business rules.

The grammar and parser utilise the [pypeg2](http://fdik.org/pyPEG/) library which must be installed for aml to work.

To use `aml` the programmer creates a "language instace", which currently is a (compile, evaluate) function pair. Calling the compile function yields an object (essentially an AST). This object can then be evaluated. Since the language is very simple, sufficient documentation can be given by example:

	>>> cli = create_lang_instance
	>>> c,e = cli(); e(c('1 = 1'))
	True
	>>> c,e = cli(); e(c('1 = 0'))
	False
	>>> c,e = cli(); e(c('"1" = "1"'))
	True
	>>> c,e = cli({'foo' : 1}); e(c('foo = 1'))
	True
	>>> c,e = cli({'foo' : 1.00}); e(c('foo = 1'))
	True
	>>> c,e = cli({'foo' : 2.24}); e(c('foo = 2.24'))
	True
	>>> c,e = cli(); e(c("'foo'" + '=' + '"foo"'))
	True
	>>> c,e = cli({'foo' : 'foo'}); e(c('foo = "foo"'))
	True
	>>> c,e = cli(); e(c('true or 1=1 and 0=1'))
	True
	>>> c,e = cli(); e(c('(1=1)'))
	True
	>>> c,e = cli(); e(c('(true or 1=1) and 0=1'))
	False
	>>> c,e = cli(); e(c('1 > 1'))
	False
	>>> c,e = cli(); e(c('not 1 > 1'))
	True
	>>> c,e = cli(); e(c('1 != 1'))
	False
	>>> c,e = cli(); e(c('-2 = -2'))
	True
