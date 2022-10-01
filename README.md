# Dandy bot
### Made by Nergan

Dandy is a DnD bot for Discord. It helps to track the locations,
manage interactions with NPCs and create the atmosphere for your
campaign.

None of the arts belong to me.

## Table of Contents

1. [Setting up](#settup)
2. [Abilities](#abilities)
3. [Custom mechanics support](#custom)
4. [Additional info](#info)

## Setting up <a name="settup"></a>

Before Dandy can be used he needs to be added to your
Discord server. Instructions for this can be found
[here](https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/).

### When bot is in your server:

When you have received your token, create file named ".env" with following line:

````
Token=your_token_here
````

### Python environment setup:

Install Anaconda following instructions [here](https://www.anaconda.com/).

Open anaconda promt. Paste following commands.
````
cd path_to_folder_with_Dandy.py

conda create --name Dandy

pip install -r requirements.txt
````

### Creating your own Campaign:

To create your own campaign create a folder with a campaign
name inside campaign folder. Inside *campaign/campaign_name*
create a map.xml file. Follow the example from
*nergan_campaign*. For each NPC you should create a separate
*xml* file.

Music can only be played from YouTube.

### Launch Dandy:

Open anaconda promt and follow the commands.

````
cd path_to_folder_with_Dandy.py

conda activate Dandy

python main.py
````

Press *ctrl+C* to stop execution.

## Abilities: <a name="abilities"></a>

|command | description| example|
|:------:|:----------:|:------:|
| !dice  | Rolls number dices with specified number of sides | !dice 1d20|
| !login | Adds players character into the campaign | !login Nergan |
| !logout | Removes players character from a campaign | !logout Nergan |
| !join_voice | Commands bot to join a voice channel in which you are now. Requires a Admin role| !join_voice |
| !leave_voice | Commands bot to leave a voice channel. Requires a DM role | !leave_voice |
| !play | Plays music of current location. DM role required. | !play |
| !pause | Pauses the music. | !pause |
| !resume | Resumes music. | !resume |
| !volume | Sets volume of the bot. | !volume 50 |
| !set_campaign | Sets campaign by the name of the folder in a campaign folder with a map file. DM role required. | !set_campaign nergan_campaign |
| !set_location | Sets current location. DM role required. | !set_location Arcona |
| !location_photo | Sends a photo of a current location. | !location_photo |
| !interaction | Starts an interaction with npc. DM role required. | !interaction Boar |
| !npc_photo | Sends a photo of a current npc. | !npc_photo |
| !end_interaction | Ends current interaction with npc. DM role required. | !end_interaction |
| !bestiary | Shows information about last npc you interacted with. | !bestiary |
| !battle | Starts battle with current npc. DM role required. | !battle |

## Custom mechanics support: <a name="custom"></a>

Dandy can support you with several custom mechanics by creating atmosphere.

More mechanics will be added in the future.

### General commands:

|Command | Description | Example |
|:------:|:-----------:|:-------:|
| !stop_mechanics | Stops current mechanic. | !stop_mechanics |

### Sanity:

If one your NPCs utilizes sanity mechanic Dandy will keep
track of sanity levels of your players. Sanity goes from 100
to 0. 

Depending on player sanity level he will be receiving
messages from an NPC he's fighting. In the beginning
messages will be short and rare. Less sanity player has
More often he will receive messages. Those messages will
be longer and less readable.

|Command | Description | Example |
|:------:|:-----------:|:-------:|
| !damage_sanity | Deals a certain amount of damage to players sanity level. | !damage_sanity Nergan 20 |
| !heal_sanity | Heals a certain amount of players sanity. | !heal_sanity Nergan 20 |
| !get_sanity | Sends a list of sanity levels of players in a campaign | !get_sanity |

### Nightmare:

If your NPC has an ability to control nightmares, Dandy will
switch music to horror sound effect or send a random
horror picture at a random point in time.

### Illusions:

If NPC has an ability to create illusions, bot will
provide you with 2 commands in order to control names of 
your players

|Command |Description |Example |
|:-------:|:----------:|:-------:|
| !swap | Swaps names of the players randomly | !swap|
| !transform | Switches name of random player to ne the name of the NPC | !transform |

## Additional info <a name="info"></a>

Application can utilize docker functionality:

```
docker build --tag dnd .
```
```
docker run -e "Token=YOUR_TOKEN_HERE" -it dnd
```
#### Have any questions?
Contact the creator in Discord **Nergan#9893**