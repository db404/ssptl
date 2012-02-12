<html>
<head>
	<title>Welcome <%=user%></title>
</head>
<body>
<%include header.tpl%>
<div id='main'>
	<p>You have the following parts</p>
	<ul>
	<%for part in parts%>
	<li><%=part%></li>
	<%end%>
	</ul>
</div>
<%include footer.tpl%>
</body>
</html>
