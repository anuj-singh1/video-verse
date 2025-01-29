import json
import uuid
from datetime import datetime, timedelta

# import cloudinary.uploader
import pytz
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# from dotenv import load_dotenv
from requests import Response
from rest_framework import serializers

from .auth import authenticate_api
from .models import Video

# load_dotenv()
# config = cloudinary.config(secure=True)
local_tz = pytz.timezone('Asia/Kolkata')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'duration', 'uploaded_at']


@csrf_exempt
@require_http_methods(["GET"])
def video_list(request) -> JsonResponse:
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


# @csrf_exempt
# @require_http_methods(["POST"])
# @authenticate_api
# def video_create(request):
#     try:
#         data = json.loads(request.body)
#         title = data.get("original_filename", "Untitled")
#         file_url = data.get("secure_url")
#         duration = data.get("duration", 0)
#
#         if not file_url:
#             return JsonResponse({"error": "File URL is required"}, status=400)
#
#         video = Video.objects.create(
#             title=title,
#             file_url=file_url,
#             duration=duration,
#         )
#
#         return JsonResponse({"message": "Video uploaded successfully", "video_id": video.id}, status=201)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

def save_video(cloudinary_response) -> Video:
    return Video.objects.create(
        title=cloudinary_response.get("public_id"),
        file_url=cloudinary_response.get("secure_url"),
        duration=cloudinary_response.get("duration", 0),
        shared_link=None,
        expires_at=None)


def upload_video_to_cloud(file) -> Response:
    cloudinary_url = "https://api.cloudinary.com/v1_1/anuj-singh-devfolio/video/upload"
    data = {"upload_preset": ""}
    files = {"file": file}

    # return cloudinary.uploader.upload_large(file, resource_type="video",
    #                                         public_id=f"{datetime.timestamp(datetime.now())}_{file.name}")

    return requests.post(cloudinary_url, files=files, data=data)


@csrf_exempt
@require_http_methods(["POST"])
@authenticate_api
def video_create(request) -> JsonResponse:
    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)
    try:
        response = upload_video_to_cloud(file)
        if response.status_code == 200:
            cloudinary_response = response.json()
            video = save_video(cloudinary_response)
            return JsonResponse({"message": "File uploaded successfully", "video_id": video.id}, status=201)

        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({'message': e}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@authenticate_api
def video_share(request, video_id) -> JsonResponse:
    try:
        video = get_object_or_404(Video, id=video_id)
        data = json.loads(request.body)
        expiry_time = int(data.get("expiry_time", 15))  # Default 60 minutes

        unique_id = str(uuid.uuid4())
        expiry_at = datetime.now() + timedelta(minutes=expiry_time)

        shared_path = f"/api/videos/{unique_id}/"
        full_url = request.build_absolute_uri(shared_path)
        video.shared_link = full_url
        video.expires_at = expiry_at.replace(tzinfo=local_tz)
        video.save()

        return JsonResponse({"shared_link": full_url, "expires_at": expiry_at}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@authenticate_api
def video_trim(request, video_id) -> JsonResponse:
    try:
        video = get_object_or_404(Video, id=video_id)
        data = json.loads(request.body)
        start_time = float(data.get("start_time", 0))
        end_time = float(data.get("end_time", video.duration))

        if start_time >= end_time or start_time < 0 or end_time > video.duration:
            return JsonResponse({"error": "Invalid start or end time"}, status=400)

        # Assuming some 3rd party service to trim videos
        '''
        video_content = requests.get(video.file_url).content

        video_clip = mp.VideoFileClip(video_content)
        video_clip = video_clip.subclipped(start_time, end_time)
        
        video_clip.title = f"{video.title.split('.')[0]}_trimmed.mp4"
        cloudinary_response = upload_video_to_cloud(video_clip)
        video_clip.close()
        trimmed_video = save_video(cloudinary_response)
        '''

        return JsonResponse(VideoSerializer(video).data, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@authenticate_api
def video_merge(request) -> JsonResponse:
    try:
        data = json.loads(request.body)
        video_ids = data.get("video_ids", [])

        if not video_ids or len(video_ids) < 2:
            return JsonResponse({"error": "At least two videos are required for merging"}, status=400)

        videos = Video.objects.filter(id__in=video_ids)
        if videos.count() != len(video_ids):
            return JsonResponse({"error": "Some videos were not found"}, status=404)

        # Assuming some 3rd Party service to concatenate/merge files
        '''
        clips = [mp.VideoFileClip(video.file_url) for video in videos]
        final_clip = mp.concatenate_videoclips(clips)

        output = BytesIO()
        final_clip.write_videofile(output, codec="libx264", audio_codec="aac")
        final_clip.close()

        output.seek(0)
        merged_file_url = f"videos/merged_{datetime.now().timestamp()}.mp4"

        merged_video = Video.objects.create(
            title="Merged Video",
            file_url=merged_file_url,
            duration=sum(video.duration for video in videos)
        )
        '''

        return JsonResponse({'url': 'new file url'}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# @csrf_exempt
# @require_http_methods(["POST"])
# @authenticate_api
# def upload_video(request):
#     return render(request, 'upload.html', {'max_file_size': MAX_UPLOAD_FILE_SIZE})


@csrf_exempt
@require_http_methods(["GET"])
def video_access(request, unique_id) -> JsonResponse:
    try:
        expected_url = request.build_absolute_uri(request.path)
        video = get_object_or_404(Video, shared_link=expected_url)

        if video.expires_at and video.expires_at < datetime.now().replace(tzinfo=local_tz):
            return JsonResponse({"error": "The shared link has expired."}, status=403)

        return redirect(video.file_url)

    except Video.DoesNotExist:
        return JsonResponse({"error": "Invalid or expired link"}, status=404)
