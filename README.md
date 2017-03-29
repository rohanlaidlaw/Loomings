# Loomings
A naval-themed roguelike set in a procedurally generated world, principally inspired by the maritime traditions of 19th century whaling and the writings of Herman Melville. Written in Python 2 using the libtcod library.

## Key References
- libtcod (32bit, v1.6.2) | https://bitbucket.org/libtcod/libtcod/downloads/
- libtcod Documentation | http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/index2.html
- Roguelike Tutorial using libtcod | http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

## Planning, Game Design
### Synopsis
Player assumes the role of a whaling vessel captain. They are tasked with making their fortune on the seas by hunting sperm whales for their treasured spermacetti. They must shrewdly pick their crew members and decide upon provisions, which manifest themselves as traditional roguelike RPG elements, but also assume more complex form, and then plot a course. While upon the seas, besides dealing with the daily upkeep such as food supplies and wind and sea conditions, the player must also deal with favourable or unfavourable circumstances that arise. The ultimate end-game is to hunt down and defeat Moby Dick, the white whale. 


### Movement & General Gameplay
Let us assume that the reader is versed with basics of the roguelike game. Loomings differs from the traditional rogue-like in the economy of movement. Every tile or tiles traversed represents diminishing food stores, ship wear and changing crew morale. The player must shrewdly pick a course and stick with it lest they earn the ill-favour of their crew. They must cautiously attune to the methods of nautical navigation -- such as examining the position of the sun and stars, referring to purchased maps, inspecting their navigational instruments or conferring with other sea captains.

### Abilities

### The Sea, the Stars & the Weather
The weather and sea conditions can help or harm, and the player must pay attention to temperature, the sky, the season and known currents in order to stay on their course. Tidal waves may damage the ship or throw it off course, or strong currents might thrust a ship into a rocky outcrop as it attempts to come into harbour. Cycling over the game world are the starmap/skyboxes which represent the visible positioning of the skies. The temperature, season, ocean behaviour and time of day are all in fact derived from the position of the skyboxes and are not arbitrarily set. 

### The Crew
There are various roles to fill on the player's ship that contribute to certain meta-attributes. The characters of the world are created both at world generation as well as periodically throughout a live game. They will settle at the various ports in the world and are in fact individuals populated with a variety of traits, abilities, physicality, pay-rates, attributes, likes, dislikes, virtues and vices. The player must exercise judgement in who they hire: a cheaper novice harpooner with excellent physicality, or a more experienced harpooner who is a known thief and has a grudge against the nationality of one of your existing crew members? The collective morale of the crew is affected by events that occur and so the player must pay close heed lest his crew mutiny. Crew members may interact with each other on board for good or bad. 

### Other Ships
The player is not alone in his pursuits. There are NPC ships constantly setting about their procedurally generated paths with their individual aims and goals. The ship AI is constructed to mirror the player's ability as close as possible: other sea-captains will hire available crew members, attempt to plot courses, accrue money and resources, attempt to hunt whales, or be host to mutiny or be destroyed by storms (or the white whale) just as the player might. 

### The Whales
At world generation and periodically throughout, many whales will be spawned all of different physically, species and personality. Modelled on the behaviour of actual whales, the NPC whales will move throughout the ocean depending on the time of year, travel in pods and flee from ships. Killed whales must be processed which is another challenge in itself. 

### World Generation
Temperate zones, landmasses and the position of ports are all procedurally generated at the beginning of the game. A player will generate a world and then perhaps play multiple playthroughs on the same world. A list of the names of real-world nations and bodies of water are applied to the world, so that while the world does not resemble ours, there is some sense of familiarity with real world history.

### In-game History & NPC Memory
NPC sea-captains and characters will remember who they've seen, where they've been and when. NPC characters may make maps of their movements in previous voyages and where they sighted whales and sell them to players (or other NPCs). Theoretically, this also allows for a rudimentary world history that the player may find their previous efforts chronicled in. 

## Stages of Development
### 1.0 | Basic Gameplay 
- Simple ocean, seas and landmasses are procedurally generated.
- Whale entities are randomly placed, their movements are at this point random and devoid of intelligence or logic
- There is a single port from which the player originates, which cannot be physically explored and is merely a menu interface
- Console populated with relevant player attributes with a functioning mini-map and compass; in-game history writes to text log.
- 

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
- How should the act of the whaling occur? Does it happen on the overworld? Is there a mini-game? Is time frozen?
- How should intra-boat events and interactions occur when the progression of time is taken into account?
- How much time should progress per movement; how far ought a ships be able see around them? If each tile represents the unit of time it takes to move, that needs to be accounted for: how far, in units of time, can a real-life ship see in average conditions?
- How much of the world should be based on Earth? Real-world tradition and history is central to the whaling narrative, but faithfully recreating Earth is tiresome and allows for meta-gaming, defeating the challenge of the game --- generated an entirely random world may lie too far afield of the general aesthetic of a historical game. 
