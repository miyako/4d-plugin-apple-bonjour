//%attributes = {}
$params:=New object:C1471("domain";"";"type";"_airdrop._tcp";"includesPeerToPeer";True:C214)

$status:=Bonjour Discover ($params)

$status:=Bonjour Status ($status)  //repeat to poll

$status:=Bonjour Clear ($status)