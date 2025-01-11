import os
import requests
import time
import random
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow, argparser

# Load environment variables
load_dotenv()

# Constants
COOL_LOGIN_URL = "https://cool.ntu.edu.tw/"

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload",
                        "https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VIDEO_DIR = "videos"

MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# Credentials from environment
account = os.getenv("account")
password = os.getenv("password")
course_id = os.getenv("course_id")

description = os.getenv("DEFAULT_DESCRIPTION")
category = os.getenv("DEFAULT_CATEGORY")
privacy_status = os.getenv("DEFAULT_PRIVACY_STATUS")
made_for_kids = os.getenv("DEFAULT_SELF_DECLARED_MADE_FOR_KIDS")
playlist_id = os.getenv("TARGET_PLAYLIST_ID")

# Create a directory for downloaded videos
os.makedirs(VIDEO_DIR, exist_ok=True)

def login_to_cool(driver):
    """
    Log in to COOL platform using provided credentials.
    """
    driver.get(COOL_LOGIN_URL)
    time.sleep(3)

    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'css-qxdwt4-view--block-baseButton')]")
    login_button.click()

    time.sleep(3)

    # Enter account and password
    account_input = driver.find_element(By.XPATH, "//div[text()='\u5e33\u865f']/following-sibling::input")
    password_input = driver.find_element(By.XPATH, "//div[text()='\u5bc6\u78bc']/following-sibling::input")
    
    # Remove oninput event listener to prevent input validation
    driver.execute_script("""
                          var input = document.querySelector('input[name="ctl00$ContentPlaceHolder1$UsernameTextBox"]');
                          input.removeAttribute('oninput');
                          """)
    
    account_input.send_keys(account)
    password_input.send_keys(password)

    # Submit login form
    login_submit_button = driver.find_element(By.XPATH, "//input[@value='\u767b\u5165']")
    login_submit_button.click()

    time.sleep(3)

def get_video_links(driver, course_id):
    """
    Retrieve video links from the specified course.
    """
    url = f"https://cool.ntu.edu.tw/courses/{course_id}"
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item_name")))

    results = []
    item_names = driver.find_elements(By.CLASS_NAME, "item_name")

    for item in item_names:
        try:
            a_tag = item.find_element(By.CLASS_NAME, "item_link")
            title = a_tag.get_attribute("title").strip()
            href = a_tag.get_attribute("href").strip()
            results.append({"title": title, "href": href})
        except Exception as e:
            print(f"Error extracting link: {e}")

    return results

def download_video(driver, video_info):
    """
    Download video from the specified link.
    """
    title = video_info["title"]
    href = video_info["href"]

    driver.get(href)

    try:
        # Switch to video iframe
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "tool_content"))
        )
        driver.switch_to.frame(iframe)

        # Extract video URL
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vjs-poster"))
        )
        
        background_image_url = driver.execute_script(
            """
            var element = document.querySelector('.vjs-poster');
            return element ? element.style.backgroundImage : null;
            """
        )

        if background_image_url:
            background_image_url = background_image_url.strip('url("')[:-2]
            base_url = background_image_url.rsplit('/', 1)[0]
            video_url = f"{base_url}/transcoded.mp4"

            # Download video
            print(f"Downloading video: {title}")
            response = requests.get(video_url, stream=True)
            video_path = os.path.join(VIDEO_DIR, f"{title}.mp4")

            with open(video_path, "wb") as file:
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        print(f"\rDownloading {title}: {downloaded / total_size * 100:.2f}%", end="")

            print(f"\nDownloaded: {title}")
            return video_path

        else:
            print(f"No video found for {title}")

    except Exception as e:
        print(f"Error processing {title}: {e}")

    finally:
        driver.switch_to.default_content()

    return None

def get_authenticated_service():
    """
    Authenticate with YouTube API and return a service object.
    """
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("oauth2.json")
    credentials = storage.get()
    flags = argparser.parse_args([])

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

def upload_to_youtube(youtube, file_path, title):
    """
    Upload video to YouTube.
    """
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": made_for_kids
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    insert_request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    retry = 0

    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response and "id" in response:
                print(f"Upload complete: Video ID {response['id']}")
                return response["id"]
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                print(f"Retryable error: {e}")
            else:
                raise
        retry += 1
        if retry > MAX_RETRIES:
            print("Max retries reached. Upload failed.")
            break
        sleep_seconds = random.random() * (2 ** retry)
        print(f"Retrying in {sleep_seconds:.2f} seconds...")
        time.sleep(sleep_seconds)
    return None

def add_video_to_playlist(youtube, video_id, playlist_id):
    """
    Add the uploaded video to the specified playlist.
    """
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }

    try:
        youtube.playlistItems().insert(part="snippet", body=body).execute()
        print(f"Added video {video_id} to playlist {playlist_id}")
    except HttpError as e:
        print(f"An HTTP error occurred while adding the video to the playlist: {e}")
       
def main():
    """
    Main function to coordinate scraping, downloading, and uploading videos.
    """
    driver = uc.Chrome()
    youtube = get_authenticated_service()

    try:
        # Log in to COOL
        login_to_cool(driver)

        # Get video links
        video_links = get_video_links(driver, course_id)

        for video_info in video_links:
            # Download video
            video_path = download_video(driver, video_info)

            if video_path:
                # Upload video to YouTube
                video_id = upload_to_youtube(youtube, video_path, video_info["title"])

                # Delete local video file
                os.remove(video_path)
                print(f"Deleted local file: {video_path}")

                # Add video to playlist
                if playlist_id:
                    add_video_to_playlist(youtube, video_id, playlist_id)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
