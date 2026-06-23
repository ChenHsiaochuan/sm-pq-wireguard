| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants | Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:    |:-:     |:-:      |:-:      |:-:		
| Initiator's Anonymity | no reveal			|   unbounded		| unbounded   |  none|	✅			|   9m31s		| ProVerif			
| Initiator's Anonymity | Diffie-Hellman keys			|   unbounded		| unbounded   |  none|	✅				|  10m16s		| ProVerif
| Initiator's Anonymity | Post-Quantum keys			|   unbounded		| unbounded   |  none|	✅				|  9m55s	| ProVerif
| Initiator's Anonymity | Psk 			|   unbounded		| unbounded   |  none|	❌			|  1m15s  | ProVerif
| Initiator's Anonymity | Sic & Siq 			|   unbounded		| unbounded   |  none|	❌			|  6m25s	| ProVerif
| Initiator's Anonymity | Sic & Rr 			|   unbounded		| unbounded   |  none|	❌			|  11m47s		| ProVerif
| Initiator's Anonymity | Src & Srq			|   unbounded		| unbounded   |  none|	❌			|  3m22s	| ProVerif
| Initiator's Anonymity | Src & Ri			|   unbounded		| unbounded   |  none|	❌			|  6m46s | ProVerif
| Initiator's Anonymity | Eic & Srq			|   unbounded		| unbounded   |  none|	❌			|  3m40s	| ProVerif
| Initiator's Anonymity | Eic & Ri			|   unbounded		| unbounded   |  none|	❌			|  4m26s | ProVerif
| Initiator's Anonymity | Erc & Siq 			|   unbounded		| unbounded   |  none|	❌			|  5m12s | ProVerif
| Initiator's Anonymity | Erc & Rr 			|   unbounded		| unbounded   |  none|	❌			|  7m59s	| ProVerif
| Initiator's Anonymity | Sic & Src & Eic & Erc & Eiq & Re 			|   unbounded		| unbounded   |  none|	✅		|  9m20s | ProVerif			
| Initiator's Anonymity | Sic & Erc & Srq & Eiq & Ri & Re 			|   unbounded		| unbounded   |  none|	✅		|  9m19s | ProVerif
| Initiator's Anonymity | Src & Eic & Siq & Eiq & Rr & Re 			|   unbounded		| unbounded   |  none|	✅		|  9m9s | ProVerif
| Responder's Anonymity | no reveal			|   unbounded		| unbounded   |  none|	✅			|   8m53s | ProVerif
| Responder's Anonymity | Diffie-Hellman keys			|   unbounded		| unbounded   |  none|	✅				|  8m59s	| ProVerif
| Responder's Anonymity | Post-Quantum keys			|   unbounded		| unbounded   |  none|	✅				|  9m		| ProVerif
| Responder's Anonymity | Psk 			|   unbounded		| unbounded   |  none|	❌			|  51s  | ProVerif
| Responder's Anonymity | Src & Srq 			|   unbounded		| unbounded   |  none|	❌			|  1m22s | ProVerif
| Responder's Anonymity | Src & Ri 			|   unbounded		| unbounded   |  none|	❌			|  2m2s  | ProVerif
| Responder's Anonymity | Srq & Eic 			|   unbounded		| unbounded   |  none|	❌			|  1m2s  | ProVerif
| Responder's Anonymity | Eic & Ri 			|   unbounded		| unbounded   |  none|	❌			|  1m57s  | ProVerif
| Responder's Anonymity | Sic & Src & Eic & Erc & Siq & Eiq & Rr & Re 			|   unbounded		| unbounded   |  none|	✅		|  7m53s	| ProVerif
| Responder's Anonymity | Sic & Erc & Siq & Srq & Eiq & Ri & Rr & Re 			|   unbounded		| unbounded   |  none|	✅		|  7m59s | ProVerif
