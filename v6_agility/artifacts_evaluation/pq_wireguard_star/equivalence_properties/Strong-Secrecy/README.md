| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants     | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:      |:-:      |:-:
| Strong Secrecy | Siq & Srq & Ri & Rr & Re & Eiq   |    unbounded		| unbounded   |  none   |	✅		|   1s		| ProVerif
| Strong Secrecy | Psk & Siq & Rr & Re & Eiq   |    unbounded		| unbounded   |  none   |	✅		|   1m18s		| ProVerif
| Strong Secrecy | Psk & Srq   |    unbounded		| unbounded   |  none   |	❌		|   1m37s		| ProVerif
| Strong Secrecy | Psk & Srq   |    1		| 2   |  none   |	❌		|   1s		| DeepSec
| Strong Secrecy | Psk & Ri   |    unbounded		| unbounded   |  none   |	❌		|   1m1s		| ProVerif
| Strong Secrecy | Psk & Ri   |    1		| 2   |  none   |	❌		|   1s		| DeepSec
