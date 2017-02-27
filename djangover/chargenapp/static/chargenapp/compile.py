import os
import fnmatch
from htmlmin.minify import html_minify

libspath = 'libs'
mainpath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
#stack overflow prevention: -Xssn, n - stack size. Increase if necessary.
compressorapp = 'java -Xss32m -jar ' + libspath + '/app/js/libs/minifier/yuicompressor-2.4.8.jar '
#yui doesn't like the js reserved words to the point of not working entirely...
jscompressorapp = 'java -Xss64m -jar ' + libspath + '/app/js/libs/minifier/compiler.jar  --language_in ECMASCRIPT5 --charset UTF-8 '

def writeToFile(file, what, filename):
	content = None
	with open(what, 'r') as content_file:
		content = content_file.read()
	file.write('/*module="' + filename + '"*/\n' + content + '\n\n')

def compile_files(p_dir, p_compiles='', p_compile_vars = ''):
	root_path = mainpath + '/js/' + p_dir

	fns = []

	files = [os.path.join(dirpath, f)
		for dirpath, dirnames, files in os.walk(root_path)
		for f in fnmatch.filter(files, '*.js')]

	resultfile = mainpath + '/js/' + p_dir + '/' + p_dir  + '.comp.js'
	resultminfile = mainpath + '/js/' + p_dir + '/' + p_dir  + '.comp.min.js'

	try:
		os.remove(resultfile)
	except OSError:
		pass

	resf = open(resultfile, 'w')
	resf.write('define([' + p_compiles + '], function (' + p_compile_vars + ') { "use strict"; \n')
	resf.write('	return {\n')
	counter = 0
	for file in files:
		print file
		fileFunctionName = os.path.basename(file)[:os.path.basename(file).find('.js')]
		if fileFunctionName != p_dir + '.comp' and fileFunctionName != p_dir and fileFunctionName != p_dir + '.comp.min' and '/exclude/' not in file.replace('\\','/'):
			content = None
			with open(file, 'r') as content_file:
				content = content_file.read()
			if counter > 0:
				resf.write(',')
			resf.write('		' + fileFunctionName + ' : function() {\n')
			resf.write('			' + content)
			resf.write('	}\n\n')
			#resf.write('		' + fileFunctionName + ' : ' + content + '\n\n')

			counter += 1

	resf.write('	}')

	resf.write('	});')
	resf.close()

	cmdstring = (jscompressorapp + ' --js ' + resultfile + ' --js_output_file ' + resultminfile)
	print cmdstring
	os.system(cmdstring)

if __name__ == '__main__':
	compile_files('models')
	compile_files('collections', '"models/models.comp.min"', 'models')
	compile_files('views', '"models/models.comp.min", "collections/collections.comp.min"', 'models, collections')
