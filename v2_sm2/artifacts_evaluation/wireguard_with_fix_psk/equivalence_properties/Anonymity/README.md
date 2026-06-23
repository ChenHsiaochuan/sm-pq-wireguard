| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants     | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:      |:-:      |:-:
| Initiator's Anonymity | Psk   |    unbounded		| unbounded   |  none   |	❌		|   30s		| ProVerif
| Initiator's Anonymity | Src   |    unbounded		| unbounded   |  none   |	❌		|   1m1s		| ProVerif
| Initiator's Anonymity | Eic   |    unbounded		| unbounded   |  none   |	❌		|   59s		| ProVerif
| Initiator's Anonymity | Erc & Sic   |    unbounded		| unbounded   |  none   |	✅ 	|   5m22s		| ProVerif
| Responder's Anonymity | Psk   |    unbounded		| unbounded   |  none   |	❌		|   30s		| ProVerif
| Responder's Anonymity | Src   |    unbounded		| unbounded   |  none   |	❌		|   1m3s		| ProVerif
| Responder's Anonymity | Eic   |    unbounded		| unbounded   |  none   |	❌		|   1m3s		| ProVerif
| Responder's Anonymity | Erc & Sic   |    unbounded		| unbounded   |  none   |	✅ 	|   5m15s		| ProVerif
