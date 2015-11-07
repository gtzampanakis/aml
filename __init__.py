from __future__ import unicode_literals, print_function
import re, itertools, operator, ast
from pypeg2 import *


def py_bool_to_lit(py_bool):
	return parse( 'true' if py_bool else 'false', BooleanLiteral)

class Identifier(Symbol):
	pass
	
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

def eval_node(node, var_map):
	en = lambda n: eval_node(n, var_map)
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

def aml_evaluate(aml_c, var_map = None):
	"""
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
	"""
	result = eval_node(aml_c, var_map)
	return result

