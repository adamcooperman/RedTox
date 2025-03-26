"""
Test script for the Friendly_Text_Moderation API.
This verifies that we can connect to the API and get proper responses.
"""
import sys
import json
from gradio_client import Client

def test_api():
    """Test the Friendly_Text_Moderation API."""
    print("Testing Friendly_Text_Moderation API...")
    
    try:
        # Initialize the client
        print("Initializing client...")
        client = Client("duchaba/Friendly_Text_Moderation")
        print("Client initialized successfully!")
        
        # Test the API with a simple message
        test_text = "Hello world!"
        safer_value = 0.02
        
        print(f"Calling API with msg='{test_text}', safer={safer_value}...")
        
        # Make the API call using keyword parameters
        result = client.predict(
            msg=test_text,
            safer=safer_value,
            api_name="/fetch_toxicity_level"
        )
        
        # Process the response
        print("Response received!")
        print("\nAPI Response:")
        print(f"Plot object type: {type(result[0])}")
        print(f"JSON string: {result[1]}")
        
        # Parse the JSON string
        try:
            result_dict = json.loads(result[1])
            print("\nParsed JSON:")
            for key, value in result_dict.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            
        print("\nAPI test completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1) 