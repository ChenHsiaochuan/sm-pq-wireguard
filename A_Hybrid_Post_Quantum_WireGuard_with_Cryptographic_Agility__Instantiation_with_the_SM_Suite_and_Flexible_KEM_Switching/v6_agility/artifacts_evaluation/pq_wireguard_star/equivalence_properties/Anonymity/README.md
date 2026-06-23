| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants     | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:      |:-:      |:-:
| Initiator's Anonymity | Psk   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Initiator's Anonymity | Psk   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Initiator's Anonymity | Siq   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Initiator's Anonymity | Siq   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Initiator's Anonymity | Srq   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Initiator's Anonymity | Srq   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Initiator's Anonymity | Ri   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Initiator's Anonymity | Ri   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Initiator's Anonymity | Rr   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Initiator's Anonymity | Rr   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Initiator's Anonymity | Eiq & Re   |    unbounded		| unbounded   |  none   |	✅ 	|   1s		| ProVerif
| Responder's Anonymity | Psk   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Responder's Anonymity | Psk   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Responder's Anonymity | Srq   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Responder's Anonymity | Srq   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Responder's Anonymity | Ri   |    unbounded		| unbounded   |  none   |	❌		|   1s		| ProVerif
| Responder's Anonymity | Ri   |    1		|  2  |  none |	❌		|   1s		| DeepSec
| Responder's Anonymity | Siq & Rr & Eiq & Re   |    unbounded		| unbounded   |  none   |	✅ 	|   1s		| ProVerif
