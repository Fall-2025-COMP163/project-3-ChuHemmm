"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Chu Hemmingway

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================
def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    
    if character_class not in ["Warrior","Mage","Rogue","Cleric"]:
        raise InvalidCharacterClassError(f"Class not in valid list: {character_class}")
    
    if character_class == "Warrior":
        base_stats = {"health":120,"strength":15,"magic":5}
    elif character_class =="Mage":
        base_stats = {"health":80,"strength":8,"magic":20}
    elif character_class =="Rogue":
        base_stats = {"health":90,"strength":12,"magic":10}
    elif character_class == "Cleric":
        base_stats ={"health":100, "strength":10,"magic":15}

    character = {"name":name,
    "class":character_class,
     "level":1,
     "health":base_stats["health"],
     "max_health":base_stats["health"],
     "strength":base_stats["strength"],
     "magic":base_stats["magic"],
     "experience":0,
     "gold":100,
     "inventory":[],
     "active_quests":[],
     "completed_quests":[]}
    
    
    return character
    
    
    
    
    
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename= os.path.join(save_directory,f"{character['name']}_save.txt")
    with open (filename,"w") as file:
        file.write(f"NAME: {character['name']}\n")
        file.write(f"CLASS: {character['class']}\n")
        file.write(f"LEVEL: {character['level']}\n")    
        file.write(f"HEALTH: {character['health']}\n")
        file.write(f"MAX_HEALTH: {character['max_health']}\n")
        file.write(f"STRENGTH: {character['strength']}\n")
        file.write(f"MAGIC: {character['magic']}\n")
        file.write(f"EXPERIENCE: {character['experience']}\n")
        file.write(f"GOLD: {character['gold']}\n")
        file.write(f"INVENTORY: {','.join(character['inventory'])}\n")
        file.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
        file.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
    return True 

    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    filename = os.path.join(save_directory,f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Save directory does not exist")
    
    try:
        with open (filename,"r") as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError(f"Could not read save file")
    
    character={}

    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError(f"Format not valid")
        
        key,value = line.strip().split(":",1)
        key = key.strip()
        value = value.strip()

        if key in ["NAME", "CLASS"]:
            character[key.lower()] = value 
    
        elif key in ["LEVEL","HEALTH","MAX_HEALTH","STRENGTH","MAGIC","EXPERIENCE","GOLD"]:
            if not value.isdigit():
                raise InvalidSaveDataError(f"Expected Integer value for {key}")
            character[key.lower()] = int(value)

        elif key in ["INVENTORY","ACTIVE_QUESTS","COMPLETED_QUESTS"]:
            if value == "":
                character[key.lower()] = []
            else:
                character[key.lower()] = value.split(",")
    
        else:
            raise InvalidSaveDataError(f"Unexpected key: {key}")
    
    return character
    



    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []
    
    files = os.listdir(save_directory)

    saved_characters = []

    for filename in files:
        if filename.endswith("_save.txt"):
            name = filename.replace("_save.txt","")
            saved_characters.append(name)
    return saved_characters
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    if not os.path.exists(save_directory):
        raise CharacterNotFoundError(f"Character does not exist")
    
    filepath = os.path.join(save_directory,f"{character_name}_save.txt")

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character does not exist")
    
    os.remove(filepath)
    return True
   
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """

    if character["health"] ==0:
        raise CharacterDeadError("Character is dead and cannot gain experience")
    
    character["experience"] += xp_amount
    level_up_xp = character["level"] * 100
    
    while character["experience"] >= level_up_xp:
        character["experience"] -= level_up_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        level_up_xp = character["level"] * 100

    return character
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_gold
    return character["gold"]
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    missing_health = character["max_health"] - character["health"]
    actual_heal = min(amount, missing_health)
    character["health"] += actual_heal
    return actual_heal
    
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    

def is_character_dead(character):
    
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    if character["health"] <= 0:
        return True 
    else:
        return False
    # TODO: Implement death check
    

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if character["health"] > 0:
        return False 
    
    character["health"] = character["max_health"]//2
    return True 
    # TODO: Implement revival
    # Restore health to half of max_health


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required_keys = ["name", "class", "level", "health", "max_health", "strength", "magic", "experience", "gold", "inventory","active_quests", "completed_quests"]
    numeric_keys = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    list_keys = ["inventory", "active_quests", "completed_quests"]
    
    
    for key in required_keys:
        if key not in character:
            raise InvalidSaveDataError(f"Missing a required key: {key}")
        

    for key in numeric_keys:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"Expected integer for key: {key}")
        
    for key in list_keys:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"Expected list for key: {key}")
        
    return True
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")
