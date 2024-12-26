import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def create_requests_session():
    """
    Create a requests session with retry mechanism.
    
    Returns:
        requests.Session: Configured requests session
    """
    session = requests.Session()
    retries = Retry(
        total=5,  # Total number of retries to allow
        backoff_factor=1,  # A backoff factor to apply between attempts
        status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry on
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def scrape_codechef_problems_solved(username, session):
    """
    Scrape the number of problems solved for a given CodeChef username.
    
    Args:
        username (str): CodeChef username to scrape
        session (requests.Session): Requests session to use for scraping
    
    Returns:
        int or None: Number of problems solved, or None if not found
    """
    # Construct the URL
    url = f"https://www.codechef.com/users/{username}"
    
    # Add headers to mimic a browser request and reduce chance of being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Send GET request with longer timeout
        response = session.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the h3 tag containing "Problems Solved"
        problems_solved_tag = soup.find('h3', string=lambda text: text and 'Problems Solved' in text)
        
        if problems_solved_tag:
            # Extract the number
            number = problems_solved_tag.text.strip()
            
            # Handle different possible formats
            parts = number.split()
            if len(parts) >= 3:
                try:
                    return int(parts[-1])
                except ValueError:
                    return 0
            
        return 0
    
    except requests.RequestException as e:
        print(f"Error scraping {username}: {e}")
        return None

def scrape_multiple_users(usernames):
    """
    Scrape problems solved for multiple CodeChef usernames.
    
    Args:
        usernames (list): List of CodeChef usernames
    
    Returns:
        dict: Dictionary of usernames and their problems solved
    """
    # Create a session to reuse connections
    session = create_requests_session()
    
    results = []
    
    for username in usernames:
        # Add a random delay to avoid overwhelming the server
        time.sleep(random.uniform(1.5, 3.5))
        
        problems_solved = scrape_codechef_problems_solved(username, session)
        results.append(problems_solved)
        print(f"{username}: {problems_solved} problems solved")
    
    return results

# Example usage
if __name__ == "__main__":
    # # Your list of usernames
    # users = ['bhagyasiri06', 'madhu2891a6702', 'ajitj6703', 'sampath', 'divyamaram', 'hemanthi', 'sadwika20', 'hari22891a6708', 'pravallika', 'aakash6711', 'srinidhi6712', 'anil22891a6713', 'lekhana04', 'meghana715', 'priyanka716', 'prudvi0w', 'varshika6718', 'ruthvik6719', 'himasree22891a', 'harikrishna228', 'a6722anki', 'senani', 'vandana6724', 'prashrocks123', 'abc', 'sharan63', 'abc', 'harshith6729', 'koushik6730', 'abc', 'adithya_mc', 'ajayumar', 'hemardhan6734', 'karthikgoud07', 'mona22891a6736', 'abc', 'rishitha6738', 'abc', 'akash6740', 'pesarumaithri', 'shivaram', 'polakipooja', 'sai_aashrith', 'yuvateja6745', 'vitehchandra', 'naveenkumar228', 'sowmyaravula22', 'mamatha57', 'bhavya6754', 'farhamuskan228', 'manish6756', 'krishnasunka20', 'dhanraj58', 'shivashrith59', 'navyareddy', 'ubbadivya', 'vijaychandra62', 'krishnakoundinya', 'gautham61', 'a23895a6701', 's2395a6702', 'varu23895a6703', 'abc', 'abc', 'jaswanth23895a', 'akhila92', 'abc']


    # # Scrape problems solved
    # results = scrape_multiple_users(users)
    
    # Save results to a CSV file
    # with open('codechef_problems_solved.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['Username', 'Problems Solved'])
    #     for username, problems in results.items():
    #         writer.writerow([username, problems])
    pass

def count(users):
    results = scrape_multiple_users(users)
    return results