import xml.etree.ElementTree
import argparse
import os
from subprocess import call, check_output
from sys import platform

parser = argparse.ArgumentParser(description='Create package links for Nuget helper.')
parser.add_argument('-c', '--config', dest='config', required=True, help='Path to the Nuget package .config file')
parser.add_argument('-p', '--package-dir', dest='packageDir', required=True, help='Path to the directory where Nuget packages are installed')
parser.add_argument('-l', '--link-dir', dest='linkDir', required=True, help='Path to the directory where links to Nuget packages are created')
parser.add_argument('-r', '--params', dest='params', required=False, help='Path to XML parameter file')
args = parser.parse_args()

def loadDictionary(path):
	"""
	Loads a parameter file to a dictionary.
	"""
	if not os.path.exists(path):
		return None

	result = {}

	items = xml.etree.ElementTree.parse(path).getroot()
	for item in items.findall('item'):
		key = item.get('key')
		value = item.get('value')
		result[key] = value

	return result

## LInk parameters.
linkParams = {}
if args.params is not None:
	linkParams = loadDictionary(args.params)

def requireLinkParam(name):
	name = name[4:]
	value = linkParams.get(name)
	if value is None:
		print 'Required parameter %s not found' % (name)
		raise Exception('Required parameter %s not found' % (name))
	return value

def normalizePath(path):
	if platform == 'cygwin':
		return check_output(['cygpath', '-w', path])
	else:
		return path

def makeJunction(source, dest):	
	print 'Create junction: "%s" -> "%s"' % (source, dest)
	call(["rm", "-f", dest])

	if platform == 'cygwin' or platform == 'win32':
		source = source.replace('/', '\\')
		dest = dest.replace('/', '\\')
		call('cmd /C mklink /J "%s" "%s"' % (dest, source), shell=True)
	else:		
		call('ln -s "%s" "%s"' % (source, dest), shell=True)

def processPackageLinkSpec(packageId, packageContentDir, linkDir):
	"""
	Process package.linkspec in package content directory. 
	Return (process status, link name)
	"""
	result = False
	linkNames = packageId

	linkspecFile = os.path.join(packageContentDir, 'package.linkspec')
	if not os.path.exists(linkspecFile):
		return (False, packageId)

	spec = xml.etree.ElementTree.parse(linkspecFile).getroot()

	useChildPackageLinks = False
	if spec.get('useChildPackageLinks'):
		useChildPackageLinks = spec.get('useChildPackageLinks').lower() in ['true', 'yes']

	childPackageLinks = spec.find('childPackageLinks')

	if useChildPackageLinks and childPackageLinks is not None:		
		for link in childPackageLinks.findall('link'):
			childPackageId = link.get('package')
			linkSource = os.path.join(packageContentDir, childPackageId)

			if not link.get('name'):
				childPackageLinkName = os.path.basename(linkSource)
			else:
				childPackageLinkName = link.get('name')

			linkDest = os.path.join(linkDir, childPackageLinkName)
			
			makeJunction(linkSource, linkDest)

		result = True
		linkNames = []
	elif spec.get('name'):
		linkNames = spec.get('name')

	# external package links
	externalPackageLinks = spec.find('externalPackageLinks')
	if externalPackageLinks is not None:
		for link in externalPackageLinks.findall('link'):
			externalPackageId = link.get('package')
			packagePath = link.get('path')

			if externalPackageId.startswith('ref:'):
				externalPackageId = requireLinkParam(externalPackageId)	

			linkSource = os.path.join(os.getcwd(), externalPackageId)
			linkDest = os.path.join(packageContentDir, packagePath)

			# print '%s -> %s' % (externalPackageId, packagePath)
			# print '%s -> %s' % (normalizePath(linkSource), linkDest)			
			makeJunction(normalizePath(linkSource), linkDest)

	return (result, linkNames)


e = xml.etree.ElementTree.parse(args.config).getroot()
for package in e.findall('package'):
	packageId = package.get('id')
	packageVersion = package.get('version')
	
	packageContentDir = os.path.join(args.packageDir, '%s.%s' % (packageId, packageVersion), 'content')
	# source = os.path.join(args.packageDir, '%s.%s' % (packageName, packageVersion), 'content')

	(processed, linkName) = processPackageLinkSpec(packageId, packageContentDir, args.linkDir)

	if not processed:
		linkDest = os.path.join(args.linkDir, linkName)
		makeJunction(packageContentDir, linkDest)
		# call(["rm", "-f", dest])

		# if platform == 'cygwin':
		# 	source = source.replace('/', '\\')
		# 	dest = dest.replace('/', '\\')
		# 	call('cmd /C mklink /J "%s" "%s"' % (dest, source), shell=True)
		# else:
		# 	call('ln -s "%s" "%s"' % (source, dest), shell=True)