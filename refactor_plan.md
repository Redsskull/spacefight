# Game Engine Refactoring Plan

## Current Issues

### God Object Problem
- Character class has too many responsibilities:
  - State management
  - Input handling
  - Combat mechanics
  - Animation control
  - Movement logic
  - Collision detection

### Configuration Issues
- Settings split between config.py and inline constants
- Need better organization of configuration data

## New Directory Structure

src/
├── characters/
│   ├── __init__.py
│   ├── base.py             # Base Character class core logic
│   ├── player_chars.py     # Regar, Susan, Emily, Bart implementations
│   └── traits/
│       ├── __init__.py
│       ├── combat.py       # Combat behavior mixin
│       ├── movement.py     # Movement behavior mixin
│       └── animation.py    # Animation behavior mixin
├── enemies/
│   ├── __init__.py
│   ├── base.py             # Base Enemy class
│   ├── states.py           # Enemy state management
│   └── types/              # Enemy implementations
│       ├── __init__.py
│       ├── basic.py        # Basic enemy types
│       └── boss.py         # Boss enemy types
├── combat/
│   ├── __init__.py
│   ├── attack.py           # Attack mechanics
│   ├── damage.py           # Damage handling
│   └── projectiles.py      # Projectile system
├── graphics/
│   ├── __init__.py
│   ├── sprite_loader.py    # Sprite loading and scaling
│   ├── animator.py         # Animation state machine
│   └── effects.py          # Visual effects
├── config/
│   ├── __init__.py
│   ├── characters.py       # Character-specific settings
│   ├── enemies.py          # Enemy-specific settings
│   ├── combat.py           # Combat-related constants
│   ├── spawning.py         # Enemy spawn configuration
│   ├── graphics.py         # Visual/animation settings
│   └── controls.py         # Input mappings
├── managers/
│   ├── __init__.py
│   ├── character_manager.py # Character lifecycle
│   ├── enemy_manager.py    # Enemy spawning and state
│   ├── combat_manager.py   # Combat resolution
│   └── animation_manager.py # Animation state
└── screens/
    ├── __init__.py
    ├── base.py             # Screen base class
    ├── states.py           # Screen state management
    ├── transitions.py      # Screen transition effects
    └── screens/            # Screen implementations
        ├── __init__.py
        ├── main_menu.py
        └── story.py


## Implementation Plan

### 1. Extract Combat System
- ✅ Create CombatMixin class
- ✅ Move attack logic to dedicated module
- ✅ Implement damage handling system  
- ✅ Build projectile management
- ✅ Implement basic movement tests
- ✅ Set up character trait system

### 2. Separate Animation System
- ✅ Design Animator class basic structure 
- ✅ Extract sprite loading
- ✅ Create animation state machine (Implemented in [`Animator`](graphics/animator.py) with state transitions)
- ✅ Implement AnimationManager (Complete in [`AnimationManager`](managers/animation_manager.py))
- ✅ Handle sprite flipping (Implemented via `should_flip` in [`AnimationMixin`](characters/traits/animations.py))

### 3. Movement System
- ✅ Design MovementMixin
- ✅ Implement basic movement
- ✅ Handle player controls
- ✅ Add position management
- ✅ Set up movement tests
- ✅ Extract boundary checking
- ✅ Add movement state tracking
- ✅ Implement vector utilities  # Can mark this complete since we're using pygame.math.Vector2

### 4. Configuration System
- ✅ Organize by domain
- ✅ Character stats 
- ✅ Combat settings
- ✅ Animation configs
- ✅ Control mappings
- ✅ Proper package structure

### 5. Manager Responsibilities

#### CharacterManager
- ✅ Character lifecycle
- ✅ State tracking
- ✅ Collection management
- ✅ Character initialization

#### CombatManager
- ✅ Damage resolution
- ✅ Projectile management
- ✅ Collision detection
- ✅ Combat state tracking

#### AnimationManager
- ✅ Animation state sync
- ✅ Sprite management
- ✅ Effect coordination

### 6. Screen Management
- [ ] Create screens package structure
- [ ] Move screen implementations to dedicated folder
- [ ] Implement screen state management
- [ ] Add transition system
- [ ] Remove direct screen imports
- [ ] Centralize state handling in Game class
- [ ] Add screen lifecycle hooks
- [ ] Test screen transitions

### 7. Enemy System Refactoring
- ✅ Create enemies package structure
- ✅ Move enemy configs
- ✅ Move to modular system
- ✅ Implement sprite-based collision
- ✅ Integrate animation system

#### EnemyManager Updates 
- ✅ Update imports to use new structure
- ✅ Implement basic enemy logic
- ✅ Add facing direction system
- ✅ Improve spawn management
- [ ] Add wave system (Future)

#### Base Enemy Class
- ✅ Extract core enemy logic
- ✅ Implement state machine
- ✅ Animation integration
- ✅ Sprite management

## Benefits

1. **Improved Testability**
   - Isolated components
   - Clear dependencies
   - Easier mocking
   - ✅ Mockable systems

2. **Better Maintenance**
   - Modular systems
   - Single responsibility
   - Clear interfaces

3. **Code Organization**
   - Logical grouping
   - Reduced file sizes
   - Better navigation

4. **Reduced Complexity**
   - Focused components
   - Clear boundaries
   - Simplified testing

## Implementation Steps

1. **Setup Phase**
   - Create directory structure
   - Setup test framework
   - Initialize base classes

2. **Core Systems**
   - Implement trait system
   - Build component registry
   - Create event system

3. **Migration**
   - Move existing code
   - Update references
   - Fix dependencies

## Implementation Order
1. ✅ Complete Combat System
2. ✅ Complete Movement System 
3. ✅ Basic Animation System
4. ✅ Enemy System Refactor
5. ✅ Configuration System Base
6. [ ] Screen Management Refactor (Next)
7. ✅ Full Animation System (Sprites & Effects Complete)
8. [ ] Wave System (Future)

## Success Metrics

- [✅] Reduced file sizes (Split enemy system)
- [✅] Increased test coverage (Added enemy tests)
- [✅] Clearer dependencies (Modular config system)
- [✅] Easier maintenance (Trait-based system)
- [ ] Better performance (Pending optimization)