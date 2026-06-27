# DOVE HUNT #

## Overview
Dove Hunt is a 2-player shooting game which was created using Python and Pygame. 
Players compete to shoot as many doves as possible before the timer runs out

## Technologies Used
- Python 3
- Pygame
- Github
- OBS Studio
- Clipchamp (for editing audio)

## Files
- main.py (the program)
- dove.png (sprite)
- backdrop.png
- leaderboard.txt
- sounds/gun_shot.mp3
- sounds/bird_shot.wav
- sounds/beep_sound.wav
- sounds/rain_loop.wav

## How to run the game
1. Make sure that Python & Pygame are installed
2. Place all required files in the project folder:
   - dove.png
   - backdrop.png
   - sounds/gun_shot.mp3
   - sounds/bird_shot.wav
   - sounds/beep_sound.wav
   - sounds/rain_loop.wav
3. Run the python file
4. Read the instructions and press ENTER to start the game
5. Select a difficulty level (Easy, Medium or Hard)

## Controls
### Player 1
- W - move up
- A - move left
- S - move down
- D - move right
- SPACE - shoot
- Q - change crosshair colour

### Player 2
- Up Arrow - move up
- Left Arrow - move left
- Down Arrow - move down
- Right Arrow - move right
- ENTER - shoot
- P - change crosshair colour

### Additional Controls
- N - toggle night mode
- M - mute/unmute audio
- L - open leaderboard
- ESC - return from leaderboard
- R - restart game (after Game Over)

## Difficulty Levels
### Easy
- Dove Speed = 4
- Spawn Delay = 2000ms
### Medium
- Dove Speed = 7
- Spawn Delay = 1300ms
### Hard
- Dove Speed = 10
- Spawn Delay = 800ms


## Features
- 2-player gameplay
- Difficulty Modes Selection Menu
- Animated main menu
- Dove spawning systems
- Dove hit detection
- Dove falling animation when shot
- Hit flash effect
- "+1" score pop-up effect
- Crosshair colour selection
- Night Mode
- Background music
- Sound Effects
- Mute/Unmute Toggle Option 
- 60-second game timer
- Last 10-seconds warning beeps
- Leaderboard saving/viewing system (.txt file)
- Improved GAME OVER screen
- Winner Detection
- Random Dove Positioning
- Timer colour changes (W -> Y -> R)
- Difficulty-based dove speed and spawn rates
- Restart Game Option
- Crosshair movement controls
- HUD/Scoreboard & Timer Display

## Documentation
- README.md file
- Instructions.txt file

At the end of the game, the scores are saved to:
leaderboard.txt

The file records Player 1 and Player 2 scores, and the winner

## Team Roles
### Timer & Systems 
- Project management and team coordination ​
- Game timer (60 seconds)
- Timer colour changes (white → yellow → red) ​
- Last 10-second warning beep system ​
- Audio setup and loading ​
- Background music system ​
- Mute/unmute audio ​
- Restart game ​
- Game Over detection ​
- Clear crosshairs when game ends ​
- Freeze gameplay when timer reaches zero ​
- Leaderboard saving & loading system ​
- Score file management (leaderboard.txt) ​
- README file ​
- Instructions file (instructions.txt)

### Game Logic
- Dove spawning system​
- Random dove positioning​
- Dove movement system​
- Difficulty settings (Easy, Medium, Hard)​
- Difficulty-based spawn rates​
- Difficulty-based dove speeds​
- Player movement controls​
- Crosshair movement system​
- Hitbox system​
- Collision detection​
- Shooting mechanics​
- Score calculation​
- Dove falling animation after being shot​
- Dove hit flash effect​
- Crosshair boundary limits​
- Dove removal when off-screen​
- Hit effect visuals (+1 score pop-up)​
- Crosshair rendering

### UI & Scoreboard
- Instructions screen​
- Difficulty selection menu​
- Leaderboard screen​
- Player 1 & Player 2 score display​
- Timer display​
- HUD (scoreboard bar) design​
- Game Over screen​
- Winner announcement display​
- Total Dove hit display​
- Restart prompt display​
- Player colour selection display​
- Night mode status display​
- Mute status display​
- Leaderboard navigation display​
- Difficulty menu styling and layout​
- Menu panels and UI borders​
- Animated title effect​
- Crosshair colour customisation display​
- Scoreboard and menu styling​
