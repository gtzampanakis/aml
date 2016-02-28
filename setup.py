from distutils.core import setup

with open('README.md') as readme_file:
	setup(
		name = 'amlang',
		packages = ['aml'],
		version = '1.0.0',
		description = 'Small and simple expression language',
		long_description = readme_file.read(),
		author = 'Giorgos Tzampanakis',
		author_email = 'giorgos.tzampanakis@gmail.com',
		url = 'https://github.com/gtzampanakis/aml', # use the URL to the github repo
		keywords = [
			'programming',
			'language',
			'expression',
		],
		install_requires = [
			'pyPEG2',
		],
		# Full list here: https://pypi.python.org/pypi?:action=list_classifiers
		classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Environment :: Console',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Operating System :: MacOS :: MacOS X',
			'Operating System :: Microsoft :: Windows',
			'Operating System :: POSIX',
			'Programming Language :: Python',
			'Topic :: Software Development :: Compilers',
		],
	)
