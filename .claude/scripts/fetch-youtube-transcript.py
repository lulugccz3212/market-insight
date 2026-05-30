import sys
import argparse
import requests
from http.cookiejar import MozillaCookieJar
from youtube_transcript_api import YouTubeTranscriptApi

def load_cookies(cookies_path):
    cj = MozillaCookieJar()
    try:
        cj.load(cookies_path, ignore_discard=True, ignore_expires=True)
        return cj
    except Exception as e:
        print(f"Warning: Could not load cookies as MozillaCookieJar: {e}. Trying simple key-value parsing.")
        from requests.cookies import cookiejar_from_dict
        cookies_dict = {}
        try:
            with open(cookies_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        cookies_dict[parts[5]] = parts[6]
            return cookiejar_from_dict(cookies_dict)
        except Exception as e2:
            print(f"Failed simple parsing as well: {e2}")
            return None

def fetch_transcript(video_id, output_path, cookies_path=None, language='pt'):
    try:
        print(f"Attempting to fetch transcript for video: {video_id} in language: {language}")
        
        languages = [language]
        if language != 'pt':
            languages.append('pt')
        languages.append('en')
        
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        })
        
        if cookies_path:
            print(f"Loading cookies from: {cookies_path}")
            cj = load_cookies(cookies_path)
            if cj:
                session.cookies = cj
                print("Cookies successfully loaded into session.")
            else:
                print("Warning: Failed to load cookies, proceeding without cookies.")

        api = YouTubeTranscriptApi(http_client=session)
        transcript_list = api.fetch(video_id, languages=languages)
        
        formatted_lines = []
        for entry in transcript_list:
            start_sec = int(entry['start'])
            minutes = start_sec // 60
            seconds = start_sec % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            formatted_lines.append(f"{timestamp} {entry['text']}")
        
        content = "\n".join(formatted_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully fetched and saved transcript to: {output_path}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error fetching transcript: {error_msg}")
        
        error_report = (
            f"ERROR: Failed to fetch YouTube transcript for video {video_id}.\n\n"
            f"Reason:\n{error_msg}\n\n"
            "How to resolve this:\n"
            "1. Export cookies from your logged-in browser (using 'Get cookies.txt' or 'EditThisCookie' extension) to a file named '.claude/youtube-cookies.txt'.\n"
            "   Then run the script with: python .claude/scripts/fetch-youtube-transcript.py -v YOUR_VIDEO_ID -o OUTPUT_FILE --cookies .claude/youtube-cookies.txt\n"
            "2. Alternatively, manually open the YouTube video in your browser, open the transcript panel ('Show Transcript'), copy all the text, and paste it into a file.\n"
        )
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(error_report)
        
        return False

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcripts with proxy/cookie support.")
    parser.add_argument("-v", "--video-id", required=True, help="YouTube Video ID or full URL")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("-c", "--cookies", help="Path to cookies.txt file")
    parser.add_argument("-l", "--lang", default="pt", help="Language code (default: pt)")
    
    args = parser.parse_args()
    
    video_id = args.video_id
    if "youtube.com" in video_id or "youtu.be" in video_id:
        if "v=" in video_id:
            video_id = video_id.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_id:
            video_id = video_id.split("youtu.be/")[1].split("?")[0]
            
    fetch_transcript(video_id, args.output, args.cookies, args.lang)

if __name__ == "__main__":
    main()
