<html>
<head>
    <style type="text/css">
    	${css}
    </style>
</head>
<body> 
	<table width="150px">
%for o in objects :
		<tr>
			<td>Transaction ID</td><td>${o.trans_id}</td>
		</tr>
		<tr>
			<td>Customer</td><td>${o.customer_id.name}</td>
		</tr>
		<tr>
			<td>Date</td><td>${o.trans_date}</td>
		</tr>
		<tr>
			<td>Total Amount</td><td>${o.total_amount}</td>
		</tr>
		<tr>
			<td>Total Item</td><td>${o.total_item}</td>			
		</tr>									
%endfor
	</table>
</body>
</html>