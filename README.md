freezing-ironman
================

Stages of development:

1. Identify main features of players.
2. Develop 2D twin stick shooter using some of these features as properties.
3. Add recording of moves made and send to the server. 
4. Identify the best way of achieving low latency transfer of recordings. 
	n.b, possible solutions -
		Save until end of each "match" and then said
		Encode bits onto each request sent to the server
		Use bits to represent grouped actions as opposed to send two bits for two actions done in the same timeframe
5. Create bots to play 2D twinstick, sending data to server. Keep running until I have at least ~1000 matches for each bot.
6. Write ML for server to change features of bots
7. While all features not changed, goto 5
8. Create 3D shooter game like CS
9. Port bots and recording code and apply ML here.
10. Create multyplayer version and unleash on the world.