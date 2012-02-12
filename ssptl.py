#ssptl - Super Simple Python Templating Language
#LGPL License see http://www.gnu.org/licenses/lgpl-3.0-standalone.html
import os
import os.path

class SSPTLException(Exception):
	pass

class CodeGen:

	def appendO(self,data,cr=True,quote=True):
		if data.strip()=='':
			return 
		data=data.replace("'","\\'")
		if cr:
			data=data+'\\n'
		if quote:
			self.code.append('\t' * self.indent + 'o.append(\'%s\')' % data + '\n')
		else:
			self.code.append('\t' * self.indent + 'o.append(%s)' % data + '\n')

	def appendC(self,data):
		self.code.append('\t' * self.indent + data+'\n')

	def handleCommand(self,command):
		output=False
		if command[0]=='=':
			self.appendO('str(%s)' % command[1:],False,False)
			output=True
		elif command[0:2]=='if':
			self.appendC('if '+command[2:]+':')
			self.indent+=1
		elif command[0:4]=='else':
			self.indent-=1
			self.appendC('else:')
			self.indent+=1
		elif command[0:5]=='end':
			self.indent-=1
		elif command[0:3]=='for':
			self.appendC('for '+command[3:]+':')
			self.indent+=1
		elif command[0:5]=='while':
			self.appendC('while '+command[5:]+':')
			self.indent+=1
		else:
			self.appendC(command)
	
		return output

	def codeStartHandle(self,line):
		
		startCount=0
		endCount=0
		inLine=True
		hasOutput=False

		if line.strip()=='<%':
			self.inCode=True
			return

		while inLine:
			startPos=line.find('<%')
			endPos=line.find('%>')

			
			if startPos>=0:
				if endPos<0:
					raise SSPTLException, 'No end tag'

				self.appendO(line[:startPos],False)
			
				if endPos>=0:
					hasOutput=hasOutput or self.handleCommand(line[startPos+2:endPos])
					line=line[endPos+2:]	

			else:
				inLine=False
				self.appendO(line[endPos+1:],hasOutput)

	def codeEndHandle(self,line):
		if line.strip()=='%>' and self.inCode:
			self.inCode=False
		else:
			raise SSPTLException, 'Code block end tag must be only item on line'
				

	def codeHandle(self,line):
		if line.find('<%')>=0:
			if self.inCode:
				raise SSPTLException, 'Nested <% error'
			else:
				self.codeStartHandle(line)
		else:
			self.codeEndHandle(line)	

	def generate(self,template):
		
		self.indent=0
		lines=template.split('\n')

		self.code=[]

		self.appendC('o=[]')
		self.inCode=False

		for line in lines:		
			if (line.find('<%')<0) and (line.find('%>')) < 0:
				if self.inCode:
					self.appendC(line)
				else:					
					self.appendO(line)
			else:
				self.codeHandle(line)

		self.appendC('result = \'\'.join(o)')
		
		
		return ''.join(self.code)

class Template:

	codeCache={}
	codeGen=CodeGen()

	#If cache=True ssptl templates will cache the compiled template 
	#(much faster) if staticCache is also set to true the cache 
	#will be at the module level - beware thread safety.
	def __init__(self,cache=True,staticCache=True):
		self.cache=cache
		self.staticCache=staticCache
		


	def getFile(self,fileName):
		if os.path.exists(fileName):
			fp=open(fileName,'r')
			data=''.join(fp.readlines())
			fp.close()
			return data
		else:
			raise SSPTLException, 'File Not Found :' + fileName
			

	def preProcess(self,template,depth=0,container='.'):
		
		baseDir=os.path.dirname(container)
		
		if template.find('<%include')>=0:
			lines=[]
			for line in template.split('\n'):
				startPos=line.find('<%include')
				if startPos>=0:
					endPos=line.find('%>')
					fileName=line[startPos+9:endPos].strip()
					if depth<50:
						lines.append(self.preProcess(self.getFile(os.path.join(baseDir,fileName)),depth+1,fileName))
					else:
						raise SSPTLException, 'Circular includes - '+fileName
				else:
					lines.append(line+'\n')
					
			return ''.join(lines)
		else:
			return template	

	def getCode(self,template,id,fileName='.'):
		
		
		if id!=None and self.cache and self.codeCache.has_key(id):
			code=self.codeCache[id]
		else:
			template=self.preProcess(template,container=fileName)
			sourceCode=Template.codeGen.generate(template)
			code=compile(sourceCode,'<string>','exec')
			
			if id!=None and self.cache:
				if self.staticCache:
					Template.codeCache[id]=code
				else:
					self.codeCache[id]=code	
		return code

	#Render a using a string as a template - if you pass in optional id,
	#this will enable caching of the compiled template
	def renderString(self,template,data,id=None):
		
		code=self.getCode(template,id)
		exec(code,data)
		return data['result']

	#Render a file based template
	def renderFile(self,fileName,data):
		
		code=self.getCode(self.getFile(fileName),fileName,fileName)
		exec(code,data)
		return data['result']

	#Clear the template cache
	def clearCache(self):
		if self.staticCache:
			Template.codeCache={}
		else:
			self.codeCache={}

if __name__=='__main__':

	EXAMPLE="""
<%
import random
%>
<html>
  <title><%=title%></title>
  <%if doBody%>
  <body>
  <%for item in items%>
     <p><%=item%></p>
  <%end%>
  <p>this</p>
  <p>is static text</p>
  <ul>
<%
x=0
%>
  <%while x<5%>
  <li><%=random.randint(0,10)%></li>
<%
x+=1
%>
  </ul>
  <%end%>
  </body>
  <%end%>
</html>
"""
	t=Template(cache=False)
	data={'title':'Template Test','items':['cat','dog','mouse'],'doBody':True}
	x=t.renderString(EXAMPLE,data)	
	print x
