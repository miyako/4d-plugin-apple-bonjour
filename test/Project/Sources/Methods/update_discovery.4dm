//%attributes = {"invisible":true,"preemptive":"capable"}
C_OBJECT:C1216($1;$params)

$params:=$1

$status:=Bonjour Status ($params)

CALL FORM:C1391($params.window;$params.method_ui;$status)

DELAY PROCESS:C323(Current process:C322;$params.interval)

CALL WORKER:C1389(Current process name:C1392;Current method name:C684;$params)