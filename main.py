"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("Main Menu")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input() 
    
    return int(choice)
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

    character_name = input()
    character_class = input()
    try:
        character_manager.create_character(character_name, character_class)
    except InvalidCharacterClassError:
        print("Invalid character class.")
    character_manager.save_character(current_character)
    
    game_loop()

    


    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character

    saved_characters = character_manager.list_saved_characters()
    print(f"Saved Characters: {saved_characters}")
    character_choice = input()
    try:
        character_manager.load_character(character_choice)
    except (CharacterNotFoundError, SaveFileCorruptedError):
        print("Error Loading Character")
    game_loop()

    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action

    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        else:
            game_running = False
        save_game()
    

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("Game Menu")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    choice = input()
    return int(choice)

    # TODO: Implement game menu
    

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    

    for key in current_character:
        if key not in ['inventory', 'active_quests', 'completed_quests']:
            print(f"{key}: {current_character[key]}")
        else:
            print(f"{key}: {", ".join(current_character[key])}")
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items

    item_id = input()
    item_id = all_items[item_id]
    print(f"Current Inventory: {current_character['inventory']}")
    print("Options:")    
    print("1. Use Item")
    print("2. Equip Weapon")
    print("3. Equip Armor")
    print("4. Drop Item")
    choice = input()
    try:
        if choice == "1":
            inventory_system.use_item(current_character, item_id, all_items)
        elif choice == "2":
            inventory_system.equip_weapon(current_character, item_id, all_items)
        elif choice == "3":
            inventory_system.equip_armor(current_character, item_id, all_items)
        else:
            inventory_system.use_item(current_character, item_id, all_items)
    except (ItemNotFoundError, InventoryFullError):
        print("Inventory Error")



    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    print("Quest Menu")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (for testing)")
    print("7. Back")  

    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    

def explore():
    """Find and fight random enemies"""
    global current_character
    


    try:
        enemy = combat_system.get_random_enemy_for_level(current_character['level'])
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()
    except (InvalidTargetError, CharacterDeadError):
        print("Combat Error")
            
    # TODO: Implement exploration    
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items


    print("Shop Menu")
    print("Available items:")
    for item_id in all_items:
        print(item_id)
    item_id = input()
    print("Options:")    
    print("1. Buy Item")
    print("2. Sell Item")
    print(f"Current gold: {current_character['gold']}")
    choice = input()
    try:
        if choice == "1":
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
        elif choice == "2":
            inventory_system.sell_item(current_character, item_id, all_items[item_id])
    except (InsufficientResourcesError, InventoryFullError, ItemNotFoundError):
        print("Shop Error")
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    character_manager.save_character(current_character)

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except (MissingDataFileError, InvalidDataFormatError):
        game_data.create_default_data_files()


    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    

    print ("Your character has died!") 
    choice = input("Would you like to Revive (costs gold) or Quit? ")
    if choice.lower() == "revive":
        character_manager.revive_character(current_character)
    elif choice.lower() == "quit":
        game_running = False
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
