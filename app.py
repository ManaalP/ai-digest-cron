import os
import json

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    
    if path == "/api/config":
        supabase_url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        supabase_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
        body = json.dumps({"supabaseUrl": supabase_url, "supabaseAnonKey": supabase_key}).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
            ("Cache-Control", "public, max-age=60, s-maxage=60")
        ]
        start_response("200 OK", headers)
        return [body]

    # Serve static assets or index.html
    file_to_serve = "index.html"
    if path.startswith("/seed_7days.json"):
        file_to_serve = "seed_7days.json"
        content_type = "application/json"
    else:
        content_type = "text/html; charset=utf-8"

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, file_to_serve)
        with open(file_path, "rb") as f:
            content = f.read()
        headers = [
            ("Content-Type", content_type),
            ("Cache-Control", "public, max-age=0, must-revalidate")
        ]
        start_response("200 OK", headers)
        return [content]
    except Exception as e:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [str(e).encode("utf-8")]

# Alias for WSGI/ASGI handlers
application = app
handler = app
