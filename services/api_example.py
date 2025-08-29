"""
Example usage of the API class.

This file demonstrates how to use the API class for making HTTP requests.
"""

from services.http_client import API

def example_usage():
    """
    Example of how to use the API class.
    """
    # Initialize the API client
    api = API(
        base_url="https://api.example.com",
        headers={"Content-Type": "application/json"},
        timeout=30,
        max_retries=3,
    )
    
    # Example GET request
    try:
        # Get a list of users
        users = api.get("/users", params={"page": 1, "limit": 10})
        print(f"Users: {users}")
        
        # Get a specific user
        user = api.get("/users/1")
        print(f"User: {user}")
    except Exception as e:
        print(f"Error getting users: {str(e)}")
    
    # Example POST request
    try:
        # Create a new user
        new_user = api.post(
            "/users",
            json_data={
                "name": "John Doe",
                "email": "john.doe@example.com",
                "role": "user",
            },
        )
        print(f"New user created: {new_user}")
    except Exception as e:
        print(f"Error creating user: {str(e)}")
    
    # Example PUT request
    try:
        # Update a user
        updated_user = api.put(
            "/users/1",
            json_data={
                "name": "John Doe Updated",
                "email": "john.updated@example.com",
            },
        )
        print(f"User updated: {updated_user}")
    except Exception as e:
        print(f"Error updating user: {str(e)}")
    
    # Example DELETE request
    try:
        # Delete a user
        result = api.delete("/users/1")
        print(f"User deleted: {result}")
    except Exception as e:
        print(f"Error deleting user: {str(e)}")

# Example with authentication
def example_with_auth():
    """
    Example of how to use the API class with authentication.
    """
    # Initialize the API client with authentication
    api = API(
        base_url="https://api.example.com",
        headers={"Content-Type": "application/json"},
        timeout=30,
        max_retries=3,
        auth=("username", "password"),  # Basic authentication
    )
    
    # Make authenticated requests
    try:
        # Get protected resource
        data = api.get("/protected-resource")
        print(f"Protected data: {data}")
    except Exception as e:
        print(f"Error accessing protected resource: {str(e)}")

# Example with custom headers and timeout
def example_with_custom_options():
    """
    Example of how to use the API class with custom options for specific requests.
    """
    # Initialize the API client
    api = API(
        base_url="https://api.example.com",
        headers={"Content-Type": "application/json"},
        timeout=30,
        max_retries=3,
    )
    
    # Make request with custom headers and timeout
    try:
        # Get data with custom headers and timeout
        data = api.get(
            "/data",
            headers={"Authorization": "Bearer token123", "Accept": "application/json"},
            timeout=60,  # Override default timeout for this request
        )
        print(f"Data with custom options: {data}")
    except Exception as e:
        print(f"Error getting data with custom options: {str(e)}")

if __name__ == "__main__":
    print("Running API examples...")
    example_usage()
    example_with_auth()
    example_with_custom_options()