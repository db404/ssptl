#To run : python example.py
import ssptl

#3 Steps

#1 Get a template
t=ssptl.Template()

#2 Add some data
data={'user':'test@test.com',
'parts':('widget','widgeon','pidgeon','pig-iron'),
'showfooter':True
}
#3 Render it - easy
print t.renderFile('templates/index.tpl',data)
