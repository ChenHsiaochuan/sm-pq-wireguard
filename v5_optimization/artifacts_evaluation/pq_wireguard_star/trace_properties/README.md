| Security Property    		|  Minimal Defensive Models     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:     |:-:      |:-:
| Agreement on InitHello message | Psk			| unbounded | unbounded | none |	✅		|   1s		| ProVerif
| Agreement on RecHello message | Psk & (Srq $\vee$ Ri)			| unbounded | unbounded | none |	✅				|  20s			| ProVerif
| Agreement on Confirm message | Psk & (Siq $\vee$ Rr)			| unbounded | unbounded | none |	✅				|  48s			| ProVerif
| Session key Secrecy - Initiator's point of view | Psk & (Srq $\vee$ Ri)			| unbounded | unbounded | none |	✅				|  8s			| ProVerif
| Session key Secrecy - Responder's point of view | Psk & (Siq $\vee$ Rr)			| unbounded | unbounded | none |	✅				|  16s			| ProVerif
| Session key Secrecy - Mutual point of view | 	Psk & (Srq $\vee$ Ri) & (Siq $\vee$ Rr) & (Eiq $\vee$ Re)	| unbounded | unbounded | none |	✅				|  7s			| ProVerif
| Session key Forward Secrecy - Mutual point of view | 	Psk & (Srq $\vee$ Ri) & (Siq $\vee$ Rr) & (Eiq $\vee$ Re)	| unbounded | unbounded | none |	✅				|  3s			| ProVerif
|  Session Uniqueness - Initiator's point of view | $\varnothing$	|	unbounded | unbounded | none	|	✅		|   1s		| ProVerif
|  Session Uniqueness - Responder's point of view | $\varnothing$	 | unbounded | unbounded | none		|	✅		|   1s		| ProVerif
| Bilateral Unknown Key Share attacks resistance  | 	$\varnothing$	| unbounded | unbounded | unbounded |	✅				|  1s			| ProVerif
| Unilateral Unknown Key Share attacks resistance - Initiator  | 	$\varnothing$	| unbounded | unbounded | unbounded |	✅				|  1s			| ProVerif
| Unilateral Unknown Key Share attacks resistance - Responder | $\varnothing$	| unbounded | unbounded | unbounded | 	✅				|  1s			| ProVerif
