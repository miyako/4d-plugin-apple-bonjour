//%attributes = {}
C_OBJECT:C1216(<>P)

If (Not:C34(Bool:C1537(<>P.success)))
	
	$params:=New object:C1471("domain";"local.";"type";"_test._tcp";"name";"TEST";"port";1904)
	
	$status:=Bonjour Publish ($params)  //isPublished may not exist at this point 
	
	<>P:=$status
	
Else 
	$status:=Bonjour Clear (<>P)
	<>P:=Null:C1517
End if 