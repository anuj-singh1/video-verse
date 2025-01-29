
# REST APIs for Video Files

## Overview

This Django-based application provides a set of REST APIs for uploading, trimming, merging, and sharing video files. Users can upload videos, manipulate video clips, and generate shareable links with expiration times.


---

## Installation

### Prerequisites

1. Install Python (recommended version: 3.8 or higher).
 SQLite will be used as the database, which is automatically included with Django.

### Set up the environment

1. Clone the repository:
   ```bash
   git clone git@github.com:anuj-singh1/video-verse.git
   cd video-verse
   ```
2. Create Virtual Env
   ```bash
   virtualenv venv
   ```
3. Activate Virtual Env
   ```bash
   source venv/bin/activate
   ```
4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Migrate the database:
   ```bash
   python manage.py migrate
   ```
---

## Running the API Server

To run the API server locally:

```bash
python manage.py runserver
```

You can now access the API at `http://127.0.0.1:8000/`.

---

## Running Tests

Run unit tests with the following command:

```bash
python manage.py test
```

## API Endpoints

- **GET /api/videos/list** - List all the videos.
- **POST /api/videos/create** - Upload a video file (size and duration validated).
- **POST /api/videos/{video_id}/share** - Generate a shareable video link with time-based expiration.
- **POST /api/videos/{video_id}/trim** - Trim an uploaded video from the start or the end.
- **POST /api/videos/merge** - Merge multiple uploaded videos into one.



## Full API Documentation at [Video Verse](https://documenter.getpostman.com/view/15010018/2sAYQiBo5L)

---

## Assumptions & Design Choices

1. **API Token Authentication**: Some endpoints require API token authentication using a static token. No complex login system is implemented, keeping it simple for demonstration purposes. Create env variable with name `AUTH_TOKEN` and use its value as bearer token in request headers.
2. **Video Size and Duration**: The limits of file upload is configurable by setting env variable `MAX_UPLOAD_FILE_SIZE=10` for 10 Mb.
3. **Video Processing**: The trimming and merging functionality would be handled by either some 3rd party video processing service or by loading files into memory and using [MoviePy](https://zulko.github.io/moviepy/)
4. **Link Expiry**: Links generated have an assumed expiry time (e.g., 15 minutes).
5. **Cloud Storage**: Using Cloudinary for video storage using unsigned request. For production, we can generate only signature from backend and use that to upload from Client's browser to avoid load on server. [Cloudinary Docs](https://cloudinary.com/documentation/client_side_uploading)

---

