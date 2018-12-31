<html>
<head>
    <style type="text/css">
    	${css}
    </style>
</head>
<body> 
%for o in objects :
	<table>
		<tr><td><b>Name</b></td><td>:</td><td>${o.name}</td></tr>
		<tr><td><b>Start Date</b></td><td>:</td><td>${o.start_date}</td></tr>
		<tr><td><b>End Date</b></td><td>:</td><td>${o.end_date}</td></tr>
		<tr><td><b>Status</b></td><td>:</td><td>${o.state}</td></tr>										
	</table>
%endfor
</body>
</html>