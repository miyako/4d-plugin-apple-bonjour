$event:=Form event:C388

Case of 
	: ($event=On Load:K2:1)
		
		$params:=New object:C1471("domain";"";"type";"_test._tcp")
		
		Form:C1466.status:=Bonjour Discover ($params)
		Form:C1466.hold:=False:C215
		
		If (Form:C1466.status.success)
			
			$params:=New shared object:C1526("type";Form:C1466.status.type;"id";Form:C1466.status.id)
			
			Use ($params)
				
				$params.window:=Current form window:C827
				$params.method:="update_discovery"
				$params.method_ui:="update_discovery_ui"
				$params.interval:=59
				
			End use 
			
			Form:C1466.worker:=$params.method+"@"+String:C10($params.window)
			
			CALL WORKER:C1389(Form:C1466.worker;$params.method;$params)
			
		End if 
		
	: ($event=On Unload:K2:2)
		
		$status:=Bonjour Clear (Form:C1466.status)
		
		KILL WORKER:C1390(Form:C1466.worker)
		
End case 