//%attributes = {}
C_OBJECT:C1216(<>P;<>D)

If (Bool:C1537(<>P.success))
	
	If (Not:C34(Bool:C1537(<>D.success)))
		
		$params:=New object:C1471("domain";"";"type";"_test._tcp")
		
		$status:=Bonjour Discover ($params)
		
		<>D:=$status
		
	Else 
		
		$status:=Bonjour Status (<>D)
		
		If ($status.success)
			If ($status.services.length>0)
				
				<>D.service:=$status.services[0]
				
				C_BLOB:C604($data)
				SET BLOB SIZE:C606($data;10)
				
				$status:=Bonjour Send (<>D;$data)
				
			End if 
			
		End if 
		
	End if 
	
End if 