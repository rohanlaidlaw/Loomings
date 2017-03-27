# Loomings
A naval-themed roguelike set in a procedurally generated world, principally inspired by the maritime traditions of 19th century whaling and the writings of Herman Melville. Written in Python 2 using the libtcod library.

## Key References
- libtcod (32bit, v1.6.2) | https://bitbucket.org/libtcod/libtcod/downloads/
- libtcod Documentation | http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/index2.html
- Roguelike Tutorial using libtcod | http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

## Planning, Game Design
### Synopsis
Player assumes the role of a whaling vessel captain. They are tasked with making their fortune on the seas by hunting sperm whales for their treasured spermacetti. They must shrewdly pick their crew members and decide upon provisions, which manifest themselves as traditional roguelike RPG elements, but also assume more complex form, and then plot a course. While upon the seas, besides dealing with the daily upkeep such as food supplies and wind and sea conditions, the player must also deal with favourable or unfavourable circumstances that arise such as coming across herds of whales, holding gam with other whaling vessels or coming into conflict with hostile vessels (the relevence is naval combat and "pirates" to the whaling narrative is limited), storms and crew sentiments. 


### Movement & General Gameplay
Let us assume that the reader is versed with basics of the roguelike game. Loomings differs from the traditional rogue-like in the economy of movement. Every tile or tiles traversed represents diminishing food stores, ship wear and changing crew morale. The player must shrewdly pick a course and stick with it lest they earn the ill-favour of their crew. They must cautiously attune to the methods of nautical navigation -- such as examining the position of the sun or inspecting their compass, sexton, etc. 

## Stages of Development
### 1.0 | Basic Gameplay 
- Simple ocean, seas and landmasses are procedurally generated.
- Whale entities are randomly placed, their movements are at this point random.
- There is a single port from which the player originates, which cannot be physically explored and is merely a menu interface with a list of places to visit.
- Console populated with relevant player attributes with a functioning mini-map and compass, in-game history writes to text log.

## Planning, System Design
As roguelikes are a turn-based game, the scheduling and order of operations for the primary event loop is of key significance. Assuming the game is in its projected completed state, the ordering of the event loop will look roughly as follows:

[WIP]

- handle player movement
- check AI line-of-sight
- handle AI movement
- progress & update weather conditions based on skyboxes and pre-existing conditions
- check for collisions: player, other entities, physical weather conditions (rough waves, currents, winds)
- progress skyboxes and therefore progress time

## Design Problems to Resolve
- How should the act of the whaling ship lowering its boats to hunt a whale, a game within a game, take place?
- How should intra-boat events and interactions occur when the progression of time is taken into account?
- How much time should progress per movement; how far ought a ships be able see around them? Tiles being smaller units of time means the map must be made exponentially larger, whereas with tiles representing larger units of time makes it questionable that a player might be able to see ships several "days" away.
- How much of the world should be based on Earth? Real-world tradition and history is central to the whaling narrative, but faithfully recreating Earth allows for meta-gaming and defeats the challenge of the game --- generated an entirely random world may lie too far afield of the general aesthetic of a historical game. 
