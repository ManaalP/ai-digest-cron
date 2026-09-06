import os
import json
import re

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if path == "/og-preview.jpg":
        file_path = os.path.join(base_dir, "og-preview.jpg")
        content_type = "image/jpeg"
        cache_ctrl = "public, max-age=86400, s-maxage=86400"
    elif path == "/favicon.svg":
        file_path = os.path.join(base_dir, "favicon.svg")
        content_type = "image/svg+xml"
        cache_ctrl = "public, max-age=86400, s-maxage=86400"
    elif path.startswith("/seed_7days.json"):
        file_path = os.path.join(base_dir, "seed_7days.json")
        content_type = "application/json"
        cache_ctrl = "public, max-age=60, must-revalidate"
    else:
        file_path = os.path.join(base_dir, "index.html")
        content_type = "text/html; charset=utf-8"
        cache_ctrl = "public, max-age=0, must-revalidate"

    try:
        if content_type.startswith("image/"):
            with open(file_path, "rb") as f:
                content = f.read()
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()

            # Dynamic Host & Open Graph Metadata Injection
            if file_path.endswith("index.html"):
                host = environ.get("HTTP_X_FORWARDED_HOST") or environ.get("HTTP_HOST") or "ai-digest-by-mp.vercel.app"
                proto = environ.get("HTTP_X_FORWARDED_PROTO") or environ.get("wsgi.url_scheme") or "https"
                base_url = f"{proto}://{host}"
                query_str = environ.get("QUERY_STRING", "")
                
                full_current_url = f"{base_url}{path}"
                if query_str:
                    full_current_url += f"?{query_str}"

                # Update canonical host URLs
                html = html.replace("https://ai-digest-by-mp.vercel.app/og-preview.jpg", f"{base_url}/og-preview.jpg")
                html = html.replace('content="https://ai-digest-by-mp.vercel.app"', f'content="{full_current_url}"')

                # Dynamic customization for WhatsApp, Twitter, and Social crawlers
                if "tab=models" in query_str:
                    model_match = re.search(r'inspect=([a-zA-Z0-9\-_]+)', query_str)
                    if model_match:
                        model_name = model_match.group(1).replace("-", " ").title()
                        new_title = f"{model_name} — AI Digest Model Inspector"
                        new_desc = f"Deep dive into {model_name}: architecture, SWE-bench score, token pricing, context window, and developer verdict."
                    else:
                        new_title = "Frontier Models & Benchmarks — AI Digest"
                        new_desc = "Compare verified frontier models (Claude 3.7 Sonnet, OpenAI o3-mini, DeepSeek-R1, Gemini 2.0 Flash) with SWE-bench scores, pricing, and specs."
                    
                    html = html.replace("<title>AI Digest — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace("<title>AI Pulse — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace('content="AI Digest — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="AI Pulse — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="A calm, reader-friendly developer digest tracking frontier models, weekly breakthroughs, and benchmark comparisons."', f'content="{new_desc}"')
                
                elif "tab=milestones" in query_str:
                    new_title = "3-Year AI Milestones Archive (2023–2026) — AI Digest"
                    new_desc = "Explore the definitive timeline of frontier AI breakthroughs from GPT-4 and AlphaFold 3 to Claude 3.7 Sonnet and DeepSeek-R1."
                    html = html.replace("<title>AI Digest — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace("<title>AI Pulse — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace('content="AI Digest — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="AI Pulse — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="A calm, reader-friendly developer digest tracking frontier models, weekly breakthroughs, and benchmark comparisons."', f'content="{new_desc}"')
                
                elif "tab=tasks" in query_str:
                    new_title = "Developer AI Task & Model Selector Guide — AI Digest"
                    new_desc = "Actionable engineering guide mapping specific software workflows to the optimal frontier AI models."
                    html = html.replace("<title>AI Digest — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace("<title>AI Pulse — Frontier AI &amp; Developer Intelligence</title>", f"<title>{new_title}</title>")
                    html = html.replace('content="AI Digest — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="AI Pulse — Frontier AI &amp; Developer Intelligence"', f'content="{new_title}"')
                    html = html.replace('content="A calm, reader-friendly developer digest tracking frontier models, weekly breakthroughs, and benchmark comparisons."', f'content="{new_desc}"')

            content = html.encode("utf-8")

        headers = [
            ("Content-Type", content_type),
            ("Cache-Control", cache_ctrl),
            ("Access-Control-Allow-Origin", "*")
        ]
        start_response("200 OK", headers)
        return [content]
    except Exception as e:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [str(e).encode("utf-8")]

# Alias for WSGI/ASGI handlers
application = app
handler = app
