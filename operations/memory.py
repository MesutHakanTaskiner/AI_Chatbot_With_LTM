from typing import List, Dict


def get_memories(memory: List) -> str:
    """
    Retrieves the memory ID for a given memory name from the provided memory list.
    
    Args:
        memory (List[Dict[str, str]]): A list of dictionaries containing memory information.
        memory_name (str): The name of the memory to search for.
        
    Returns:
        str: The ID of the found memory or an empty string if not found.
    """
    try:
        raw_data = memory[0].get_all()
        data = []

        for i in raw_data["results"]:
            data.append(i["memory"])

        return data
    except Exception as e:
        print(f"Error retrieving memory: {e}")
        return []
    


def update_memory(memory: List, update_data: Dict) -> str:
    """
    Updates the memory value for a given memory name in the provided memory list.
    
    Args:
        memory (List[Dict[str, str]]): A list of dictionaries containing memory information.
        memory_name (str): The name of the memory to update.
        new_value (str): The new value to set for the specified memory name.
        
    Returns:
        str: A message indicating the result of the update operation.
    """

    try:
        raw_data = get_memories(memory)

        data_id = ""
        data_new = ""
        for data in raw_data["results"]:
            if data["memory"] == update_data["old_value"]:
                data_id = data["id"]
                data_new = update_data["new_value"]

        memory[0].update(data_id, data_new)
    except Exception as e:
        print(f"Error updating memory: {e}")
        return "Memory update failed"
    
    return "Memory updated successfully"



def delete_memory(memory: List, delete_data: Dict) -> str:
    """
    Deletes the memory for a given memory name from the provided memory list."
    """
    try:
        raw_data = get_memories(memory)

        data_id = ""
        for data in raw_data["results"]:
            if data["memory"] == delete_data["value"]:
                data_id = data["id"]

        memory[0].delete(memory_id = data_id)
    except Exception as e:
        print(f"Error deleting memory: {e}")
        return "Memory deletion failed"
    
    return "Memory deleted successfully"
    