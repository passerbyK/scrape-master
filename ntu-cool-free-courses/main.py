import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize an empty list to store the results
courses = []

# Set the range of course IDs to scrape
start_id = 1
end_id = 40000
num_threads = 10  # Number of threads

# Define a function to handle each course page
def fetch_course(course_id):
    url = f'https://cool.ntu.edu.tw/courses/{course_id}'
    response = requests.get(url)
    result = None

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the page exists
    if soup.find('div', class_='ic-Error-page'):
        return result

    # Check if it redirects to the login page
    if "login/portal" in response.url:
        return result

    # Find the course name
    crumb_div = soup.find('div', class_='ic-app-crumbs')

    if crumb_div:
        a_tag = crumb_div.find('a', href=f'https://cool.ntu.edu.tw/courses/{course_id}')
        if a_tag:
            span_tag = a_tag.find('span', class_='ellipsible')
            if span_tag:
                course_name = span_tag.get_text(strip=True)
                result = [course_name, url, course_id]

    return result

# Use a thread pool to handle concurrency
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    future_to_course = {executor.submit(fetch_course, course_id): course_id for course_id in range(start_id, end_id + 1)}

    for future in tqdm(as_completed(future_to_course), total=end_id - start_id + 1):
        course = future.result()
        if course:
            courses.append(course)

# Convert the results into a DataFrame
df = pd.DataFrame(courses, columns=['Course Name', 'URL', 'Course ID'])

# Save the DataFrame to a CSV file
df.to_csv('ntu_courses.csv', encoding="utf-8-sig", index=False)

# Print the total number of courses saved
print(f'Total number of courses saved: {len(courses)}')