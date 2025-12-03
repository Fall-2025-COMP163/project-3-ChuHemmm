"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Chu Hemmingway

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Data file not found: {filename}")
    except Exception:
        raise CorruptedDataError(f"Error reading data file.")
    
    quest = {}
    current_block = []

    for line in lines:
        Line = line.strip()
        if Line == "":
            if current_block:
                quest_data = parse_quest_block(current_block)
                quest_id = quest_data["quest_id"]
                quest[quest_id] = quest_data
                current_block = []
        else:
            current_block.append(Line)

    if current_block:
        quest_data = parse_quest_block(current_block)
        quest_id = quest_data["quest_id"]
        quest[quest_id] = quest_data
        
    return quest 

    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Data file not found: {filename}")
    except Exception:
        raise CorruptedDataError(f"Error reading data file.")
    
    items= {}
    current_block = []

    for line in lines: 
        stripped_line=line.strip()
        if stripped_line =="":
            if current_block:
                item_data = parse_item_block(current_block)
                
                validate_item_data(item_data)
                
                item_id = item_data["item_id"]
                items[item_id] = item_data
                current_block = []
        else:
            current_block.append(stripped_line)

    if current_block:
        item_data = parse_item_block(current_block)
        validate_item_data(item_data)
        item_id = item_data["item_id"]
        items[item_id] = item_data
    
    return items

    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = ["quest_id", 
                       "title", 
                       "description", 
                       "reward_xp", 
                       "reward_gold", 
                       "required_level", 
                       "prerequisite"]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
    number_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in number_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Field {field} must be an integer")
    return True
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    # fields can only be item_id, name, type, effect, cost, description
    requried_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in requried_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
    
    #Types can only be weapon, armor, or consumable
    valid_types = ["weapon", "armor", "consumable"]
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
        
    #Cost has to be an interger to work propperly 

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Field cost must be an integer")   
    
    #Used Ai Assistant to help with this part
    #Effect has to be a dictionary with one stat and integer value
    effect = item_dict.get("effect")
    
    if isinstance(effect, str):
        try:
            stat, value = effect.split(":", 1)
            effect = {stat: int(value)}
            item_dict["effect"] = effect
        except Exception:
            raise InvalidDataFormatError("Effect must be in format stat_name:value")
        
    if not isinstance(effect, dict) or len(effect) != 1:
        raise InvalidDataFormatError("Effect must be a dictionary with one stat")
    
    for stat, value in effect.items():
        if not isinstance(value, int):
            raise InvalidDataFormatError("Effect value must be an integer")
    return True 

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    #Createing data file directory if it does not exist
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("data/quests.txt"):
        try: 
            with open("data/quests.txt", "w") as file:
                file.write("QUEST_ID:first_quest\n")
                file.write("TITLE:First Quest\n")
                file.write("DESCRIPTION:This is your first quest.\n")
                file.write("REWARD_XP:100\n")
                file.write("REWARD_GOLD:50\n")
                file.write("REQUIRED_LEVEL:1\n")
                file.write("PREREQUISITE:NONE\n")
        except Exception:
            raise CorruptedDataError("Cannot create quests.txt.")
        
    if not os.path.exists("data/items.txt"):
        try:
            with open("data/items.txt", "w") as file:
                file.write("ITEM_ID:Iron_Sword\n")
                file.write("NAME:Iron Sword\n")
                file.write("TYPE:weapon\n")
                file.write("EFFECT:attack:5\n")
                file.write("COST:100\n")
                file.write("DESCRIPTION:A basic iron sword.\n")
            
        except Exception:
            raise CorruptedDataError("Cannot create items.txt.")


    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # A new quest dictionary is created 
    quest = {}

    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError(f"Quest dosent have : in lines")
        
        key, value = line.split(":", 1)
        
        key = key.strip().lower()
        value = value.strip()

        quest[key] = value

    try:
        quest["reward_xp"] = int(quest["reward_xp"])
        quest["reward_gold"] = int(quest["reward_gold"])
        quest["required_level"] = int(quest["required_level"])
    except Exception:
        raise InvalidDataFormatError("Quest fields must be integers.")
    return quest
        



    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    #Checking for dict format and splitting on :
    try:
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Item dosent have : in lines")
            

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "item_id":
                item["item_id"] = value
            elif key == "name":
                item["name"] = value
            elif key == "type":
                item["type"] = value.lower()
            elif key == "effect":

                stat, amount = value.split(":", 1)
                stat = stat.strip()
                amount = int(amount.strip())
                item["effect"] = {stat.lower(): amount}

            elif key == "cost":
                item["cost"] = int(value)
            elif key == "description":
                item["description"] = value
            else:
                raise InvalidDataFormatError(f"Unknown item field: {key}")
    except ValueError:
        raise InvalidDataFormatError("Item fields have invalid format.")
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item: {e}")
    return item
        
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")
