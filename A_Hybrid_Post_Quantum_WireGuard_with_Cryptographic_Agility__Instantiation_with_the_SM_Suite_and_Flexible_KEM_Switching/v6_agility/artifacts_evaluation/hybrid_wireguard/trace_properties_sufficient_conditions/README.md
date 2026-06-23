| Security Property    		|  Threat Model     | Number of Sessions   | Number of Honest Participants  | Number of Dishonest Participants| Result     			| Execution Time   | Tool
|---    						|:-:    	|:-:			|:-:     |:-:   |:-:      |:-:      |:-:
| Agreement, Secrecy, Session Uniqueness  | 	no reveal		|   unbounded		| unbounded   |  none |	✅			|   20s | ProVerif    		
| Agreement, Secrecy, Session Uniqueness  | 	minimal defensive models for each property		|   unbounded		| unbounded   |  none|	✅			|   11m53s | Tamarin
| Agreement on InitHello message | Psk & Sic      |    unbounded		| unbounded   |  none |	❌		|   15s		| ProVerif
| Agreement on InitHello message | Psk & Src      |    unbounded		| unbounded   |  none|	❌				|  15s			| ProVerif
| Agreement on InitHello message | Psk & DHsisr      |    unbounded		| unbounded   |  none|	❌				|  28s		| ProVerif
| Agreement on RecHello message | Psk & Srq & Src      |    unbounded		| unbounded   |  none|	❌			|  1m40s  | ProVerif
| Agreement on RecHello message | Psk & Srq & Eic & DHsisr      |    unbounded		| unbounded   |  none|	❌			|  3m7s  | ProVerif
| Agreement on RecHello message | Psk & Srq & Eic & Sic 			|   unbounded		| unbounded   |  none|	❌			|  1m50s  | ProVerif
| Agreement on RecHello message | Psk & Ri & Src 			|   unbounded		| unbounded   |  none|	❌			|  1m1s  | ProVerif
| Agreement on RecHello message | Psk & Ri & Eic & DHsisr 			|   unbounded		| unbounded   |  none|	❌			|  1m40s  | ProVerif
| Agreement on RecHello message | Psk & Ri & Eic & Sic 			|   unbounded		| unbounded   |  none|	❌			|  1m  | ProVerif
| Agreement on Confirm message | Psk & Siq & Sic 			|   unbounded		| unbounded   |  none|	❌			|  31s  | ProVerif
| Agreement on Confirm message | Psk & Siq & Erc & DHsisr 			|   unbounded		| unbounded   |  none|	❌			|  29s  | ProVerif
| Agreement on Confirm message | Psk & Siq & Erc & Src  			|   unbounded		| unbounded   |  none|	❌			|  31s  | ProVerif
| Agreement on Confirm message | Psk & Rr & Sic 			|   unbounded		| unbounded   |  none|	❌			|  23s  | ProVerif
| Agreement on Confirm message | Psk & Rr & Erc & DHsisr 			|   unbounded		| unbounded   |  none|	❌			|  19s  | ProVerif
| Agreement on Confirm message | Psk & Rr & Erc & Src 			|   unbounded		| unbounded   |  none|	❌			|  14s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Srq & Src      |    unbounded		| unbounded   |  none|	❌			|  5s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Srq & Eic & DHsisr      |    unbounded		| unbounded   |  none|	❌			|  8s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Srq & Eic & Sic			|   unbounded		| unbounded   |  none|	❌			|  5s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Ri & Src$ 			|   unbounded		| unbounded   |  none|	❌			|  4s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Ri & Eic & DHsisr 			|   unbounded		| unbounded   |  none|	❌			|  6s  | ProVerif
| Session key Secrecy - Initiator's point of view  | Psk & Ri & Eic & Sic 			|   unbounded		| unbounded   |  none|	❌			|  4s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Siq & Sic 			|   unbounded		| unbounded   |  none|	❌			|  30s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Siq & Erc & DHsisr 			|   unbounded		| unbounded   |  none|	❌			|  27s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Siq & Erc & Src 			|   unbounded		| unbounded   |  none|	❌			|  22s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Rr & Sic$ 			|   unbounded		| unbounded   |  none|	❌			|  22s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Rr & Erc & DHsisr$ 			|   unbounded		| unbounded   |  none|	❌			|  19s  | ProVerif
| Session key Secrecy - Responder's point of view  | Psk & Rr & Erc & Src$ 			|   unbounded		| unbounded   |  none|	❌			|  12s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Siq & Srq & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  2m47s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Siq & Srq & Re 			|   unbounded		| unbounded   |  none|	❌			|  1m28s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Siq & Ri & Eiq      |    unbounded		| unbounded   |  none|	❌			|  1m50s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Siq & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  1m4s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Srq & Rr & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  53s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Srq & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  20s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Rr & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  32s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Src & Erc & Rr & Ri & Re  			|   unbounded		| unbounded   |  none|	❌			|  14s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Siq & Srq & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  6m26s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Siq & Srq & Re 			|   unbounded		| unbounded   |  none|	❌			|  3m6s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Siq & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  3m48s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Siq & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  1m52s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Srq & Rr & Eiq  			|   unbounded		| unbounded   |  none|	❌			|  1m35s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Srq & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  36s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Rr & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  55s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Sic & Rr & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  24s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Siq & Srq & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  5m40s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Siq & Srq & Re 			|   unbounded		| unbounded   |  none|	❌			|  2m21s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Siq & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  3m14s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Siq & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  1m40s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Srq & Rr & Eiq 			|  unbounded		| unbounded   |  none|	❌			|  1m34s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Srq & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  35s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Ri & Rr & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  45s  | ProVerif
| Session key Secrecy - Mutual point of view  | Psk & Eic & Erc & DHsisr & Ri & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  19s  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Siq* & Srq* & Eiq|   unbounded		| unbounded   |  none|	❌			|  55s  | ProVerif
|Session key Forward Secrecy  | Psk* & Src* & Erc & Siq* & Srq* & Re|   unbounded		| unbounded   |  none|	❌			|  38s  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Siq* & Ri & Eiq      |    unbounded		| unbounded   |  none|	❌			|  1m  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Siq* & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  44s  | ProVerif
| Session key Forward Secrecy | Psk* & Src* & Erc & Srq* & Rr & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  36s  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Srq* & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  27s  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Rr & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  41s  | ProVerif
| Session key Forward Secrecy  | Psk* & Src* & Erc & Rr & Ri & Re  			|   unbounded		| unbounded   |  none|	❌			|  36s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Siq* & Srq* & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  1m6s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Siq* & Srq* & Re 			|   unbounded		| unbounded   |  none|	❌			|  38s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Siq* & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  1m14s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Siq* & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  46s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Srq* & Rr & Eiq  			|   unbounded		| unbounded   |  none|	❌			|  1m11s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Srq* & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  34s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Rr & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  1m18s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Sic* & Rr & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  47s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Siq* & Srq* & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  39s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Siq* & Srq* & Re 			|   unbounded		| unbounded   |  none|	❌			|  30s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Siq* & Ri & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  46s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Siq* & Ri & Re 			|   unbounded		| unbounded   |  none|	❌			|  38s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Srq* & Rr & Eiq 			|  unbounded		| unbounded   |  none|	❌			|  27s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Srq* & Rr & Re 			|   unbounded		| unbounded   |  none|	❌			|  21s  | ProVerif
| Session key Forward Secrecy  | Psk* & Eic & Erc & DHsisr* & Ri & Rr & Eiq 			|   unbounded		| unbounded   |  none|	❌			|  35s  | ProVerif
| Bilateral Unknown Key Share attacks resistance  | reveal all keys 			|   unbounded		| unbounded   |  unbounded |	 ✅			|  34s  | ProVerif
| Unilateral Unknown Key Share attacks resistance - Initiator | reveal all keys			|   unbounded		| unbounded   |  unbounded|	 ✅			|  1m25s  | ProVerif
| Unilateral Unknown Key Share attacks resistance - Responder | reveal all keys 			|   unbounded		| unbounded   |  unbounded|	 ✅			|  2m11s  | ProVerif
