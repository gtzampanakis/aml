# aml
Accounting Mini Language --- Small and simple expression language running on Python.

`aml` is a very small programming language running on top of Python. Currently it allows only comparisons between literals and boolean combinations thereof. `aml` is ideal for exposing a powerful but safe interface to users who need to define business rules.

The grammar and parser utilise the [pypeg2](http://fdik.org/pyPEG/) library which must be installed for aml to work.

To use `aml` the programmer creates a "language instace". Calling the compile function yields an object (essentially an AST). This object can then be evaluated directly using the evaluate function or translated to Python or SQL using the respective functions.

Since the language is very simple, sufficient documentation can be given by example:

	>>> lang_instance = create_lang_instance()
	>>> lang_instance.aml_evaluate(lang_instance.aml_compile('1 = 1'))
	True
	>>> li = create_lang_instance()
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> p = li.aml_translate_python
	>>> s = li.aml_translate_sql
	>>> u = li.aml_suggest
	>>> e(c('1 = 0'))
	False
	>>> e(c('"1" = "1"'))
	True
	>>> e(c('(1=1)'))
	True
	>>> e(c('1 > 1'))
	False
	>>> e(c('not 1 > 1'))
	True
	>>> e(c('1 != 1'))
	False
	>>> e(c('-2 = -2'))
	True
	>>> eval(p(c('-2 = -2')))
	True
	>>> eval(p(c('null = null')))
	True
	>>> eval(p(c('1 = null')))
	False
	>>> e(c('"foo" = "foo"'))
	True
	>>> e(c('"foo" = \\'foo\\''))
	True
	>>> e(c('"fo\\'o" = "fo\\'o"'))
	True
	>>> e(c("'foo'" + '=' + '"foo"'))
	True
	>>> li = create_lang_instance({'foo' : 1});
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 1'))
	True
	>>> li = create_lang_instance({'foo' : 1.00})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 1'))
	True
	>>> li = create_lang_instance({'foo' : 2.24})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = 2.24'))
	True
	>>> li = create_lang_instance({'foo' : 'foo'})
	>>> c = li.aml_compile
	>>> e = li.aml_evaluate
	>>> e(c('foo = "foo"'))
	True
	>>> li = create_lang_instance()
	>>> c = li.aml_compile
	>>> p = li.aml_translate_python
	>>> s = li.aml_translate_sql
	>>> s(c('null = null'))
	u'null is null'
	>>> p(c('null = null'))
	u'None == None'
	>>> s(c('null != null'))
	u'null is not null'
	>>> p(c('null != null'))
	u'None != None'
	>>> s(c('5 != 3'))
	u'5 <> 3'
	>>> p(c('5 != 3'))
	u'5 != 3'
	>>> li = create_lang_instance({'foo' : 'bar', 'fo2' : 'ba2'})
	>>> c = li.aml_compile
	>>> p = li.aml_translate_python
	>>> e = li.aml_evaluate
	>>> u = li.aml_suggest
	>>> u('1 = fo')
	[u'fo2', u'foo']
	>>> u('1 = FO')
	[u'fo2', u'foo']
	>>> p(c('null = null'))
	u'None == None'
	>>> e(c('foo = "bar"'))
	True
	>>> e(c('fo2 = "ba2"'))
	True
