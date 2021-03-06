freezing-ironman
================

Stages of development:

1. Identify main features of players. (2Y:3N)
2. Develop 2D twin stick shooter using some of these features as properties.
	*	Develop displaying of players and monsters (Y)
	*	Develop shooting (Y)
	* 	Develop collision detection (Y)
	*	Develop deaths (Y)
	* 	Develop "exploding" effects
	* 	Link in player class
		* 	Tie shots to player properties
		*	Tie damage and health to player properties
		* 	Tie movement to player properties
	* 	Create terrain and link collision detection
	*	Create level structure. Each level should be designed so that different play styles reward players
	*	Create backgrounds
	*	Move and refactor to proper structure
	*	Release game
3. Add recording of moves made and send to the server. 
4. Identify the best way of achieving low latency transfer of recordings. Possible solutions below
	*	Save until end of each "match" and then said
	*	Encode bits onto each request sent to the server
	*	Use bits to represent grouped actions as opposed to send two bits for two actions done in the same timeframe
5. Create bots to play 2D twinstick, sending data to server. Keep running until I have at least ~1000 matches for each bot.
6. Write ML for server to change features of bots
7. While all features not changed, goto 5
8. Create 3D shooter game like CS
9. Port bots and recording code and apply ML here.
10. Create multyplayer version and unleash on the world.