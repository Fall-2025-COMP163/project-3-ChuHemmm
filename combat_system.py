"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Chu Hemmingway

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================
def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    if enemy_type == "goblin":
      base_stats =  {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10}
    elif enemy_type == "orc":
       base_stats =  {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25}
    elif enemy_type == "dragon":
       base_stats =  {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    enemy = {"name":"",
             "enemy_type":enemy_type,
             "health":base_stats["health"],
             "max_health":base_stats["health"],
             "strength":base_stats["strength"],
             "magic":base_stats["magic"],
             "xp_reward":base_stats["xp_reward"],
             "gold_reward":base_stats["gold_reward"]}
    if enemy_type == "goblin":
        enemy["name"] = "Goblin"
    elif enemy_type == "orc":
        enemy["name"] = "Orc"
    elif enemy_type == "dragon":
        enemy["name"] = "Dragon"   
    return enemy

    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        enemy = create_enemy("goblin")
    elif 3<= character_level <=5:
        enemy = create_enemy("orc")
    else:
       enemy = create_enemy("dragon")

    return enemy

    
    



    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0

    


        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is already dead and cannot fight")
       
        while self.combat_active == True:
            self.player_turn()
            if self.enemy['health'] <= 0:
                self.combat_active = False

                rewards = get_victory_rewards(self.enemy)
                return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
            
            self.enemy_turn()
            if self.character['health'] <= 0:
                self.combat_active = False
                raise CharacterDeadError("Character has died in battle")
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if self.combat_active == False:
            raise CombatNotActiveError("Player Cannot go when combat is not active")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")

        choice = input("Choose a action 1-3")

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            print(f" You did {damage} damage to the enemy.")

        elif choice == "2":
            if self.character["class"] == "Cleric":
                heal_amount = use_special_ability(self.character, self.enemy)
                print(f"You healed yourself for {heal_amount} health.")
            else:
                damage = use_special_ability(self.character, self.enemy)
                self.apply_damage(self.enemy, damage)
                print(f"You did {damage} damage to the enemy with your special ability.")
        
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                print("You escaped the battle")
                return
            else:
                print("Escape failed countinue fighting.")
        else:  
            print("Invalid choice. Please select a valid action.")

       
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if self.combat_active == False:
            raise CombatNotActiveError("Enemy Cannot go when combat is not active")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        print(f" The enemy did {damage} damage to you")
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
    
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        damage = attacker["strength"] - (defender["strength"] // 4)
        if damage < 1:
            damage = 1 
        return damage
        # TODO: Implement damage calculation
        
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0 
        
        # TODO: Implement damage application
        
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy['health'] <= 0:
            return 'player'
        if self.character['health'] <= 0:
            return 'enemy'
        else:
            return None 
        # TODO: Implement battle end check
        
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        result = random.randint(0,1)
        if result == 1:
            self.combat_active = False
            return True
        else: 
            return False

        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    if character['class'] == "Warrior":
        damage = character["strength"] * 2 
        print("Warrior used Power Strike!")
        return damage 
    
    elif character['class'] == "Mage":
        damage = character["magic"] * 2
        print("Mage used Fireball!")
        return damage 
    
    elif character["class"] == "Rogue":
        chance = random.randint(0,1)
        if chance == 1:
            damage = character["strength"] * 3
            print("Rogue used Critical Strike! It's super effective!")
            return damage
        else:
            print("Rogue Critical strike missed")
            return 0
    
    elif character["class"] == "Cleric":
        heal_amount = 30
        character["health"] += heal_amount
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]
        print("Cleric used Heal!")
        return heal_amount 

    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character["strength"] * 2
    return damage 

    # TODO: Implement power strike
    # Double strength damage
 

def mage_fireball(character, enemy):
    """Mage special ability"""

    damage = character["magic"] * 2 
    return damage 
    
    # TODO: Implement fireball
    # Double magic damage


def rogue_critical_strike(character, enemy): 
    """Rogue special ability"""
    
    if random.randint(0,1) == 1:
        damage = character["strength"] * 3
        return damage
    else: 
        return 0

    # TODO: Implement critical strike
    # 50% chance for triple damage
    

def cleric_heal(character):
    """Cleric special ability"""

    heal_amount = 30 
    character["health"] += heal_amount
    if character ["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    return heal_amount

    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    if character["health"] > 0:
        return True
    else:
        return False 
    # TODO: Implement fight check


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    rewards = {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}
    return rewards
    # TODO: Implement reward calculation
    

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
