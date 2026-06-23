| Security Property    		|  Minimal Defensive Models     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:     |:-:      |:-:
| Agreement on InitHello message | Psk			| unbounded | unbounded | none |	✅		|   1s		| ProVerif
| Agreement on RecHello message | Psk & (Srq $\vee$ Ti) & (Srq $\vee$ Ri)			| unbounded | unbounded | none |	✅				|  1m12s			| ProVerif
| Agreement on Confirm message | Psk & (Siq $\vee$ Tr) & (Siq $\vee$ Rr)			| unbounded | unbounded | none |	✅				|  4s			| ProVerif
| Session key Secrecy - Initiator's point of view | Psk & (Srq $\vee$ Ti) & (Srq $\vee$ Ri)			| unbounded | unbounded | none |	✅				|  1m28s			| ProVerif
| Session key Secrecy - Responder's point of view | Psk & (Siq $\vee$ Tr) & (Siq $\vee$ Rr)			| unbounded | unbounded | none |	✅				|  15s			| ProVerif
| Session key Secrecy - Mutual point of view | 	Psk & (Srq $\vee$ Ti) & (Srq $\vee$ Ri) & (Siq $\vee$ Tr) & (Siq $\vee$ Rr) & (Eiq $\vee$ Re)	| unbounded | unbounded | none |	✅				|  35s			| ProVerif
| Session key Forward Secrecy - Mutual point of view | 	Psk & (Srq $\vee$ Ti) & (Srq $\vee$ Ri) & (Siq $\vee$ Tr) & (Siq $\vee$ Rr) & (Eiq $\vee$ Re)	| unbounded | unbounded | none |	✅				|  11s			| ProVerif
|  Session Uniqueness - Initiator's point of view | $\varnothing$	|	unbounded | unbounded | none	|	✅		|   1s		| ProVerif
|  Session Uniqueness - Responder's point of view | $\varnothing$	 | unbounded | unbounded | none		|	✅		|   1s		| ProVerif
| Bilateral Unknown Key Share attacks resistance  | 	Eiq $\vee$ Re	| unbounded | unbounded | unbounded |	✅				|  14s			| ProVerif
| Unilateral Unknown Key Share attacks resistance - Initiator  | 	Psk & (Siq $\vee$ Tr) & (Siq $\vee$ Rr) & (Eiq $\vee$ Re)	| unbounded | unbounded | unbounded |	✅				|  1m37s			| ProVerif
| Unilateral Unknown Key Share attacks resistance - Responder | Psk & (Srq $\vee$ Ti) & (Srq $\vee$ Ri) & (Eiq $\vee$ Re)	| unbounded | unbounded | unbounded | 	✅				|  1m31s			| ProVerif
