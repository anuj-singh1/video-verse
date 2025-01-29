from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from video_backend.models import Video
from video_server.settings import AUTH_STATIC_TOKEN, local_tz, MAX_UPLOAD_FILE_SIZE


class VideoAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {AUTH_STATIC_TOKEN}"}

    def test_upload_large_file(self):
        large_video = SimpleUploadedFile(
            "large_video.mp4",
            b"\x00" * (21 * 1024 * 1024),  # 21 MB File
            content_type="video/mp4"
        )
        response = self.client.post(
            "/api/videos/create/",
            {"title": "Test Large Video", "file": large_video, "duration": 120},
            **self.auth_header
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"],
                         f"File size should not exceed {MAX_UPLOAD_FILE_SIZE // (1024 * 1024):.2f} MB")

    def test_expired_shared_link_access(self):
        video = Video.objects.create(
            title="Expired Video",
            file_url="http://example.com/video.mp4",
            duration=120,
            shared_link="http://testserver/api/videos/9b84960d-08b5-4701-b7d0-f6d717a00710/",
            expires_at=datetime.now().replace(tzinfo=local_tz) - timedelta(hours=1)
        )

        response = self.client.get('/api/videos/9b84960d-08b5-4701-b7d0-f6d717a00710/')
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "The shared link has expired.")
