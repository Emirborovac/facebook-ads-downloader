from django.shortcuts import render, HttpResponse
import os
import yt_dlp
import instaloader
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import FileResponse

def download_video_view(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        output_path = os.path.join(os.getcwd(), 'downloads')  # Save to 'downloads' folder in the current directory

        # Create downloads directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        debug_info = []  # Collect debug information

        def is_youtube(url):
            return 'youtube.com' in url or 'youtu.be' in url

        def is_instagram(url):
            return 'instagram.com' in url

        def is_facebook_ad(url):
            return 'facebook.com' in url and 'ads' in url

        try:
            if is_youtube(video_url):
                debug_info.append("Processing YouTube URL")
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'nocache': True,
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(video_url, download=False)
                        duration = info_dict.get('duration', 0)
                        debug_info.append(f"Video duration: {duration} seconds")
                        if duration < 0.5 or duration > 1200:
                            debug_info.append("Invalid video duration")
                            return HttpResponse("Invalid video duration. Must be between 0.5 and 1200 seconds.")
                        ydl.download([video_url])
                        video_path = ydl.prepare_filename(info_dict)
                        debug_info.append(f"Downloaded video path: {video_path}")
                        return FileResponse(open(video_path, 'rb'), as_attachment=True, filename=os.path.basename(video_path))
                except Exception as e:
                    debug_info.append(f"Failed to download YouTube video: {e}")
                    return HttpResponse(f"Failed to download YouTube video: {e}")

            elif is_instagram(video_url):
                debug_info.append("Processing Instagram URL")
                try:
                    L = instaloader.Instaloader()
                    session_file_path = r'/path/to/your/instaloader/session'  # Replace with your path
                    if os.path.exists(session_file_path):
                        L.load_session_from_file('your_username', session_file_path)
                        debug_info.append("Loaded Instagram session")
                    else:
                        debug_info.append("Session file not found")
                        return HttpResponse("Session file not found.")

                    shortcode = video_url.split("/")[-2]
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    video_url = post.video_url
                    debug_info.append(f"Instagram video URL: {video_url}")
                    if video_url:
                        video_file_name = "instagram_reel.mp4"
                        video_path = os.path.join(output_path, video_file_name)
                        response = requests.get(video_url, stream=True)
                        with open(video_path, 'wb') as video_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                video_file.write(chunk)
                        debug_info.append(f"Downloaded Instagram video to: {video_path}")
                        return FileResponse(open(video_path, 'rb'), as_attachment=True, filename=video_file_name)
                    else:
                        debug_info.append("No video URL found on Instagram post")
                        return HttpResponse("Failed to download Instagram video: No video URL found.")
                except Exception as e:
                    debug_info.append(f"Failed to download Instagram video: {e}")
                    return HttpResponse(f"Failed to download Instagram video: {e}")

            elif is_facebook_ad(video_url):
                debug_info.append("Processing Facebook Ad URL")
                try:
                    options = Options()
                    options.add_argument("--headless")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--window-size=1920x1080")
                    options.add_argument("--log-level=3")

                    driver = webdriver.Chrome(options=options)  # Ensure chromedriver is in your PATH
                    try:
                        driver.get(video_url)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                        video_element = driver.find_element(By.TAG_NAME, "video")
                        video_src_url = video_element.get_attribute('src')
                        debug_info.append(f"Extracted video URL: {video_src_url}")

                        if not video_src_url:
                            debug_info.append("No video source URL found")
                            return HttpResponse("Failed to download Facebook Ad video: No video source found.")

                        response = requests.get(video_src_url, stream=True)
                        if response.status_code == 200:
                            video_path = os.path.join(output_path, "facebook_ad_video.mp4")
                            with open(video_path, 'wb') as video_file:
                                for chunk in response.iter_content(chunk_size=8192):
                                    video_file.write(chunk)
                            debug_info.append(f"Downloaded Facebook Ad video to: {video_path}")
                            return FileResponse(open(video_path, 'rb'), as_attachment=True, filename="facebook_ad_video.mp4")
                        else:
                            debug_info.append(f"Failed to download video: HTTP {response.status_code}")
                            return HttpResponse("Failed to download Facebook Ad video.")
                    finally:
                        driver.quit()
                except Exception as e:
                    debug_info.append(f"Failed to download Facebook Ad video: {e}")
                    return HttpResponse(f"Failed to download Facebook Ad video: {e}")

            else:
                debug_info.append("Unsupported video URL")
                return HttpResponse("Unsupported video URL.")
        finally:
            # Print all debug information to the console
            for info in debug_info:
                print(info)
    else:
        return render(request, 'downloader/index.html')
