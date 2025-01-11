# Scrape-Master

This repository contains multiple projects focused on web scraping, targeting various websites and datasets. Each project is tailored to extract and process specific types of data efficiently and effectively. Below is an overview of the projects included:

## Projects Overview

### 1. **Data Mining**
   - **Focus**: General-purpose data mining and extraction from diverse sources.
   - **Key Features**:
     - Flexible data scraping pipelines.
     - Optimized for handling structured and semi-structured data.
   - **Subprojects**:
     - **Hotel Data Scraper**: A simple web scraper built using Python with Beautiful Soup and Selenium for scraping hotel information. This project is beginner-friendly and does not employ multi-threading.
     - **Foodie Reviews Crawler**: A web crawler implemented in Python with Beautiful Soup and Selenium for extracting food reviews. It emphasizes simplicity and demonstrates a practical approach to web scraping.

### 2. **Interview-TW-Crawler**
   - **Focus**: Scraping interview-related content from Taiwanese platforms, specifically [面試趣](https://interview.tw/).
   - **Key Features**:
     - Scrapes interview data and career insights.
     - Version 1.1 includes features for skipping Google account verification and gathering company URLs.
     - To customize the crawler for specific companies and fix various bugs, further improvements are needed.
   
### 3. **NPO-Crawler**
   - **Focus**: Extracting information about non-profit organizations (NPOs) from the [台灣公益資訊中心](https://www.npo.org.tw/npolist.aspx).
   - **Key Features**:
     - Collects detailed data on NPO profiles.
     - Ideal for research and transparency purposes.

### 4. **Multithreaded Web Crawler for Free NTU COOL Courses**
   - **Focus**: Crawling free NTU COOL courses without logging in and saving the data in a CSV format.
   - **Key Features**:
     - Uses multithreading to speed up the crawling process.
     - Retrieves course details without requiring user login.
     - Outputs course data in a structured CSV file.

### 5. **NTU COOL Video Crawler v1.1**
   - **Focus**: Automating the download and upload of NTU COOL videos to YouTube.
   - **Key Features**:
     - **Login Automation**: Automates login to NTU COOL using credentials stored in a `.env` file.
     - **Video Retrieval**: Extracts video links from specific NTU COOL course pages.
     - **Video Downloading**: Downloads videos from NTU COOL, focusing on the older video format.
     - **YouTube Uploading**: Uploads videos to YouTube with metadata such as title, description, and privacy settings.
     - **Playlist Integration**: Adds uploaded videos to a specific YouTube playlist.

   - **Limitations**:
     - Only supports videos in NTU COOL’s older video format.
     - Does not handle non-video content (e.g., PDFs).
     - YouTube API credentials expire periodically, requiring re-authentication.

## Usage
Each project is organized into its respective folder with detailed documentation and code. Please refer to the README within each project directory for setup instructions and usage guidelines.

## Contribution
Contributions are welcome. If you encounter issues or have suggestions, feel free to submit a pull request or [contact me](mailto:xiangyi.huang0213@gmail.com).

## License
This repository is licensed under the MIT License. Please review the license file for more details.
