//%attributes = {}
$params:=New object:C1471("domain";"local.";"type";"_test._tcp";"name";"Hello World";"port";1904)

$status:=Bonjour Publish ($params)  //isPublished may not exist at this point

$status:=Bonjour Status ($status)  //repeat to poll

For ($i;1;5)
	
	C_BLOB:C604($TXT)
	CONVERT FROM TEXT:C1011(Generate UUID:C1066;"utf-8";$TXT)
	C_TEXT:C284($data)
	BASE64 ENCODE:C895($TXT;$data)
	
	$status.data:=JSON Stringify:C1217(New object:C1471("test";$data))
	
	$status:=Bonjour Update ($status)
	
	DELAY PROCESS:C323(Current process:C322;200)
	
End for 

$status:=Bonjour Clear ($status)