//%attributes = {"invisible":true,"preemptive":"incapable"}
C_OBJECT:C1216($1;$status)

$status:=$1

If (Not:C34(Form:C1466.hold))
	
	Form:C1466.status:=$status
	
End if 