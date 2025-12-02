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
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    try:
        with open(filename, 'r') as file:
            content = file.read()
            quests = {}
            quest_blocks = content.strip().split('\n\n')
            for block in quest_blocks:
                lines = block.strip().split('\n')
                quest_data = parse_quest_block(lines)
                validate_quest_data(quest_data)
                quests[quest_data['quest_id']] = quest_data
            return quests
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")
    except InvalidDataFormatError as e:
        raise e
    except Exception as e:
        raise CorruptedDataError(f"Quest data file '{filename}' is corrupted: {e}")

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
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    try:
        with open (filename, 'r') as file:
            content = file.read()
            items = {}
            item_blocks = content.strip().split('\n\n')
            for block in item_blocks:
                lines = block.strip().split('\n')
                item_data = parse_item_block(lines)
                validate_item_data(item_data)
                items[item_data['item_id']] = item_data
            return items
    except FileNotFoundError:
        raise MissingDataFileError(f"Item data file '{filename}' not found.")
    except InvalidDataFormatError as e:
        raise e
    except Exception as e:
        raise CorruptedDataError(f"Item data file '{filename}' is corrupted: {e}")

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_fields = ['quest_id', 'title', 'description', 'reward_xp',
                       'reward_gold', 'required_level', 'prerequisite']
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")
    # Check that numeric values are actually numbers
    for field in ['reward_xp', 'reward_gold', 'required_level']:
        if field in quest_dict and not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Field '{field}' must be an integer.")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")
    if item_dict['type'] not in ['weapon', 'armor', 'consumable']:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    for field in ['cost']:
        if field in item_dict and not isinstance(item_dict[field], int):
            raise InvalidDataFormatError(f"Field '{field}' must be an integer.")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    data_dir= "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    quest_file = os.path.join(data_dir, "quests.txt")
    item_file = os.path.join(data_dir, "items.txt")
    if not os.path.exists(quest_file):
        with open(quest_file, 'w') as qf:
            qf.write(
                "QUEST_ID: first_quest\n"
                "TITLE: The Beginning\n"
                "DESCRIPTION: Your first quest to get started.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )
    if not os.path.exists(item_file):
        with open(item_file, 'w') as itf:
            itf.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 10\n"
                "DESCRIPTION: Restores 20 health points.\n"
            )
            itf.close()

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
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_data = {}
    for line in lines:
        if ': ' not in line:
            raise InvalidDataFormatError(f"Invalid quest line format: {line}")
        key, value = line.split(': ', 1)
        key = key.strip().lower()
        value = value.strip()
        if key in ['reward_xp', 'reward_gold', 'required_level']:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got: {value}")
        quest_data[key] = value
    return quest_data

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_data = {}
    for line in lines:
        if ': ' not in line:
            raise InvalidDataFormatError(f"Invalid item line format: {line}")
        key, value = line.split(': ', 1)
        key = key.strip().lower()
        value = value.strip()
        if key in ['cost']:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got: {value}")
        item_data[key] = value
    return item_data


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

