# NTU COOL Video Crawler v1.1

This project provides a Python-based automation tool to download videos from NTU COOL (National Taiwan University’s online course platform) and upload them to YouTube. The script utilizes Selenium for web scraping, the YouTube Data API for uploading, and OAuth 2.0 for authentication.

---

## Features

- **Login Automation**: Automates login to the NTU COOL platform using credentials provided in an `.env` file.
- **Video Retrieval**: Extracts video links from a specific NTU COOL course page.
- **Video Downloading**: Downloads videos from NTU COOL, specifically those stored in the platform's older video format.
- **YouTube Uploading**: Uploads downloaded videos to YouTube with metadata such as title, description, category, and privacy settings.
- **Playlist Integration**: Adds uploaded videos to a specified YouTube playlist.

### Limitations

1. **Supported Formats**: The script currently only supports videos in NTU COOL’s older video format. Videos stored as external YouTube links or in unsupported formats cannot be downloaded.
2. **Unsupported Content**: The script does not handle non-video content such as PDFs or other documents.
3. **Authentication Expiry**: The YouTube API credentials (`oauth2.json`) will expire periodically, requiring re-authentication.

---

## Prerequisites

### 1. Install Required Libraries
Install the necessary Python libraries using:
```bash
pip install -r requirements.txt
```

### 2. Enable YouTube Data API
- Enable the [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) in your Google Cloud Console.
- Ensure that you enable at least the following permissions for the API:
  - `"https://www.googleapis.com/auth/youtube.upload"`
  - `"https://www.googleapis.com/auth/youtube.force-ssl"`
- Download your `client_secrets.json` file from the Google Cloud Console and place it in the project directory.
- Make sure to add your personal Google account to the **Developer Contact Information** in the Google Cloud Console.

### 3. Set Up `.env` File
Create a `.env` file in the project directory with the following content:

```env
# NTU COOL account credentials
account=<YOUR_COOL_ACCOUNT>
password=<YOUR_COOL_PASSWORD>

# Course ID to be scraped
course_id=<COURSE_ID>

# Default video settings for YouTube
DEFAULT_DESCRIPTION="This is the course video from NTU"
DEFAULT_CATEGORY=22 # Category ID for "People & Blogs"
DEFAULT_PRIVACY_STATUS="private"
DEFAULT_SELF_DECLARED_MADE_FOR_KIDS=False

# Target YouTube playlist
TARGET_PLAYLIST_ID=<PLAYLIST_ID>
```

---

## Usage

### 1. Run the Script
Start the script using:
```bash
python main.py
```

### 2. Log in to NTU COOL
The script will:
- Open a Chrome browser (via undetected_chromedriver).
- Automatically log in to NTU COOL using the credentials in the `.env` file.

### 3. Download Videos
The script will navigate to the specified course page, retrieve video links, and download them to the `videos` directory.

### 4. Upload Videos to YouTube
Each downloaded video will be:
- Uploaded to YouTube with metadata from the `.env` file.
- Optionally added to a specified playlist.

### 5. Manage Local Files
After a successful upload, the script will delete the local video file to save space.

---

## File Structure

```plaintext
.
├── videos/                # Directory for downloaded videos
├── client_secrets.json    # OAuth 2.0 client secrets for YouTube API
├── .env                   # Environment variables
├── main.py         # Main Python script
├── oauth2.json            # OAuth credentials (generated on first run)
└── requirements.txt       # Required Python libraries
```

---

## Notes

- **First-Time Authentication**: On the first run, you will be prompted to grant permissions to the YouTube API. This generates an `oauth2.json` file for subsequent runs.
- **Re-Authentication**: If the `oauth2.json` file expires, delete it and re-run the script to authenticate again.
- **NTU COOL Updates**: If NTU COOL updates its website structure, the scraping logic may need adjustments.

---

## Troubleshooting

1. **Google API Errors**
   - Ensure your `client_secrets.json` file is valid and placed in the correct directory.
   - Re-authenticate if the `oauth2.json` file is invalid or expired.

2. **Video Download Issues**
   - Check if the video format is supported.
   - Ensure your NTU COOL account has access to the course content.

3. **YouTube Upload Failures**
   - Verify your YouTube account permissions.
   - Check if the YouTube API quota has been exceeded.

---

## Dependencies

- Selenium
- undetected-chromedriver
- Google API Client
- Oauth 2.0 Client
- Requests
- Python Dotenv

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## References

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Uploading a Video to YouTube](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [YouTube API PlaylistItems.insert Documentation](https://developers.google.com/youtube/v3/docs/playlistItems/insert)
- [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- [NTU COOL Platform](https://cool.ntu.edu.tw/)

---

## Contact

If you encounter issues or have suggestions, feel free to [contact me](mailto:xiangyi.huang0213@gmail.com).
