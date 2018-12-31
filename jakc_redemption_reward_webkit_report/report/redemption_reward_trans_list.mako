<html>
<head>
    <style type="text/css">
    	${css}
    </style>
</head>
<body> 
	<table width="100%">
		<tr>
			<th>Date</th>
			<th>Customer</th>
			<th>Reward</th>
			<th>Point</th>
			<th>Booking</th>
			<th>Status</th>
		</tr>							

%for o in objects :		
		<tr>
			<td>${o.trans_date}</td>
			<td>${o.customer_id.name}</td>
			<td>${o.reward_id.name}</td>
			<td>${o.point}</td>
			<td>${o.is_booking}</td>			
			<td>${o.state}</td>
		</tr>
%endfor
	</table>
</body>
</html>