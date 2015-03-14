# Introduction #

ssptl is a very simple templating language for Python.

## Why ##

Why make another templating language?  ssptl has been used in a number of situations where a 'real' templating language would have been overkill, but more functionality is needed than is available with Python string primitives.

Also as a single file there is no need to 'install' the language on the target system.

It has been used in the 'real world' for stand alone simple web servers, and for XML templating.

## The Good ##

Has all the basic functionality  you would expect - _if_,_while_,_for_,_include_ etc. are all there. Also although not a goal, it seems to be fairly speedy.

## The not so good ##

Errors in templates aren't handled very gracefully.
Does not _always_ respect white spaces, some effort has been made to make it _mostly_ work, but it's been used mainly for HTML and XML where this isn't really an issue.


---


## How to use ##

There is an example included in the source.  Basic syntax:

### outputting data ###

```
<li> <%=myData%> </li>
```

### for loop ###
```
<%for row in rows%>
<p><%=row%></p>
<%end%>
```

### if ###
```
<%if hello%>
<h1> Hi There!</h1>
<%end%>
```

### while loop ###

```
<%while myCondition or not theEnd%>
<tag value='<%=data[4]%>'/>
<%end>
```

### arbitrary Python code ###

Note this can be tricky to use inside while/for/if due to indentation, done right there's no real need to ever do this, however it's available if you need it.
```
<%
def myFunction(data):
  return data.upper()
%>

<%for row in rows%>
<p><%=myFunction(row)%></p>
<%end%>
```


---


## How do you pronounce it ##

err... 'Spittle' ?