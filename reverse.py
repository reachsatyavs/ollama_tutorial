# Import necessary libraries
import sys

def reverse_string(input_str):
    """
    Reverse a given string and return the reversed version.
    
    Parameters:
    - input_str (str): The string to be reversed
    
    Returns:
    - str: The reversed string
    """
    try:
        # Check if input is indeed a string
        if not isinstance(input_str, str):
            raise ValueError("Input must be a string")
        
        # Reverse the string using slicing
        reversed_str = input_str[::-1]
        
        return reversed_str
    
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main function to demonstrate reversing a string.
    """
    try:
        # Get user input
        user_input = input("Enter a string to reverse: ")
        
        # Call the reverse_string function
        reversed_result = reverse_string(user_input)
        
        # Print the result
        print(f"The reversed string is: {reversed_result}")
    
    except Exception as e:
        print(f"An error occurred during execution: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()