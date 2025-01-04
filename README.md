# Pixel Survivors - A No-Assets Game Development Demo

This project demonstrates how to create a simple 2D game without using any external assets (no images, sounds, or other resources). Everything is generated programmatically using Python and Pygame.

## Educational Purpose

This project serves as an educational example of:
- How to create a game when you can't create or download assets
- Basic game development concepts using Pygame
- Procedural generation of graphics and sound
- Simple game architecture and state management

## Features & Implementation Details

### Graphics
- All graphics are basic geometric shapes (rectangles, circles)
- No sprites or textures - everything is drawn using Pygame's primitive shapes
- Simple particle system for effects (basic squares/circles)
- Rudimentary animation through position/size changes
- Fullscreen support (somewhat janky but functional)

### Sound System
- All sounds are synthesized using numpy and pygame.sndarray
- Basic waveform generation (sine waves, noise)
- Simple effects like echo and distortion
- Sounds include:
  - Menu interactions (select, back, confirm)
  - Combat effects (hits, death)
  - Pickup and purchase sounds
  - Level up and game over sounds

### Game Systems
- Basic combat with rectangular hitboxes
- Simple enemy AI (move towards player)
- Rudimentary shop system
- Experience and leveling system
- Basic UI with text rendering
- Menu system with settings

### State Management
- Game state machine (menu, playing, shopping, game over)
- Settings persistence
- Basic pause functionality

## Known Limitations/Quirks
- Very basic collision detection (just rectangle overlap)
- Primitive visual representation (everything is geometric shapes)
- Simple AI behavior
- Basic sound synthesis that might sound rough
- UI elements can be visually basic
- Shop interface is minimal
- Fullscreen implementation has some positioning quirks

## Controls
- WASD or Arrow Keys: Move player
- Mouse: Aim
- Left Click: Attack
- ESC: Pause/Menu
- Space: Interact with shop

## Technical Details
- Written in Python using Pygame
- Uses numpy for sound synthesis
- No external dependencies beyond Pygame and numpy
- All game elements are procedurally generated

## Project Structure
- `src/main.py`: Main game loop and initialization
- `src/game/`: Core game systems
- `src/ui/`: User interface elements
- `src/entities/`: Game entities (player, enemies)
- `src/game/sound_manager.py`: Sound synthesis and management
- `src/game/settings.py`: Game settings and constants

## Educational Value
This project demonstrates:
1. Basic game architecture
2. State management
3. Input handling
4. Procedural generation
5. Sound synthesis
6. Simple physics/collision
7. UI implementation
8. Settings management

## Running the Game
```bash
python src/main.py
```

## Requirements
- Python 3.x
- Pygame
- Numpy

## Credits
Created by ThenerzZ as an educational demonstration

## Note
This is intentionally a bare-bones implementation to demonstrate game development concepts without external assets. It's not meant to be a polished game but rather an educational example of creating something playable with minimal resources. 