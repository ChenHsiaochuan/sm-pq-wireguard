| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants     | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:     |:-:      |:-:      |:-:
| Strong Secrecy | Siq & Srq & Ti & Tr & Ri & Rr & Re & Eiq	 |   unbounded		| unbounded   |  none   |	✅		|   1s		| ProVerif
| Strong Secrecy | Psk & Siq & Tr & Ri & Rr & Re & Eiq	 |   unbounded		| unbounded   |  none   |	✅		|   8s		| ProVerif
| Strong Secrecy | Psk & Siq & Tr & Ti & Rr & Re & Eiq	 |   unbounded		| unbounded   |  none   |	✅		|   8s		| ProVerif
| Strong Secrecy | Psk & Srq	 |   unbounded		| unbounded   |  none   |	❌		|   17s		| ProVerif
| Strong Secrecy | Psk & Srq	 |   1		| 2   |  none   |	❌		|   1s		| DeepSec
| Strong Secrecy | Psk & Ri & Ti	 |   unbounded		| unbounded   |  none   |	❌		|   16s		| ProVerif
| Strong Secrecy | Psk & Ri & Ti	 |   1		| 2   |  none   |	❌		|   1s		| DeepSec
