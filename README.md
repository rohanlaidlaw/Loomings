# Loomings
[![Build Status](https://travis-ci.org/volsci/loomings.svg?branch=master)](https://travis-ci.org/volsci/loomings)

A naval-themed roguelike set in a procedurally generated world, principally inspired by the maritime traditions of 19th century whaling and the writings of Herman Melville. Written in Python 2.7 using the libtcod library.

## Key References
- libtcod (32bit, v1.6.2) | https://bitbucket.org/libtcod/libtcod/downloads/
- libtcod Documentation | http://roguecentral.org/doryen/data/libtcod/doc/1.5.1/index2.html
- Roguelike Tutorial using libtcod | http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

## Getting Started
### Python and libtcod Versioning
A 32bit installation of both Python and libtcod is required.

### Installing Dependencies
The guide for precisely installing libtcod and SDL2 can be followed [here](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_1).

## Testing
### Installing Test Suite
Unit tests are handled by [pytest](https://docs.pytest.org/en/latest/contents.html), which can be installed with `pip install -U pytest`, and the installation checked for sucess with `pytest --version`.

### Running Unit Tests
Unit testing is activated with the command `pytest` in the same directory as the unit tests. All unit tests contained within files named `test_*.py` or `*_test.py` in a given directory will be run. 

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Planning & Game Design
### Synopsis
Player assumes the role of a whaling vessel captain. They are tasked with making their fortune on the seas by hunting sperm whales for their treasured spermacetti. They must shrewdly pick their crew members and decide upon provisions, which manifest themselves as traditional roguelike RPG elements, but also assume more complex form, and then plot a course. While upon the seas, besides dealing with the daily upkeep such as food supplies and wind and sea conditions, the player must also deal with favourable or unfavourable circumstances that arise. The ultimate end-game is to hunt down and defeat Moby Dick, the white whale. 

### Movement & General Gameplay
Let us assume that the reader is versed with basics of the roguelike game. Loomings differs from the traditional rogue-like in the economy of movement. Every tile or tiles traversed represents diminishing food stores, ship wear and changing crew morale. The player must shrewdly pick a course and stick with it lest they earn the ill-favour of their crew. They must cautiously attune to the methods of nautical navigation -- such as examining the position of the sun and stars, referring to purchased maps, inspecting their navigational instruments or conferring with other sea captains.

### The Sea, the Stars & the Weather
The weather and sea conditions can help or harm, and the player must pay attention to temperature, the sky, the season and known currents in order to stay on their course. Tidal waves may damage the ship or throw it off course, or strong currents might thrust a ship into a rocky outcrop as it attempts to come into harbour. Cycling over the game world are the starmap/skyboxes which represent the visible positioning of the skies. The temperature, season, ocean behaviour and time of day are all in fact derived from the position of the skyboxes and are not arbitrarily set. 

### The Crew
There are various roles to fill on the player's ship that contribute to certain meta-attributes. The characters of the world are created both at world generation as well as periodically throughout a live game. They will settle at the various ports in the world and are in fact individuals populated with a variety of traits, abilities, physicality, demands, attributes, likes, dislikes, virtues and vices. The player must exercise judgement in who they hire: a cheaper novice harpooner with excellent physicality, or a more experienced harpooner who is a known thief and has a grudge against the nationality of one of your existing crew members? The collective morale of the crew is affected by events that occur and so the player must pay close heed lest his crew mutiny. Crew members may interact with each other on board for good or bad. 

### Other Ships
The player is not alone in his pursuits. There are NPC ships constantly setting about their procedurally generated paths with their individual aims and goals. The ship AI is constructed to mirror the player's ability as close as possible: other sea-captains will hire available crew members, attempt to plot courses, accrue money and resources, attempt to hunt whales, be host to mutiny or be destroyed by storms (or the white whale) just as the player might. 

### The Whales
At world generation and periodically throughout, many whales will be spawned all of different physically, species and personality. Modelled on the behaviour of actual whales, the NPC whales will move throughout the ocean depending on the time of year, travel in pods and flee from ships. Killed whales must be processed which is another challenge in itself. 

### World Generation
Temperate zones, landmasses and the position of ports are all procedurally generated at the beginning of the game using Perlin Noise. A player will generate a world and then perhaps play multiple playthroughs on the same world. A list of the names of real-world nations and bodies of water are applied to the world, so that while the world does not resemble ours, there is some sense of familiarity with real world history.

### In-game History & NPC Memory
NPC sea-captains and characters will remember who they've seen, where they've been and when. NPC characters may make maps of their movements in previous voyages and where they sighted whales and sell them to players (or other NPCs). Theoretically, this also allows for a rudimentary world history that the player may find their previous efforts chronicled within. 

### Ports
Port-towns are not physically traversable, but are instead a menu of available locations and present NPCs. The player will be presented with a list of locations that can be accesed by different keys. A GUI panel may display other ships anchored in the harbour, and while within say, a tavern, a list of NPC crew members for hire. Depending on how big a role Ports play, or how complex the behaviour governing ownership of ships becomes, the player may find themselves subordinate to investors, part-owners or companies who set the player certain jobs and of course maintain monopoly over receipt of the player's whaling yield. This too should extend to NPC ships. With these components in place, a bustling and intricate socio-economic hierarchy emerges -- one that the player may wish to ascend (perhaps even coming to open a late-game state where they do not brave the seas themselves, but rather employ others to do so...).

### Trade
The economy of the generated world will operate on a fairly simple supply/demand model. The player (and other NPC ships) may fetch better prices for whale oil in one port, but it may prove too difficult or dangerous to travel there. Whether or not the game will be populated with other trade-goods is not decided at this time. Loomings does not set out to be a fully-fledged trade sim, and only seeks to embody the narrative and events of novels such as Moby Dick. Whaling ships were not tradesemen and did not idly flit between port-towns exchanging wares, so this part of the game takes a back seat. It is for this same reason that existential threats in Loomings are whales, crew behaviour and the elements -- there are no pirates planned, and there will be no ship-to-ship combat. 
