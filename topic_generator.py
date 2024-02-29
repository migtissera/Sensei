import requests
import random

TOPICS = [
    "Culture",
    "Geography",
    "Health",
    "History",
    "Humanities",
    "Mathematics",
    "Nature",
    "People",
    "Philosophy",
    "Religion",
    "Society",
    "Technology",
]


def fetch_deepest_subcategory(category, depth=1, current_depth=0, added_depth=False):
    """Fetches the deepest subcategory from a given Wikipedia category, avoiding lists, by-category groupings, and stubs when possible."""
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "subcat",
        "cmlimit": "max",
        "format": "json",
    }

    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        categorymembers = data['query']['categorymembers']

        valid_subcats = [subcat['title'].replace("Category:", "") for subcat in categorymembers if "list" not in subcat['title'].lower() and "by" not in subcat['title'].lower() and "stubs" not in subcat['title'].lower()]

        if not valid_subcats:  # If no valid subcategories are found, return the original category
            return category

        for _ in range(len(valid_subcats)):  # Attempt to select a valid subcategory
            selected_subcat = random.choice(valid_subcats)

            if current_depth < depth:
                deeper_category = fetch_deepest_subcategory(selected_subcat, depth, current_depth + 1, added_depth)
                if deeper_category != selected_subcat:  # If a deeper valid category is found, return it
                    return deeper_category
            else:
                return selected_subcat  # Return the selected subcategory if at max depth

        return category  # Fallback to the original category if no deeper valid category is found

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch subcategories: {e}")
        return None


def write_topics_file(topics):
    """Writes the topics and their deep subcategories to a file."""
    with open('topics.py', 'w') as f:
        f.write("TOPICS = [\n")
        for topic, subcats in topics.items():
            # Format the topic and its deep subcategories for writing
            formatted_subcats = ", ".join(subcats)
            f.write(f'  "{topic} - {formatted_subcats}",\n')
        f.write("]\n")


# Main script
if __name__ == "__main__":
    detailed_topics = {}
    for topic in TOPICS:
        detailed_topics[topic] = []
        for _ in range(6):  # Repeat to get four deep subcategories
            deepest_subcategory = fetch_deepest_subcategory(topic, depth=random.randint(2, 3))
            detailed_topics[topic].append(deepest_subcategory)
        print(f"Deep subcategories for {topic}: {detailed_topics[topic]}")

    # Write the detailed topics to a file
    write_topics_file(detailed_topics)
    print("Finished writing topics to topics.py")
