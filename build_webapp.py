#!/usr/bin/env python3
"""
build_webapp.py - Generates the production-grade, mobile & web-friendly
AI Engineering & News Web Application (index.html).
"""

import json
from pathlib import Path

# Load seed data
seed_file = Path("seed_7days.json")
if seed_file.exists():
    with open(seed_file, "r") as f:
        seed_data = json.load(f)
else:
    seed_data = {}

seed_json_str = json.dumps(seed_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AI Pulse — Developer &amp; Applied AI Intelligence</title>
    <meta name="description" content="Daily curated technical AI digest, 7-day calendar archive, frontier model tracker, and task recommender for software engineers.">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    
    <!-- Supabase JS Client -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

    <style>
        :root {{
            --bg-base: #0a0d14;
            --bg-surface: #111622;
            --bg-card: #151c2c;
            --bg-card-hover: #1c253b;
            --border-subtle: #1e293b;
            --border-highlight: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-rose: #f43f5e;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.45);
            --shadow-glow: 0 0 25px -5px rgba(6, 182, 212, 0.25);
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-sans);
            min-height: 100vh;
            line-height: 1.5;
            overflow-x: hidden;
        }}

        /* Header & Nav */
        header {{
            position: sticky;
            top: 0;
            z-index: 50;
            background: rgba(10, 13, 20, 0.85);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 12px 18px;
        }}

        .header-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text-primary);
            cursor: pointer;
        }}

        .brand-icon {{
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 16px;
            color: #000;
        }}

        .brand-text {{
            font-size: 17px;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 40%, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .nav-tabs {{
            display: flex;
            gap: 6px;
            background: var(--bg-surface);
            padding: 4px;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
        }}

        .nav-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-family: var(--font-sans);
            font-size: 13px;
            font-weight: 600;
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.18s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}

        .nav-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.04);
        }}

        .nav-btn.active {{
            background: var(--bg-card-hover);
            color: var(--accent-cyan);
            border: 1px solid var(--border-highlight);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .status-pill {{
            font-size: 11px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.12);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.25);
            cursor: pointer;
        }}

        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--accent-emerald);
            box-shadow: 0 0 8px var(--accent-emerald);
        }}

        /* Main Container */
        main {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 18px 80px 18px;
        }}

        /* 7-Day Calendar Bar */
        .calendar-section {{
            margin-bottom: 24px;
        }}

        .calendar-title-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .section-label {{
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .calendar-strip {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .day-pill {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 10px 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .day-pill:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
        }}

        .day-pill.active {{
            background: linear-gradient(145deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.15));
            border-color: var(--accent-cyan);
            box-shadow: var(--shadow-glow);
        }}

        .day-pill .day-name {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .day-pill.active .day-name {{
            color: var(--accent-cyan);
        }}

        .day-pill .day-date {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
            margin: 2px 0 4px 0;
        }}

        .day-pill .article-count {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 999px;
            background: var(--border-subtle);
            color: var(--text-secondary);
            display: inline-block;
        }}

        .day-pill.active .article-count {{
            background: var(--accent-cyan);
            color: #000;
        }}

        /* Executive Highlights Card */
        .highlights-card {{
            background: linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(15, 23, 42, 0.95));
            border: 1px solid var(--border-highlight);
            border-left: 4px solid var(--accent-cyan);
            border-radius: var(--radius-lg);
            padding: 20px 24px;
            margin-bottom: 28px;
            box-shadow: var(--shadow-card);
        }}

        .highlights-header {{
            font-size: 14px;
            font-weight: 800;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .highlights-list {{
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 12px;
        }}

        .highlights-list li {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.5;
            background: rgba(255, 255, 255, 0.02);
            padding: 10px 14px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-subtle);
        }}

        .highlights-list li strong {{
            color: var(--text-primary);
            display: block;
            margin-bottom: 2px;
            font-size: 13px;
        }}

        /* Inshorts-Style Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 36px;
        }}

        .article-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-card);
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }}

        .article-card:hover {{
            transform: translateY(-3px);
            border-color: var(--border-highlight);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
        }}

        .article-card.groundbreaking {{
            border-color: rgba(244, 63, 94, 0.5);
            background: linear-gradient(180deg, rgba(244, 63, 94, 0.05) 0%, var(--bg-surface) 100%);
        }}

        .article-card.groundbreaking::before {{
            content: "🚨 GROUNDBREAKING DISCOVERY";
            display: block;
            background: linear-gradient(90deg, #f43f5e, #e11d48);
            color: #fff;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.07em;
            padding: 4px 14px;
        }}

        .card-media {{
            width: 100%;
            height: 180px;
            background: #0f1420;
            overflow: hidden;
            position: relative;
        }}

        .card-media img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}

        .article-card:hover .card-media img {{
            transform: scale(1.03);
        }}

        .card-media-fallback {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #131b2e, #0e1526);
            color: var(--text-muted);
            font-size: 32px;
        }}

        .card-body {{
            padding: 18px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }}

        .card-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            gap: 8px;
        }}

        .source-tag {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .badge-pill {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .badge-breakthrough {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }}
        .badge-devtools {{ background: rgba(67, 56, 202, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }}
        .badge-localai {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-production {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-research {{ background: rgba(139, 92, 246, 0.15); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.3); }}

        .card-title {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1.35;
            color: var(--text-primary);
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .continuation-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 11px;
            font-weight: 600;
            color: #a78bfa;
            background: rgba(139, 92, 246, 0.1);
            padding: 3px 8px;
            border-radius: 4px;
            margin-bottom: 10px;
            cursor: pointer;
            border: 1px solid rgba(139, 92, 246, 0.25);
            transition: background 0.15s ease;
        }}

        .continuation-badge:hover {{
            background: rgba(139, 92, 246, 0.2);
        }}

        .card-summary {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.55;
            margin-bottom: 14px;
            flex: 1;
        }}

        .dev-impact-box {{
            background: var(--bg-card);
            border-left: 3px solid var(--accent-cyan);
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 14px;
        }}

        .dev-impact-title {{
            font-size: 10.5px;
            font-weight: 700;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .dev-impact-text {{
            font-size: 12px;
            color: var(--text-primary);
            margin-top: 2px;
            line-height: 1.4;
        }}

        .card-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 14px;
        }}

        .tag-chip {{
            font-size: 10.5px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            background: var(--bg-base);
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid var(--border-subtle);
        }}

        .card-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 12px;
            border-top: 1px solid var(--border-subtle);
            font-size: 12px;
        }}

        .impact-meter {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 700;
            color: var(--accent-cyan);
        }}

        .action-link {{
            color: var(--accent-cyan);
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: color 0.15s ease;
        }}

        .action-link:hover {{
            color: #67e8f9;
        }}

        /* 1-Liners Table */
        .oneliners-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 40px;
        }}

        .oneliner-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid var(--border-subtle);
            gap: 16px;
        }}

        .oneliner-row:last-child {{
            border-bottom: none;
        }}

        .oneliner-source {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            min-width: 120px;
            text-transform: uppercase;
        }}

        .oneliner-content {{
            flex: 1;
            font-size: 13px;
        }}

        .oneliner-content a {{
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 600;
        }}

        .oneliner-content a:hover {{
            color: var(--accent-cyan);
        }}

        /* Frontier Model Tracker View */
        .models-view {{
            display: none;
        }}

        .models-view.active {{
            display: block;
        }}

        .models-filter-bar {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            margin-bottom: 20px;
            padding-bottom: 4px;
        }}

        .filter-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 999px;
            cursor: pointer;
            white-space: nowrap;
        }}

        .filter-chip.active {{
            background: var(--accent-cyan);
            color: #000;
            border-color: var(--accent-cyan);
        }}

        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
        }}

        .model-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}

        .model-name {{
            font-size: 18px;
            font-weight: 800;
            color: var(--text-primary);
        }}

        .model-lab {{
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-cyan);
        }}

        .model-specs-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            background: var(--bg-card);
            padding: 12px;
            border-radius: var(--radius-md);
            font-size: 12px;
        }}

        .spec-item .spec-label {{
            color: var(--text-muted);
            font-size: 10.5px;
            text-transform: uppercase;
        }}

        .spec-item .spec-val {{
            color: var(--text-primary);
            font-weight: 700;
            margin-top: 2px;
        }}

        /* Task Recommender View */
        .recommender-view {{
            display: none;
        }}

        .recommender-view.active {{
            display: block;
        }}

        .tasks-strip {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin-bottom: 24px;
        }}

        .task-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 10px 18px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }}

        .task-btn:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .task-btn.active {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2));
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
        }}

        .recommendation-panel {{
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-lg);
            padding: 24px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .rec-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 18px;
        }}

        .rec-badge {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }}

        .rec-model {{
            font-size: 18px;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 6px;
        }}

        .rec-desc {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Highlights & Milestone Archive View */
        .archive-view {{
            display: none;
        }}

        .archive-view.active {{
            display: block;
        }}

        .archive-controls {{
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}

        .year-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: var(--radius-sm);
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
        }}

        .year-btn.active {{
            background: var(--accent-cyan);
            color: #000;
            border-color: var(--accent-cyan);
        }}

        .milestones-timeline {{
            border-left: 2px solid var(--border-subtle);
            padding-left: 24px;
            margin-left: 10px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .milestone-item {{
            position: relative;
        }}

        .milestone-item::before {{
            content: '';
            position: absolute;
            left: -31px;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan);
        }}

        .milestone-date {{
            font-size: 12px;
            font-family: var(--font-mono);
            color: var(--accent-cyan);
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .milestone-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
        }}

        .milestone-desc {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Modal */
        .modal-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 100;
            padding: 16px;
        }}

        .modal-overlay.active {{
            display: flex;
        }}

        .modal-box {{
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-lg);
            max-width: 480px;
            width: 100%;
            padding: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        }}

        .form-group {{
            margin-bottom: 16px;
        }}

        .form-group label {{
            display: block;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-secondary);
            margin-bottom: 6px;
            text-transform: uppercase;
        }}

        .form-input {{
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 10px 14px;
            font-family: var(--font-mono);
            font-size: 13px;
            color: var(--text-primary);
            outline: none;
        }}

        .form-input:focus {{
            border-color: var(--accent-cyan);
        }}

        .btn-primary {{
            background: var(--accent-cyan);
            color: #000;
            border: none;
            padding: 10px 18px;
            border-radius: var(--radius-sm);
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            width: 100%;
        }}

        /* Mobile Adjustments */
        @media (max-width: 768px) {{
            header {{
                padding: 10px 14px;
            }}
            .header-inner {{
                flex-direction: column;
                align-items: stretch;
            }}
            .brand-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .nav-tabs {{
                overflow-x: auto;
                width: 100%;
            }}
            .cards-grid {{
                grid-template-columns: 1fr;
            }}
            .calendar-strip {{
                grid-template-columns: repeat(7, minmax(75px, 1fr));
            }}
            .oneliner-row {{
                flex-direction: column;
                gap: 4px;
            }}
            .oneliner-source {{
                min-width: auto;
            }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-inner">
            <div class="brand-row">
                <a class="brand" onclick="switchView('feed')">
                    <div class="brand-icon">⚡</div>
                    <div class="brand-text">AI PULSE // DIGEST</div>
                </a>
                <div class="status-pill" id="supabase-status-pill" onclick="openSupabaseModal()">
                    <div class="status-dot"></div>
                    <span id="supabase-status-label">Live Data Sync</span>
                </div>
            </div>

            <nav class="nav-tabs">
                <button class="nav-btn active" id="tab-feed" onclick="switchView('feed')">📰 Daily Feed</button>
                <button class="nav-btn" id="tab-models" onclick="switchView('models')">🏆 Model Tracker</button>
                <button class="nav-btn" id="tab-recommender" onclick="switchView('recommender')">🎯 Task Recommender</button>
                <button class="nav-btn" id="tab-archive" onclick="switchView('archive')">📅 Landmark Milestones</button>
            </nav>
        </div>
    </header>

    <main>
        <!-- 1. DAILY FEED VIEW -->
        <section id="view-feed" class="feed-view">
            <!-- 7-Day Calendar Strip -->
            <div class="calendar-section">
                <div class="calendar-title-row">
                    <div class="section-label">
                        <span>🗓️ Past 7 Days Archive (Click a Date)</span>
                    </div>
                    <div style="font-size:12px; color:var(--text-muted);">
                        Rolling 7-Day Strict Index
                    </div>
                </div>
                <div class="calendar-strip" id="calendar-strip"></div>
            </div>

            <!-- Executive Highlights for Selected Day -->
            <div class="highlights-card" id="highlights-container">
                <div class="highlights-header">
                    <span>⚡ Executive Highlights (3-Minute Summary)</span>
                </div>
                <ul class="highlights-list" id="highlights-list"></ul>
            </div>

            <!-- Inshorts Cards Grid -->
            <div class="section-label" style="margin-bottom:14px;">
                <span>🏆 Top 10 Developer &amp; Applied AI Breakthroughs</span>
            </div>
            <div class="cards-grid" id="cards-grid"></div>

            <!-- Quick Hits (1-Liners) Section -->
            <div class="oneliners-card">
                <div class="section-label" style="margin-bottom: 14px; display:flex; justify-content:space-between;">
                    <span>⚡ The Quick Hits (All Fresh Stories in 1-Line)</span>
                    <span id="oneliners-count-badge" style="font-size:11px; color:var(--accent-cyan);">0 items</span>
                </div>
                <div id="oneliners-container"></div>
            </div>
        </section>

        <!-- 2. FRONTIER MODEL TRACKER VIEW -->
        <section id="view-models" class="models-view">
            <div class="calendar-title-row">
                <div class="section-label">
                    <span>🏆 Frontier Model Matrix by Lab (2025-2026)</span>
                </div>
            </div>

            <div class="models-filter-bar">
                <button class="filter-chip active" onclick="filterModels('All')">All Labs</button>
                <button class="filter-chip" onclick="filterModels('OpenAI')">OpenAI</button>
                <button class="filter-chip" onclick="filterModels('Anthropic')">Anthropic</button>
                <button class="filter-chip" onclick="filterModels('Google DeepMind')">Google DeepMind</button>
                <button class="filter-chip" onclick="filterModels('DeepSeek')">DeepSeek</button>
                <button class="filter-chip" onclick="filterModels('Meta AI')">Meta AI</button>
                <button class="filter-chip" onclick="filterModels('xAI')">xAI</button>
                <button class="filter-chip" onclick="filterModels('Mistral')">Mistral</button>
                <button class="filter-chip" onclick="filterModels('Alibaba')">Alibaba</button>
            </div>

            <div class="models-grid" id="models-grid"></div>
        </section>

        <!-- 3. TASK-BASED RECOMMENDER VIEW -->
        <section id="view-recommender" class="recommender-view">
            <div class="calendar-title-row">
                <div class="section-label">
                    <span>🎯 What Model Should I Use For My Task?</span>
                </div>
            </div>

            <div class="tasks-strip">
                <button class="task-btn active" onclick="selectTask('coding')">💻 Coding &amp; Agentic Dev</button>
                <button class="task-btn" onclick="selectTask('reasoning')">🧠 Complex Math &amp; Reasoning</button>
                <button class="task-btn" onclick="selectTask('video')">🎬 Video Generation &amp; Editing</button>
                <button class="task-btn" onclick="selectTask('image')">🎨 Image Generation &amp; Design</button>
                <button class="task-btn" onclick="selectTask('automation')">⚡ Low-Cost Extraction &amp; Workflows</button>
                <button class="task-btn" onclick="selectTask('local')">🔒 Local &amp; Private Offline Inference</button>
                <button class="task-btn" onclick="selectTask('context')">📚 Massive Context (1M-2M+ Tokens)</button>
            </div>

            <div id="recommendation-panel" class="recommendation-panel"></div>
        </section>

        <!-- 4. LANDMARK ARCHIVE VIEW -->
        <section id="view-archive" class="archive-view">
            <div class="calendar-title-row">
                <div class="section-label">
                    <span>📅 Landmark AI Milestones (Last 2 Years: 2024–2026)</span>
                </div>
            </div>

            <div class="archive-controls">
                <button class="year-btn active" onclick="filterArchiveYear('2026')">2026</button>
                <button class="year-btn" onclick="filterArchiveYear('2025')">2025</button>
                <button class="year-btn" onclick="filterArchiveYear('2024')">2024</button>
            </div>

            <div class="milestones-timeline" id="milestones-timeline"></div>
        </section>
    </main>

    <!-- Supabase Configuration Modal -->
    <div class="modal-overlay" id="supabase-modal" onclick="closeModalOnBackdrop(event)">
        <div class="modal-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <h3 style="font-size:16px; font-weight:800;">⚙️ Supabase Integration</h3>
                <span onclick="closeSupabaseModal()" style="cursor:pointer; color:var(--text-muted); font-size:18px;">&times;</span>
            </div>
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:16px;">
                Connect this web app to your Supabase PostgreSQL project. Articles older than 7 days are automatically pruned by the backend cron.
            </p>
            <div class="form-group">
                <label>Supabase URL</label>
                <input class="form-input" id="cfg-supabase-url" placeholder="https://xyz.supabase.co">
            </div>
            <div class="form-group">
                <label>Supabase Public Anon Key</label>
                <input class="form-input" id="cfg-supabase-key" type="password" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...">
            </div>
            <button class="btn-primary" onclick="saveSupabaseConfig()">Save &amp; Sync with Supabase</button>
            <button onclick="usePreloadedData()" style="background:transparent; border:1px solid var(--border-subtle); color:var(--text-secondary); padding:8px; border-radius:var(--radius-sm); font-size:12px; width:100%; margin-top:8px; cursor:pointer;">
                Use Preloaded 7-Day Live Dataset
            </button>
        </div>
    </div>

    <!-- Continuation Linked Article Modal -->
    <div class="modal-overlay" id="continuation-modal" onclick="closeModalOnBackdrop(event)">
        <div class="modal-box" style="max-width:560px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <span style="font-size:11px; font-weight:800; color:#a78bfa; text-transform:uppercase;">↳ Linked Story Context</span>
                <span onclick="closeContinuationModal()" style="cursor:pointer; color:var(--text-muted); font-size:18px;">&times;</span>
            </div>
            <h3 id="cont-modal-title" style="font-size:17px; font-weight:800; margin-bottom:8px; line-height:1.35;"></h3>
            <div id="cont-modal-date" style="font-size:12px; color:var(--text-muted); margin-bottom:12px;"></div>
            <p id="cont-modal-summary" style="font-size:13.5px; color:var(--text-secondary); line-height:1.55; margin-bottom:16px;"></p>
            <a id="cont-modal-link" href="#" target="_blank" class="action-link">Open Original Source &rarr;</a>
        </div>
    </div>

    <script>
        // Seeded 7-Day Archive Data (Generated from Live Feeds)
        const SEED_DATA = {seed_json_str};

        // Milestone Archive (2024 - 2026)
        const MILESTONES = [
            {{ year: "2026", date: "Sep 2026", title: "Scal3R & Internet-Scale Dexterous Robotics", desc: "Breakthroughs in multi-relative pose estimation for 3D reconstruction and internet-scale human demonstration retrieval for humanoid manipulation." }},
            {{ year: "2026", date: "Jul 2026", title: "Claude 3.7 Sonnet & Hybrid Reasoning", desc: "Anthropic introduces hybrid immediate-and-thinking reasoning with native terminal execution for agentic engineering." }},
            {{ year: "2026", date: "May 2026", title: "xAI Colossus 2 - 1st Gigawatt Datacenter", desc: "xAI begins operations on the first gigawatt-scale AI computing infrastructure for Grok-3 frontier training." }},
            {{ year: "2025", date: "Dec 2025", title: "DeepSeek-R1 Open Weight Reasoning", desc: "DeepSeek releases R1, demonstrating competitive reasoning with o1 through pure reinforcement learning at a fraction of compute cost." }},
            {{ year: "2025", date: "Oct 2025", title: "OpenAI o3 Frontier Reasoning", desc: "OpenAI establishes new records on competitive programming (Codeforces 2700+) and frontier science benchmarks." }},
            {{ year: "2025", date: "Jul 2025", title: "Llama 3.1 405B Open Weights", desc: "Meta AI open-sources its first frontier-scale 405B parameter model, enabling distillation into local 8B and 70B variants." }},
            {{ year: "2025", date: "Feb 2025", title: "Gemini 2.0 Flash Production Leap", desc: "Google DeepMind delivers sub-200ms multimodal inference with native agentic search and code execution." }},
            {{ year: "2024", date: "Jun 2024", title: "Claude 3.5 Sonnet Coding Revolution", desc: "Anthropic releases Claude 3.5 Sonnet, establishing the gold standard for software engineering and tool orchestration." }},
            {{ year: "2024", date: "May 2024", title: "GPT-4o Omnimodal Release", desc: "OpenAI debuts real-time voice-to-voice and vision processing natively within a single multimodal neural network." }},
            {{ year: "2024", date: "Feb 2024", title: "Sora & Gemini 1.5 Pro 2M Context", desc: "OpenAI showcases generative physics video with Sora, and Google unlocks million-token context windows." }}
        ];

        // Frontier Models Matrix
        const FRONTIER_MODELS = [
            {{ name: "Claude 3.7 Sonnet", lab: "Anthropic", date: "2026", context: "200K tokens", license: "Proprietary API", architecture: "Dense", reasoning: "Hybrid / Extended", coding: "SOTA (92.4%)", strength: "Best for Agentic Coding, Refactoring, Terminal tool use" }},
            {{ name: "OpenAI o3", lab: "OpenAI", date: "2025", context: "200K tokens", license: "Proprietary API", architecture: "Reasoning Model", reasoning: "Top Frontier (98%)", coding: "SOTA Competitive", strength: "Complex mathematical proofs, hard algorithmic logic" }},
            {{ name: "DeepSeek-R1", lab: "DeepSeek", date: "2025", context: "128K tokens", license: "Open Weights (MIT)", architecture: "MoE (671B / 37B active)", reasoning: "Top Frontier (96%)", coding: "Near-o1 Level", strength: "Self-hosted high-reasoning, low inference cost" }},
            {{ name: "Gemini 2.0 Flash", lab: "Google DeepMind", date: "2025", context: "1M tokens", license: "Proprietary API", architecture: "MoE", reasoning: "Strong (88%)", coding: "Fast & Precise", strength: "Sub-200ms latency, multimodal video/audio processing" }},
            {{ name: "Llama 3.3 70B", lab: "Meta AI", date: "2025", context: "128K tokens", license: "Open Weights (Community)", architecture: "Dense (70B)", reasoning: "Strong (86%)", coding: "Excellent", strength: "Highest quality offline inference on dual RTX 4090s" }},
            {{ name: "Qwen 2.5 Coder 32B", lab: "Alibaba", date: "2025", context: "128K tokens", license: "Open Weights (Apache 2)", architecture: "Dense (32B)", reasoning: "Good (84%)", coding: "SOTA Open Coding", strength: "Best local coding model fit on a single 16GB GPU" }},
            {{ name: "Grok 3", lab: "xAI", date: "2025", context: "256K tokens", license: "Proprietary API", architecture: "Colossus Scale", reasoning: "Frontier (94%)", coding: "Very Strong", strength: "Real-time world knowledge synthesis, raw throughput" }},
            {{ name: "Mistral Large 2", lab: "Mistral", date: "2024", context: "128K tokens", license: "Open Weights / API", architecture: "123B Dense", reasoning: "Strong (85%)", coding: "Multilingual SOTA", strength: "European compliance, 80+ programming languages" }}
        ];

        // Task Recommendations
        const TASK_RECOMMENDATIONS = {{
            coding: {{
                title: "💻 Coding & Agentic Software Engineering",
                topPick: {{ model: "Claude 3.7 Sonnet", lab: "Anthropic", reason: "Unmatched at understanding massive git diffs, multi-file edits, and executing terminal CLI commands via tools." }},
                budget: {{ model: "Gemini 2.0 Flash", lab: "Google", reason: "Fastest response time and fractions of a cent per 1k tokens for background linting and inline autocomplete." }},
                local: {{ model: "Qwen 2.5 Coder 32B (Q4_K_M GGUF)", lab: "Alibaba", reason: "Runs comfortably in 20GB VRAM / Ollama with coding benchmark scores matching GPT-4o." }},
                tips: "Provide repository file trees and clear reproduction scripts. For agentic loops, limit maximum autonomous steps to prevent cost runaway."
            }},
            reasoning: {{
                title: "🧠 Complex Math, Logic & Deep Planning",
                topPick: {{ model: "OpenAI o3 / o1", lab: "OpenAI", reason: "Gold-standard test-time compute scaling that thinks through edge cases before outputting a token." }},
                budget: {{ model: "DeepSeek-R1 API", lab: "DeepSeek", reason: "Matches o1 benchmark curves at ~90% lower API cost per million tokens." }},
                local: {{ model: "DeepSeek-R1-Distill-Qwen-32B", lab: "DeepSeek / Qwen", reason: "Distilled reasoning traces fit onto single GPU setups without requiring 671B parameters." }},
                tips: "Do NOT use few-shot prompt templates with reasoning models; let the model generate its own internal chain of thought."
            }},
            video: {{
                title: "🎬 Video Generation & Neural Motion Editing",
                topPick: {{ model: "Runway Gen-3 Alpha / Sora", lab: "Runway / OpenAI", reason: "Exceptional temporal coherence, photorealistic camera motions, and cinematic lighting control." }},
                budget: {{ model: "Kling AI / Luma Dream Machine", lab: "Kuaishou / Luma", reason: "Generous free tier credits with fast rendering speeds and consistent motion dynamics." }},
                local: {{ model: "CogVideoX-5B / Wan2.1", lab: "THUDM / Alibaba", reason: "Leading open-weights video diffusion models executable on 24GB VRAM with ComfyUI." }},
                tips: "Specify lens focal length (e.g. '35mm anamorphic') and exact physical motion vectors to prevent morphing artifacts."
            }},
            image: {{
                title: "🎨 Image Generation & Asset Design",
                topPick: {{ model: "Midjourney v6.1 / Flux.1 Pro", lab: "Midjourney / Black Forest Labs", reason: "Highest aesthetic composition, typography rendering, and photorealistic skin textures." }},
                budget: {{ model: "Flux.1 Schnell", lab: "Black Forest Labs", reason: "4-step ultra-fast distillation with commercial Apache 2.0 license." }},
                local: {{ model: "Flux.1 Dev (NF4 / GGUF)", lab: "Black Forest Labs", reason: "Runs under 12GB VRAM using Forge or ComfyUI with full LoRA compatibility." }},
                tips: "Use natural descriptive English paragraphs rather than comma-separated tag spam for Flux and Midjourney v6."
            }},
            automation: {{
                title: "⚡ Low-Cost Bulk Extraction & Workflows",
                topPick: {{ model: "Gemini 2.0 Flash", lab: "Google", reason: "Extremely aggressive pricing ($0.10 / 1M input) with 1M context window and near-zero latency." }},
                budget: {{ model: "GPT-4o-mini", lab: "OpenAI", reason: "Reliable structured JSON output schema support for bulk classification tasks." }},
                local: {{ model: "Llama 3.2 3B / Qwen 2.5 7B", lab: "Meta / Alibaba", reason: "Blistering fast throughput (150+ tokens/sec) for offline edge document processing." }},
                tips: "Always enforce strict JSON Schema validation mode when extracting tabular records."
            }},
            local: {{
                title: "🔒 Local & Private Offline Inference",
                topPick: {{ model: "Llama 3.3 70B (Q4_K_M GGUF)", lab: "Meta AI", reason: "The undisputed champion of 70B open weights. Matches original GPT-4 on almost all tasks." }},
                budget: {{ model: "Qwen 2.5 14B (Q5_K_M GGUF)", lab: "Alibaba", reason: "Superb sweet spot between 8B and 70B; fits entirely inside 12GB RTX 3060/4060 VRAM." }},
                local: {{ model: "Ollama / vLLM / llama.cpp", lab: "Open Source", reason: "Top tier inference engines with OpenAI-compatible local endpoints at http://localhost:11434/v1." }},
                tips: "Use GGUF format with `llama-server` or `Ollama` for automatic CPU/GPU layer offloading on mixed memory systems."
            }},
            context: {{
                title: "📚 Massive Context (1M-2M+ Tokens) Document Analysis",
                topPick: {{ model: "Gemini 1.5 Pro / 2.0 Pro", lab: "Google DeepMind", reason: "Flawless 2,000,000 token needle-in-a-haystack retrieval across entire codebases and video streams." }},
                budget: {{ model: "Gemini 2.0 Flash", lab: "Google DeepMind", reason: "1,000,000 token context window available for pennies." }},
                local: {{ model: "Llama 3.1 70B (128K context)", lab: "Meta AI", reason: "Reliable 128K context window for local enterprise compliance." }},
                tips: "Place key search instructions and queries at the VERY END of the long context prompt for optimal recall."
            }}
        }};

        // State
        let activeDateKey = Object.keys(SEED_DATA)[0] || "today";
        let currentView = "feed";
        let supabaseClient = null;

        // Init
        document.addEventListener("DOMContentLoaded", () => {{
            initSupabaseFromStorage();
            renderCalendarStrip();
            renderActiveDay();
            renderModelTracker("All");
            selectTask("coding");
            filterArchiveYear("2026");
        }});

        function switchView(viewName) {{
        });

        function switchView(viewName) {
            currentView = viewName;
            document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll("main > section").forEach(s => s.style.display = "none");

            document.getElementById(`tab-${viewName}`).classList.add("active");
            document.getElementById(`view-${viewName}`).style.display = "block";
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function initSupabaseFromStorage() {
            // 1. Check if hosted on Vercel with native Supabase integration
            try {
                const resp = await fetch('/api/config');
                if (resp.ok) {
                    const data = await resp.json();
                    if (data.supabaseUrl && data.supabaseAnonKey) {
                        connectSupabase(data.supabaseUrl, data.supabaseAnonKey, "Vercel + Supabase Live");
                        return;
                    }
                }
            } catch (e) {
                // Not running on serverless Vercel host or offline
            }

            // 2. Check localStorage
            const url = localStorage.getItem("ai_pulse_sb_url");
            const key = localStorage.getItem("ai_pulse_sb_key");
            if (url && key) {
                connectSupabase(url, key, "Supabase Live Sync");
            }
        }

        function connectSupabase(url, key, label) {
            if (window.supabase) {
                try {
                    supabaseClient = window.supabase.createClient(url, key);
                    document.getElementById("supabase-status-label").innerText = label;
                    document.getElementById("supabase-status-pill").style.borderColor = "var(--accent-cyan)";
                    fetchLiveArticlesFromSupabase();
                } catch (e) {
                    console.error("Supabase connect error:", e);
                }
            }
        }

        async function fetchLiveArticlesFromSupabase() {
            if (!supabaseClient) return;
            try {
                const { data, error } = await supabaseClient
                    .from('articles')
                    .select('*')
                    .order('published_date', { ascending: false });

                if (!error && data && data.length > 0) {
                    groupAndMergeSupabaseArticles(data);
                }
            } catch (e) {
                console.warn("Could not fetch live articles, using preloaded data:", e);
            }
        }

        function groupAndMergeSupabaseArticles(articles) {
            const grouped = {};
            articles.forEach(a => {
                const dayKey = (a.published_date || '').slice(0, 10);
                if (!dayKey) return;
                if (!grouped[dayKey]) {
                    const d = new Date(dayKey + 'T00:00:00Z');
                    grouped[dayKey] = {
                        date: dayKey,
                        day_name: d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }),
                        highlights: [
                            `<strong>Live Updates:</strong> ${articles.length} active articles currently indexed in Supabase.`,
                            `<strong>Strict Retention:</strong> Articles automatically pruned after 7 days.`
                        ],
                        top_10: [],
                        one_liners: []
                    };
                }
                if (grouped[dayKey].top_10.length < 10) {
                    grouped[dayKey].top_10.push(a);
                } else {
                    grouped[dayKey].one_liners.push(a);
                }
            });

            // If we received valid days from Supabase, update SEED_DATA in-memory
            if (Object.keys(grouped).length > 0) {
                Object.assign(SEED_DATA, grouped);
                activeDateKey = Object.keys(grouped)[0];
                renderCalendarStrip();
                renderActiveDay();
            }
        }

        function renderCalendarStrip() {
            const strip = document.getElementById("calendar-strip");
            strip.innerHTML = "";
            const dates = Object.keys(SEED_DATA);

            dates.forEach((dateKey, index) => {{
                const dayData = SEED_DATA[dateKey];
                const count = (dayData.top_10 || []).length + (dayData.one_liners || []).length;
                const pill = document.createElement("div");
                pill.className = `day-pill ${{dateKey === activeDateKey ? 'active' : ''}}`;
                pill.onclick = () => selectDay(dateKey);

                const d = new Date(dayData.date + "T00:00:00Z");
                const dayName = index === 0 ? "Today" : (index === 1 ? "Yesterday" : d.toLocaleDateString('en-US', {{ weekday: 'short' }}));
                const monthDay = d.toLocaleDateString('en-US', {{ month: 'short', day: 'numeric' }});

                pill.innerHTML = `
                    <div class="day-name">${{dayName}}</div>
                    <div class="day-date">${{monthDay}}</div>
                    <div class="article-count">${{count}} items</div>
                `;
                strip.appendChild(pill);
            }});
        }}

        function selectDay(dateKey) {{
            activeDateKey = dateKey;
            renderCalendarStrip();
            renderActiveDay();
        }}

        function renderActiveDay() {{
            const dayData = SEED_DATA[activeDateKey];
            if (!dayData) return;

            // 1. Render Highlights
            const hlList = document.getElementById("highlights-list");
            hlList.innerHTML = "";
            (dayData.highlights || []).forEach(hl => {{
                const li = document.createElement("li");
                li.innerHTML = hl;
                hlList.appendChild(li);
            }});

            // 2. Render Cards Grid
            const cardsGrid = document.getElementById("cards-grid");
            cardsGrid.innerHTML = "";
            const topArticles = dayData.top_10 || [];

            topArticles.forEach((a, idx) => {{
                const card = document.createElement("div");
                card.className = `article-card ${{a.is_groundbreaking ? 'groundbreaking' : ''}}`;

                let mediaHtml = "";
                if (a.image_url) {{
                    mediaHtml = `
                    <div class="card-media">
                        <img src="${{a.image_url}}" alt="Thumbnail" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'card-media-fallback\\'>⚡</div>'">
                    </div>`;
                }} else {{
                    const iconMap = {{
                        "BREAKTHROUGH": "🚨", "DEV TOOLS": "🛠️", "LOCAL AI": "⚡", "PRODUCTION": "🚀", "RESEARCH": "🔬"
                    }};
                    mediaHtml = `
                    <div class="card-media">
                        <div class="card-media-fallback">${{iconMap[a.category_tag] || '📄'}}</div>
                    </div>`;
                }}

                let contHtml = "";
                if (a.continuation) {{
                    contHtml = `
                    <div class="continuation-badge" onclick="showContinuationModal('${{escapeHtml(a.continuation.title)}}', '${{a.continuation.published_date || ''}}', '↳ Continuation of earlier story: ${{escapeHtml(a.continuation.title)}}. Click source to verify.', '${{a.continuation.url}}')">
                        ↳ Continued from: ${{a.continuation.title.slice(0, 32)}}...
                    </div>`;
                }}

                const tagPills = (a.entities || []).slice(0, 4).map(e => `<span class="tag-chip">#${{escapeHtml(e)}}</span>`).join("");

                card.innerHTML = `
                    ${{mediaHtml}}
                    <div class="card-body">
                        <div class="card-meta">
                            <span class="source-tag">${{escapeHtml(a.source)}}</span>
                            <span class="badge-pill badge-${{(a.category_tag || 'research').toLowerCase().replace(' ', '')}}">
                                ${{a.category_tag}}
                            </span>
                        </div>

                        <div class="card-title">${{escapeHtml(a.title)}}</div>
                        ${{contHtml}}

                        <div class="card-summary">${{escapeHtml(a.summary)}}</div>

                        <div class="dev-impact-box">
                            <div class="dev-impact-title">🛠️ Developer &amp; Practical Use Case</div>
                            <div class="dev-impact-text">${{escapeHtml(a.dev_use_case || 'Applicable for model integration & development workflows.')}}</div>
                        </div>

                        <div class="card-tags">${{tagPills}}</div>

                        <div class="card-footer">
                            <div class="impact-meter">
                                <span>⚡ Impact: ${{a.dev_impact_score || 85}}/100</span>
                            </div>
                            <a href="${{a.url}}" target="_blank" rel="noopener noreferrer" class="action-link">
                                Read Source &rarr;
                            </a>
                        </div>
                    </div>
                `;
                cardsGrid.appendChild(card);
            }});

            // 3. Render 1-Liners
            const onelinersContainer = document.getElementById("oneliners-container");
            onelinersContainer.innerHTML = "";
            const oneliners = dayData.one_liners || [];
            document.getElementById("oneliners-count-badge").innerText = `${{oneliners.length}} items`;

            oneliners.forEach(ol => {{
                const row = document.createElement("div");
                row.className = "oneliner-row";
                row.innerHTML = `
                    <div class="oneliner-source">${{escapeHtml(ol.source.slice(0, 16))}}</div>
                    <div class="oneliner-content">
                        <a href="${{ol.url}}" target="_blank" rel="noopener noreferrer">${{escapeHtml(ol.title)}}</a>
                        <span style="color:var(--text-muted); margin-left:6px;">&bull; ${{escapeHtml(ol.one_liner || ol.summary)}}</span>
                    </div>
                    <div>
                        <a href="${{ol.url}}" target="_blank" class="action-link" style="font-size:12px;">View &rarr;</a>
                    </div>
                `;
                onelinersContainer.appendChild(row);
            }});
        }}

        function renderModelTracker(selectedLab) {{
            const grid = document.getElementById("models-grid");
            grid.innerHTML = "";

            const filtered = selectedLab === "All" 
                ? FRONTIER_MODELS 
                : FRONTIER_MODELS.filter(m => m.lab.toLowerCase().includes(selectedLab.toLowerCase()));

            filtered.forEach(m => {{
                const card = document.createElement("div");
                card.className = "model-card";
                card.innerHTML = `
                    <div class="model-header">
                        <div>
                            <div class="model-name">${{m.name}}</div>
                            <div class="model-lab">${{m.lab}} &bull; ${{m.date}}</div>
                        </div>
                        <span class="badge-pill badge-production">${{m.license}}</span>
                    </div>

                    <div class="model-specs-grid">
                        <div class="spec-item">
                            <div class="spec-label">Context Window</div>
                            <div class="spec-val">${{m.context}}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">Architecture</div>
                            <div class="spec-val">${{m.architecture}}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">Reasoning Strength</div>
                            <div class="spec-val">${{m.reasoning}}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-label">Coding Score</div>
                            <div class="spec-val" style="color:var(--accent-cyan);">${{m.coding}}</div>
                        </div>
                    </div>

                    <div style="font-size:13px; color:var(--text-secondary); line-height:1.45;">
                        <strong style="color:var(--text-primary);">Best Application:</strong> ${{m.strength}}
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function filterModels(lab) {{
            document.querySelectorAll(".filter-chip").forEach(c => {{
                c.classList.toggle("active", c.innerText.includes(lab) || (lab === 'All' && c.innerText === 'All Labs'));
            }});
            renderModelTracker(lab);
        }}

        function selectTask(taskKey) {{
            document.querySelectorAll(".task-btn").forEach(b => {{
                b.classList.toggle("active", b.getAttribute("onclick").includes(taskKey));
            }});

            const rec = TASK_RECOMMENDATIONS[taskKey];
            const panel = document.getElementById("recommendation-panel");

            panel.innerHTML = `
                <div class="rec-box" style="border-top: 3px solid var(--accent-cyan);">
                    <div class="rec-badge" style="color:var(--accent-cyan);">🥇 Top Recommended Choice</div>
                    <div class="rec-model">${{rec.topPick.model}}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">${{rec.topPick.lab}}</div>
                    <div class="rec-desc">${{rec.topPick.reason}}</div>
                </div>

                <div class="rec-box" style="border-top: 3px solid var(--accent-amber);">
                    <div class="rec-badge" style="color:var(--accent-amber);">💰 Budget / Fast Alternative</div>
                    <div class="rec-model">${{rec.budget.model}}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">${{rec.budget.lab}}</div>
                    <div class="rec-desc">${{rec.budget.reason}}</div>
                </div>

                <div class="rec-box" style="border-top: 3px solid var(--accent-emerald);">
                    <div class="rec-badge" style="color:var(--accent-emerald);">💻 Open-Source / Local Choice</div>
                    <div class="rec-model">${{rec.local.model}}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">${{rec.local.lab}}</div>
                    <div class="rec-desc">${{rec.local.reason}}</div>
                </div>

                <div class="rec-box" style="grid-column: 1 / -1; background:var(--bg-surface); border:1px dashed var(--border-highlight);">
                    <div class="rec-badge" style="color:var(--accent-purple);">💡 Engineering Pro-Tips &amp; Best Practices</div>
                    <div class="rec-desc" style="color:var(--text-primary); font-size:13.5px;">${{rec.tips}}</div>
                </div>
            `;
        }}

        function filterArchiveYear(year) {{
            document.querySelectorAll(".year-btn").forEach(b => {{
                b.classList.toggle("active", b.innerText === year);
            }});

            const timeline = document.getElementById("milestones-timeline");
            timeline.innerHTML = "";

            const filtered = MILESTONES.filter(m => m.year === year);
            filtered.forEach(m => {{
                const item = document.createElement("div");
                item.className = "milestone-item";
                item.innerHTML = `
                    <div class="milestone-date">${{m.date}}</div>
                    <div class="milestone-title">${{m.title}}</div>
                    <div class="milestone-desc">${{m.desc}}</div>
                `;
                timeline.appendChild(item);
            }});
        }}

        // Modal Handlers
        function openSupabaseModal() {{
            document.getElementById("cfg-supabase-url").value = localStorage.getItem("ai_pulse_sb_url") || "";
            document.getElementById("cfg-supabase-key").value = localStorage.getItem("ai_pulse_sb_key") || "";
            document.getElementById("supabase-modal").classList.add("active");
        }}

        function closeSupabaseModal() {{
            document.getElementById("supabase-modal").classList.remove("active");
        }}

        function closeModalOnBackdrop(e) {{
            if (e.target.classList.contains("modal-overlay")) {{
                e.target.classList.remove("active");
            }}
        }}

        function saveSupabaseConfig() {{
            const url = document.getElementById("cfg-supabase-url").value.trim();
            const key = document.getElementById("cfg-supabase-key").value.trim();
            if (!url || !key) {{
                alert("Please enter both Supabase URL and Anon Key.");
                return;
            }}
            localStorage.setItem("ai_pulse_sb_url", url);
            localStorage.setItem("ai_pulse_sb_key", key);
            initSupabaseFromStorage();
            closeSupabaseModal();
            alert("Supabase credentials saved! The app will query your Supabase instance.");
        }}

        function usePreloadedData() {{
            localStorage.removeItem("ai_pulse_sb_url");
            localStorage.removeItem("ai_pulse_sb_key");
            supabaseClient = null;
            document.getElementById("supabase-status-label").innerText = "Live Preloaded Dataset";
            closeSupabaseModal();
        }}

        function showContinuationModal(title, date, summary, url) {{
            document.getElementById("cont-modal-title").innerText = title;
            document.getElementById("cont-modal-date").innerText = "Preceding Story Date: " + (date || "Recent");
            document.getElementById("cont-modal-summary").innerText = summary;
            document.getElementById("cont-modal-link").href = url;
            document.getElementById("continuation-modal").classList.add("active");
        }}

        function closeContinuationModal() {{
            document.getElementById("continuation-modal").classList.remove("active");
        }}

        function escapeHtml(str) {{
            if (!str) return "";
            return String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}
    </script>
</body>
</html>
"""

output_path = Path("index.html")
output_path.write_text(html_template, encoding="utf-8")
print(f"Generated {output_path.resolve()} ({output_path.stat().st_size / 1024:.1f} KB)")
