<html>
<head>
    <style type="text/css">
    	${css}
    </style>
</head>
<body> 
	<table width="100%">
		<tr>
			<th>Transaction ID</th>
			<th>Customer</th>
			<th>Date</th>
			<th>Total Amount</th>
			<th>Total Item</th>
			<th>Status</th>
		</tr>							
<%
	total_amount = 0
%>
					
%for o in objects :		
		<tr>
			<td>${o.trans_id}</td>
			<td>${o.customer_id.name}</td>
			<td>${o.trans_date}</td>
			<td>${o.total_amount}</td>
			<td>${o.total_item}</td>			
			<td>${o.state}</td>
		</tr>
		<%
			total_amount = total_amount + o.total_amount
		%>												
%endfor
	<tr>
		<td></td>
		<td></td>
		<td></td>
		<td>${total_amount}</td>
		<td></td>			
		<td></td>
	</tr>
	</table>
</body>
</html>