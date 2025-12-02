"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Chu Hemmingway

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
import character_manager

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    if quest_id in quest_data_dict:

        if character["level"]>= quest_data_dict[quest_id]["required_level"]:
                if quest_data_dict[quest_id]["prerequisite"]!="NONE":
                    if quest_data_dict[quest_id]["prerequisite"] not in character["completed_quests"]:
                        raise QuestRequirementsNotMetError("Quest Requirements Not Met")
                if quest_id not in character["completed_quests"]: 
                    if quest_id not in character["active_quests"]:
                        character["active_quests"].append(quest_id)
                        return True
                else:
                    raise QuestAlreadyCompletedError
        else:
            raise InsufficientLevelError("Insufficient Level")         
    else:
        raise QuestNotFoundError("Quest Not Found")

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    quest = quest_data_dict[quest_id]
    # Check quest is active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    # Remove from active_quests
    character['active_quests'].remove(quest_id)
    # Add to completed_quests
    character['completed_quests'].append(quest_id)
    # Grant rewards (use character_manager.gain_experience and add_gold)
    character_manager.gain_experience(character, quest['reward_xp'])
    character['gold'] += quest['reward_gold']
    # Return reward summary
    return {
        'reward_xp': quest['reward_xp'],
        'reward_gold': quest['reward_gold']
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id in character["active_quests"]:
        character["active_quests"].remove(quest_id)
        return True
    else:
        raise QuestNotActiveError("Not active")
    

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_quest=[]
    for i in character['active_quests']:
        if i in quest_data_dict:
            active_quest.append(quest_data_dict[i])
    return active_quest

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    complete_quest=[]
    for i in character['completed_quests']:
        if i in quest_data_dict:
            complete_quest.append(quest_data_dict[i])
    return complete_quest
    

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    avalable_list=[]
    for quest in quest_data_dict.items():
        
        if character["level"]>= quest["required_level"]:
            if quest["prerequisite"]!="NONE":
                raise QuestRequirementsNotMetError("Quest Requirements Not Met")
            if quest["quest_id"] not in character["completed_quests"]: 
                    if quest["quest_id"] not in character["active_quests"]:
                        avalable_list.append(quest)
    return avalable_list

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    if quest_id in character["completed_quests"]:
        return True
    else:
        return False

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    if quest_id in character["active_quests"]:
        return True
    else:
        return False

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if character["level"]>= quest_data_dict[quest_id]["required_level"]:
                if quest_id not in character["completed_quests"]: 
                    if quest_id not in character["active_quests"]:
                        return True
    else:
        return False

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    list1=[]
    list2=[]
    current=quest_id
    while True:
        found=False
        for q_id,quest in quest_data_dict.items():
            if q_id==current:
                found=True
                list1.append(q_id)
                if quest["prerequisite"]=="NONE":
                    for i in reversed(list1):
                        list2.append(i)
                    return list2
                current=quest["prerequisite"]
                break
        if found==False:
                raise QuestNotFoundError("get_quest_prerequisite_chain Quest not found")

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)
    completed_quests = len(character['completed_quests'])
    percentage = (completed_quests / total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    complete_dict={}
    XP_var=0
    gold=0
    for i in character["completed_quests"]:
        if i in quest_data_dict:
            quest=quest_data_dict[i]
            XP_var+=quest["reward_xp"]
            gold+=quest["reward_gold"]
    complete_dict["total_xp"]=XP_var
    complete_dict["total_gold"]=gold
    return complete_dict

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    lvl_list=[]
    for i in quest_data_dict:
        quest=quest_data_dict[i]
        if min_level<=quest["required_level"]<=max_level:
            lvl_list.append(quest)
    return lvl_list

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Gold: {quest_data['reward_gold']}")
    print(f"Requirments: Level {quest_data['required_level']}")
    # ... etc
    

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    return f'{quest_list["title"]}{quest_list["required_level"]}{quest_list["reward_gold"]}{quest_list["reward_xp"]}'

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    print(f'{len(character["active_quests"])}{len(character["completed_quests"])}{get_quest_completion_percentage(character, quest_data_dict)}{get_total_quest_rewards_earned(character, quest_data_dict)}')

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for i in quest_data_dict:
        quest=quest_data_dict[i]
        pre=quest["prerequisite"]
        if pre!="NONE" and pre not in quest_data_dict:
            continue
        else:
            raise QuestNotFoundError("Quest not found")
    
    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

