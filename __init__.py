from __future__ import unicode_literals, print_function
import re, itertools, operator, ast
from pypeg2 import *


def create_lang_instance(var_map = None):
	"""
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
	"""

	def py_bool_to_lit(py_bool):
		return parse( 'true' if py_bool else 'false', BooleanLiteral)

	class Identifier(Symbol):
		pass

	if var_map:
		Identifier.grammar = Enum(*[K(v) for v in var_map.iterkeys()]) 

		
	class StringLiteral(str):

		def __new__(cls, s):
			return super(StringLiteral, cls).__new__(cls, ast.literal_eval(s))

		grammar = [re.compile(r'".+?"'), re.compile(r"'.+?'")]

	class IntegerLiteral(int):
		grammar = re.compile(r'-?\d+')

	class FloatLiteral(float):
		grammar = re.compile(r'-?\d+.\d+')

	Comparable = [FloatLiteral, IntegerLiteral, StringLiteral, Identifier]

	class BooleanLiteral(Keyword):
		grammar = Enum(K('true'), K('false'))

	class ComparisonOperator(str):
		grammar = re.compile(r'=|>|<|!=|>=|<=')

	class BooleanFunctionName(Keyword):
		grammar = Enum(K('and'), K('or'))

	class ComparisonOperator(str):
		grammar = re.compile(r'=|>|<|!=|>=|<=')

	class ComparisonOperation(List):
		pass

	ComparisonOperation.grammar = (
			Comparable,
			attr('comp_op', ComparisonOperator),
			Comparable,
	)

	class BooleanOperationSimple(List):
		grammar = (
				flag('negated', K('not')),
				[BooleanLiteral, ComparisonOperation]
		)

	class BooleanOperation(List):
		pass

	BooleanOperation.grammar = (
			BooleanOperationSimple,
			maybe_some(
				BooleanFunctionName,
				BooleanOperationSimple,
			),
	)

	class Expression(List):
		pass

	Expression.grammar = (
			[BooleanOperationSimple, ('(', Expression, ')')],
			maybe_some(
				BooleanFunctionName,
				[BooleanOperationSimple, ('(', Expression, ')')],
			),
	)

	def eval_node(node):
		en = lambda n: eval_node(n)
		if isinstance(node, Identifier):
			return var_map[node]
		elif isinstance(node, StringLiteral):
			return node
		elif isinstance(node, IntegerLiteral):
			return node
		elif isinstance(node, FloatLiteral):
			return node
		elif isinstance(node, BooleanLiteral):
			if node == 'true':
				return True
			elif node == 'false':
				return False
		elif isinstance(node, ComparisonOperation):
			opa, opb = node[0:2]
			if node.comp_op == '=':
				return en(opa) == en(opb)
			elif node.comp_op == '>':
				return en(opa) >  en(opb)
			elif node.comp_op == '<':
				return en(opa) <  en(opb)
			elif node.comp_op == '!=':
				return en(opa) != en(opb)
			elif node.comp_op == '>=':
				return en(opa) >= en(opb)
			elif node.comp_op == '<=':
				return en(opa) <= en(opb)
		elif isinstance(node, BooleanOperationSimple):
			a = en(node[0])
			if node.negated:
				a = not a
			return a
		elif isinstance(node, BooleanOperation):
			if len(node) == 1:
				return en(node[0])

			fn_map = {
					'and': lambda a,b: a and b,
					'or':  lambda a,b: a or  b,
			}

			def simple_eval(tr):
				return py_bool_to_lit(fn_map[tr[1]]( en(tr[0]), en(tr[2]))) 
						

			for fname in ['and', 'or']:
				for i in xrange(1, len(node), 2):
					if node[i] == fname:
						new_self = (
							node[:i-1]
							+ [simple_eval(node[i-1:i+2])]
							+ node[i+2:]
						)
						return en(BooleanOperation(new_self))
		elif isinstance(node, Expression):
			def iter_over_relevant():
				for eli, el in enumerate(node):
					if eli % 2 == 0:
						yield eli, el

			if all(
					isinstance(el, BooleanOperationSimple) 
						or
					isinstance(el, BooleanLiteral) 
					for eli, el in iter_over_relevant()
			):
				res = en(BooleanOperation(node))
				return res
			else:
				for eli, el in iter_over_relevant():
					if isinstance(el, Expression):
						new_self = (
								node[:eli]
								+ [py_bool_to_lit(en(el))]
								+ node[eli+1:]
						)
						return en(Expression(new_self))




	def aml_compile(source):
		return parse(source, Expression)

	def aml_evaluate(aml_c):
		result = eval_node(aml_c)
		return result

	return aml_compile, aml_evaluate

