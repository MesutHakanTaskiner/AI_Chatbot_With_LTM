from typing import List, Dict

def get_memories(memory: List) -> dict:
    """
    Retrieves all memories from the first Memory object in the list.

    This function assumes that the 'memory' list contains at least one Memory object 
    that provides a 'get_all' method. The returned value is expected to be a dictionary 
    containing memory results.

    Parameters:
    - memory (List): A list expected to contain Memory objects.

    Returns:
    - dict: The dictionary containing all memory entries, or an empty dictionary if retrieval fails.
    """
    try:
        raw_data = memory[0].get_all()
        return raw_data
    except Exception as e:
        print(f"Error retrieving memory: {e}")
        return {}

def update_memory(memory: List, update_data: Dict) -> str:
    """
    Updates a memory entry with a new value.
    
    This function searches through the memory entries retrieved from the first Memory object,
    and if an entry with a matching 'old_value' is found, it updates that entry with 'new_value'.

    Parameters:
    - memory (List): A list expected to contain Memory objects.
    - update_data (Dict): A dictionary containing the keys 'old_value' and 'new_value'.

    Returns:
    - str: A message indicating the success or failure of the memory update.
    """
    try:
        raw_data = get_memories(memory)
        data_id = ""
        data_new = ""
        for data in raw_data.get("results", []):
            if data.get("memory") == update_data.get("old_value"):
                data_id = data.get("id")
                data_new = update_data.get("new_value")
                break  # Once found, exit the loop.
        if data_id:
            memory[0].update(data_id, data_new)
            return "Memory updated successfully"
        else:
            return "No matching memory entry found"
    except Exception as e:
        print(f"Error updating memory: {e}")
        return "Memory update failed"

def delete_memory(memory: List, delete_data: Dict) -> str:
    """
    Deletes a memory entry based on a specified memory value.
    
    This function searches through the memory entries from the first Memory object.
    When it finds an entry that matches the provided 'value' in delete_data, it deletes that memory.

    Parameters:
    - memory (List): A list expected to contain Memory objects.
    - delete_data (Dict): A dictionary containing the key 'value' which specifies which memory to delete.

    Returns:
    - str: A message indicating whether the deletion was successful or if it failed.
    """
    try:
        raw_data = get_memories(memory)
        #print(f"Raw data: {raw_data}")
        #print(f"Delete data: {delete_data}")
        data_id = ""
        for data in raw_data.get("results", []):
            if data.get("memory") == delete_data.get("value"):
                data_id = data.get("id")
                break  # Once found, exit the loop.
        if data_id:
            memory[0].delete(memory_id=data_id)
            return "Memory deleted successfully"
        else:
            return "No matching memory entry found"
    except Exception as e:
        print(f"Error deleting memory: {e}")
        return "Memory deletion failed"
