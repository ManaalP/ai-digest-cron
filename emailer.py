import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime, timezone


def _html_escape(s: str) -> str:
    if not s:
        return ""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def _render_category_badge(tag: str) -> str:
    colors = {
        "BREAKTHROUGH": ("#fee2e2", "#b91c1c", "🚨 BREAKTHROUGH"),
        "DEV TOOLS": ("#e0e7ff", "#4338ca", "🛠️ DEV TOOLS"),
        "LOCAL AI": ("#fef3c7", "#b45309", "⚡ LOCAL AI"),
        "PRODUCTION": ("#dcfce7", "#15803d", "🚀 PRODUCTION"),
        "RESEARCH": ("#f3e8ff", "#7e22ce", "🔬 RESEARCH"),
    }
    bg, text_color, label = colors.get(tag, ("#f1f5f9", "#475569", tag))
    return f'<span style="background:{bg};color:{text_color};font-size:11px;font-weight:700;padding:2px 8px;border-radius:4px;letter-spacing:0.04em;text-transform:uppercase;">{label}</span>'


def build_digest_html(digest_input) -> str:
    """
    Accepts either:
      - dict from rank_and_structure_digest() with keys:
          'highlights', 'top_10', 'one_liners', 'total_scanned', 'total_fresh_24h'
      - list of legacy article dicts (backwards compatible).
    """
    if isinstance(digest_input, list):
        # Wrap legacy format into standard structure
        top_articles = digest_input[:10]
        one_liners = digest_input[10:]
        highlights = ["Daily digest of recent technical AI developments."]
        total_scanned = len(digest_input)
        total_fresh = len(digest_input)
    else:
        top_articles = digest_input.get("top_10", [])
        one_liners = digest_input.get("one_liners", [])
        highlights = digest_input.get("highlights", [])
        total_scanned = digest_input.get("total_scanned", len(top_articles))
        total_fresh = digest_input.get("total_fresh_24h", len(top_articles))

    today_str = date.today().isoformat()

    # 1. Highlights Section
    highlight_lis = "".join(f'<li style="margin-bottom:8px;line-height:1.5;">{h}</li>' for h in highlights)
    highlights_html = f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin-bottom:28px;">
        <div style="font-size:13px;font-weight:700;color:#1d4ed8;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;display:flex;align-items:center;">
            ⚡ Executive Highlights (Last 24 Hours in 3 Minutes)
        </div>
        <ul style="margin:0;padding-left:20px;font-size:14px;color:#334155;">
            {highlight_lis}
        </ul>
    </div>
    """

    # 2. Top 10 Ranked Articles
    top_rows = []
    for i, a in enumerate(top_articles, 1):
        cat_badge = _render_category_badge(a.get("category_tag", "RESEARCH"))
        impact_score = a.get("dev_impact_score", 85)

        # Image presentation
        image_html = ""
        if a.get("image_url"):
            image_html = f"""
            <div style="margin:10px 0 14px 0;text-align:center;">
                <img src="{_html_escape(a['image_url'])}" alt="Visual Preview"
                     style="max-width:100%;height:auto;border-radius:8px;border:1px solid #e2e8f0;max-height:280px;object-fit:cover;" />
            </div>
            """

        # Continuation HTML
        cont_html = ""
        if a.get("continuation"):
            c = a["continuation"]
            cont_html = (
                f'<div style="font-size:12px;color:#7a5cff;font-weight:600;margin-bottom:6px;">'
                f'&#8618; Continuation of <a href="{_html_escape(c["url"])}" style="color:#7a5cff;">'
                f'{_html_escape(c["title"])}</a>'
                f'{" (" + c["published_date"][:10] + ")" if c.get("published_date") else ""}'
                f'</div>'
            )

        # Entity tags
        entity_tags = ""
        if a.get("entities"):
            chips = "".join(f'<span style="background:#f1f5f9;color:#475569;font-size:11px;padding:2px 6px;border-radius:4px;margin-right:4px;">{_html_escape(e)}</span>' for e in a["entities"])
            entity_tags = f'<div style="margin-top:8px;">{chips}</div>'

        # Special border for groundbreaking items
        border_style = "border:2px solid #f43f5e;background:#fff1f2;" if a.get("is_groundbreaking") else "border:1px solid #e2e8f0;background:#ffffff;"
        ground_header = '<div style="color:#e11d48;font-size:12px;font-weight:800;letter-spacing:0.06em;margin-bottom:6px;">🚨 GROUNDBREAKING DISCOVERY / BREAKTHROUGH</div>' if a.get("is_groundbreaking") else ''

        top_rows.append(f"""
        <div style="margin-bottom:24px;border-radius:12px;{border_style}padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            {ground_header}
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
                <div>
                    <span style="background:#0f172a;color:#ffffff;font-size:11px;font-weight:800;padding:2px 7px;border-radius:4px;margin-right:6px;">#{i:02d}</span>
                    <span style="font-size:12px;color:#64748b;text-transform:uppercase;font-weight:600;letter-spacing:0.03em;">{_html_escape(a['source'])}</span>
                </div>
                <div>
                    {cat_badge}
                    <span style="font-size:11px;color:#0284c7;font-weight:700;margin-left:6px;background:#e0f2fe;padding:2px 6px;border-radius:4px;">⚡ Impact: {impact_score}/100</span>
                </div>
            </div>

            <div style="font-size:18px;font-weight:700;line-height:1.35;margin:8px 0;">
                <a href="{_html_escape(a['url'])}" style="color:#0f172a;text-decoration:none;">
                    {_html_escape(a['title'])}
                </a>
            </div>

            {cont_html}
            {image_html}

            <div style="font-size:14px;line-height:1.6;color:#334155;margin-bottom:12px;">
                {_html_escape(a['summary'])}
            </div>

            <!-- Developer & Practical Impact Callout -->
            <div style="background:#f8fafc;border-left:3px solid #0ea5e9;padding:10px 14px;border-radius:4px;margin:10px 0;">
                <div style="font-size:11px;font-weight:700;color:#0369a1;text-transform:uppercase;letter-spacing:0.04em;">🛠️ Developer & Practical Use Case:</div>
                <div style="font-size:13px;color:#1e293b;line-height:1.45;margin-top:2px;">
                    {_html_escape(a.get('dev_use_case', 'Relevant for software engineering workflows and model deployment.'))}
                </div>
            </div>

            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;flex-wrap:wrap;">
                {entity_tags}
                <div style="margin-top:6px;">
                    <a href="{_html_escape(a['url'])}" style="font-size:13px;font-weight:600;color:#2563eb;text-decoration:none;">
                        Read Source &amp; Code &rarr;
                    </a>
                </div>
            </div>
        </div>
        """)

    # 3. Quick Hits (1-Liners) Section
    one_liner_rows = []
    for a in one_liners:
        cat_badge = _render_category_badge(a.get("category_tag", "RESEARCH"))
        one_liner_rows.append(f"""
        <tr>
            <td style="padding:10px 8px;border-bottom:1px solid #f1f5f9;vertical-align:top;width:90px;">
                <span style="font-size:11px;color:#64748b;font-weight:600;">{_html_escape(a['source'][:14])}</span>
            </td>
            <td style="padding:10px 8px;border-bottom:1px solid #f1f5f9;vertical-align:top;">
                <div style="font-size:13px;font-weight:600;">
                    <a href="{_html_escape(a['url'])}" style="color:#0f172a;text-decoration:none;">
                        {_html_escape(a['title'])}
                    </a>
                </div>
                <div style="font-size:12px;color:#64748b;line-height:1.4;margin-top:2px;">
                    {_html_escape(a.get('one_liner', a.get('summary', ''))[:160])}
                </div>
            </td>
            <td style="padding:10px 8px;border-bottom:1px solid #f1f5f9;vertical-align:top;width:60px;text-align:right;">
                <a href="{_html_escape(a['url'])}" style="font-size:12px;color:#2563eb;text-decoration:none;font-weight:600;">View &rarr;</a>
            </td>
        </tr>
        """)

    one_liners_html = ""
    if one_liners:
        one_liners_html = f"""
        <div style="margin-top:36px;">
            <div style="border-bottom:2px solid #0f172a;padding-bottom:8px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:baseline;">
                <h3 style="margin:0;font-size:16px;color:#0f172a;text-transform:uppercase;letter-spacing:0.04em;">
                    ⚡ The Quick Hits (Fresh Stories in 1-Line)
                </h3>
                <span style="font-size:12px;color:#64748b;font-weight:600;">{len(one_liners)} items</span>
            </div>
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                {''.join(one_liner_rows)}
            </table>
        </div>
        """

    return f"""
    <html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;max-width:680px;margin:0 auto;color:#0f172a;padding:12px;">
        <div style="border-bottom:3px solid #2563eb;padding-bottom:12px;margin-bottom:20px;">
            <h2 style="margin:0;font-size:24px;font-weight:800;color:#0f172a;">AI Engineering &amp; Applications Digest</h2>
            <div style="display:flex;justify-content:space-between;color:#64748b;font-size:13px;margin-top:6px;flex-wrap:wrap;">
                <span>📅 {today_str} &bull; Strict 24-Hour Window</span>
                <span>📊 {total_scanned} scanned &bull; {total_fresh} fresh &bull; Top 10 Ranked</span>
            </div>
        </div>

        {highlights_html}

        <div style="margin-bottom:14px;">
            <h3 style="margin:0 0 16px 0;font-size:16px;color:#0f172a;text-transform:uppercase;letter-spacing:0.04em;">
                🏆 Top 10 Developer &amp; Applied AI Breakthroughs
            </h3>
            {''.join(top_rows)}
        </div>

        {one_liners_html}

        <div style="color:#94a3b8;font-size:12px;margin-top:32px;text-align:center;border-top:1px solid #e2e8f0;padding-top:16px;">
            Sent by your daily AI digest pipeline &bull; Developer &amp; Application Focused
        </div>
    </body></html>
    """


def build_digest_text(digest_input) -> str:
    today_str = date.today().isoformat()
    if isinstance(digest_input, list):
        top_articles = digest_input[:10]
        one_liners = digest_input[10:]
        highlights = ["Daily digest of recent technical AI developments."]
    else:
        top_articles = digest_input.get("top_10", [])
        one_liners = digest_input.get("one_liners", [])
        highlights = digest_input.get("highlights", [])

    lines = [
        f"AI Engineering & Applications Digest -- {today_str}",
        "=" * 50,
        "",
        "EXECUTIVE HIGHLIGHTS (Last 24 Hours):",
    ]
    for h in highlights:
        # Strip simple HTML tags
        clean_h = h.replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "")
        lines.append(f" * {clean_h}")
    lines.append("")

    lines.append("TOP 10 DEVELOPER & APPLIED AI ARTICLES:")
    lines.append("-" * 50)
    for i, a in enumerate(top_articles, 1):
        lines.append(f"#{i:02d} [{a.get('category_tag', 'AI')}] {a['title']}")
        lines.append(f"Source: {a['source']} | URL: {a['url']}")
        lines.append(f"Impact Score: {a.get('dev_impact_score', 85)}/100")
        lines.append(f"Summary: {a['summary']}")
        lines.append(f"Use Case: {a.get('dev_use_case', '')}")
        lines.append("")

    if one_liners:
        lines.append("THE QUICK HITS (1-LINERS):")
        lines.append("-" * 50)
        for a in one_liners:
            lines.append(f"[{a['source']}] {a['title']} -- {a.get('one_liner', '')}")
            lines.append(f"Link: {a['url']}")
            lines.append("")

    return "\n".join(lines)


def send_email(smtp_host, smtp_port, username, password, email_from, email_to_list, digest_input):
    articles = digest_input if isinstance(digest_input, list) else digest_input.get("top_10", [])
    if not articles:
        print("[emailer] No articles to send, skipping email.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"AI Engineering Digest -- {date.today().isoformat()}"
    msg["From"] = email_from
    msg["To"] = ", ".join(email_to_list)

    msg.attach(MIMEText(build_digest_text(digest_input), "plain"))
    msg.attach(MIMEText(build_digest_html(digest_input), "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(email_from, email_to_list, msg.as_string())
    print(f"[emailer] Sent digest with {len(articles)} featured articles to {email_to_list}.")
