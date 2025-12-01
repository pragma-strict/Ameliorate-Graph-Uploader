import requests
import json
import os


def get_user_input():
    """Prompt the user for topic title, description, and app session cookie."""
    # Welcome message
    print("=" * 60)
    print("Ameliorate Graph Uploader")
    print("=" * 60)
    print()
    
    # Get topic title
    topic_title = input("Enter topic title: ").strip()
    if not topic_title:
        raise ValueError("Topic title cannot be empty")
    
    # Get description
    print("\nEnter topic description (press Enter twice when finished):")
    description_lines = []
    while True:
        line = input()
        if line == "" and description_lines and description_lines[-1] == "":
            description_lines.pop()  # Remove the last empty line
            break
        description_lines.append(line)
    description = "\n".join(description_lines).strip()
    if not description:
        raise ValueError("Description cannot be empty")
    
    # Get graph file
    print("\nEnter relative path to graph file (leave blank for default graph.json):")
    graph_file = input().strip()
    if not graph_file:
        graph_file = "graph.json"
    graph_file = os.path.join(os.path.dirname(__file__), graph_file)
    if not os.path.exists(graph_file):
        raise ValueError(f"Graph file {graph_file} does not exist")

    # Get visibility
    print("\nMake the graph visible to everyone? (y/n)")
    visibility = input().strip()
    if visibility == "y":
        visibility = "public"
    elif visibility == "n":
        visibility = "private"
    else:
        raise ValueError("Invalid visibility")

    # Get allow anyone to edit
    print("\nAllow anyone to edit the graph? (y/n)")
    allow_anyone_to_edit = input().strip()
    if allow_anyone_to_edit == "y":
        allow_anyone_to_edit = True
    elif allow_anyone_to_edit == "n":
        allow_anyone_to_edit = False
    else:
        raise ValueError("Invalid allow anyone to edit")

    # Get app session cookie
    print("\nEnter app session cookie:")
    app_session = input().strip()
    if not app_session:
        raise ValueError("App session cookie cannot be empty")
    
    return topic_title, description, graph_file, visibility, allow_anyone_to_edit, app_session



def create_topic(title, description, graph_file, visibility, allow_anyone_to_edit, app_session):
    """Create a topic using the Ameliorate API."""
    # Topic creation data
    topic_create_data = {
        "topic": {
            "title": title,
            "description": description,
            "visibility": visibility,
            "allowAnyoneToEdit": allow_anyone_to_edit
        },
        "quickViews": []
    }
    
    # API endpoint
    url = 'https://ameliorate.app/api/trpc/topic.create'
    
    # Headers for the request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json'
    }
    
    # Cookies (the session token)
    cookies = {
        'appSession': app_session
    }
    
    # Request payload (wrapped in a "json" key as the original curl command does)
    payload = {
        'json': topic_create_data
    }
    
    # Make the API call
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    
    # Check if the request was successful
    response.raise_for_status()  # This will raise an error if the request failed
    
    # Parse the JSON response
    result = response.json()
    
    # Extract the topic ID (equivalent to: jq '.result.data.json.id')
    topic_id = result['result']['data']['json']['id']
    
    return topic_id



def upload_graph(graph_file, topic_id, app_session):
    """Upload a graph to the topic."""
    graph_file_data = open(graph_file, 'r').read()
    graph_file_data = json.loads(graph_file_data)
    
    # Graph upload data
    graph_upload_data = {
        "topicId": topic_id,
        "nodesToCreate": graph_file_data['nodes'],
        "edgesToCreate": graph_file_data['edges']
    }

    # API endpoint
    url = 'https://ameliorate.app/api/trpc/topic.updateDiagram'
    
    # Headers for the request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json'
    }
    
    # Cookies (the session token)
    cookies = {
        'appSession': app_session
    }
    
    # Request payload (wrapped in a "json" key as the original curl command does)
    payload = {
        'json': graph_upload_data
    }
    
    # Make the API call
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    
    # Check if the request was successful
    response.raise_for_status()  # This will raise an error if the request failed
    
    # # Parse the JSON response
    # result = response.json()

    

def main():
    """Main function to run the topic creation script."""
    try:
        # Get user input
        title, description, graph_file, visibility, allow_anyone_to_edit, app_session = get_user_input()
        
        # Create the topic
        print("Creating topic...")
        topic_id = create_topic(title, description, graph_file, visibility, allow_anyone_to_edit, app_session)
        
        # Display result
        print(f"✓ Topic created successfully!")
        print(f"Topic ID: {topic_id}")
        
        # Upload the graph
        print("\nUploading graph...")
        upload_graph(graph_file, topic_id, app_session)
        
        # Display result
        print(f"✓ Graph uploaded successfully!")
        
    except ValueError as e:
        print(f"\n✗ Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\n✗ API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
