import math

# Define Gourav's top 6 projects
projects = [
    {
        "repo": "GouravPatidar91/cybersaathi",
        "title": "CyberSaathi",
        "desc": "Women safety and cyber security platform",
        "tags": ["TypeScript", "NextJS", "Tailwind"],
        "stars": "0",
        "updated": "updated 1mo ago",
        "langs": [
            {"name": "TypeScript", "color": "#3178c6", "percent": 81},
            {"name": "JavaScript", "color": "#f1e05a", "percent": 14},
            {"name": "CSS", "color": "#563d7c", "percent": 5}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
    },
    {
        "repo": "GouravPatidar91/Curezy-main",
        "title": "Curezy",
        "desc": "Advanced healthcare management platform",
        "tags": ["TypeScript", "React", "NodeJS"],
        "stars": "0",
        "updated": "updated 3d ago",
        "langs": [
            {"name": "TypeScript", "color": "#3178c6", "percent": 75},
            {"name": "JavaScript", "color": "#f1e05a", "percent": 20},
            {"name": "HTML", "color": "#e34c26", "percent": 5}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
    },
    {
        "repo": "GouravPatidar91/campayn",
        "title": "Campayn",
        "desc": "Campaign management and analytics system",
        "tags": ["TypeScript", "React", "CSS"],
        "stars": "0",
        "updated": "updated 2mo ago",
        "langs": [
            {"name": "TypeScript", "color": "#3178c6", "percent": 90},
            {"name": "CSS", "color": "#563d7c", "percent": 6},
            {"name": "HTML", "color": "#e34c26", "percent": 4}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5zM15.54 8.46a5 5 0 0 1 0 7.07M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>'
    },
    {
        "repo": "GouravPatidar91/curezy-ai",
        "title": "Curezy AI",
        "desc": "AI-powered diagnostics assistant",
        "tags": ["Python", "AI", "PyTorch"],
        "stars": "0",
        "updated": "updated 2mo ago",
        "langs": [
            {"name": "Python", "color": "#3572A5", "percent": 95},
            {"name": "Shell", "color": "#89e051", "percent": 5}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#A78BFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1 0-3.12 3 3 0 0 1 0-4.88 2.5 2.5 0 0 1 0-3.12A2.5 2.5 0 0 1 9.5 2zM14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 0-3.12 3 3 0 0 0 0-4.88 2.5 2.5 0 0 0 0-3.12A2.5 2.5 0 0 0 14.5 2z"/></svg>'
    },
    {
        "repo": "GouravPatidar91/github-readme-stats",
        "title": "GitHub Readme Stats",
        "desc": "Self-hosted stats card generator",
        "tags": ["JavaScript", "NodeJS", "Vercel"],
        "stars": "0",
        "updated": "updated 2d ago",
        "langs": [
            {"name": "JavaScript", "color": "#f1e05a", "percent": 98},
            {"name": "CSS", "color": "#563d7c", "percent": 2}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#EC4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
    },
    {
        "repo": "GouravPatidar91/GouravPatidar91",
        "title": "GouravPatidar91",
        "desc": "My dynamic interactive GitHub profile",
        "tags": ["Python", "SVG", "Profile"],
        "stars": "1",
        "updated": "updated 5m ago",
        "langs": [
            {"name": "Python", "color": "#3572A5", "percent": 60},
            {"name": "SVG", "color": "#ff9900", "percent": 35},
            {"name": "Markdown", "color": "#083fa6", "percent": 5}
        ],
        "icon": '<svg x="16" y="44" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'
    }
]

# SVG configuration
width = 1180
height = 607
circumference = 2 * math.pi * 27  # 169.646

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,\'Liberation Mono\',monospace" role="img" aria-label="Projects">')
svg.append('<rect width="1180" height="607" fill="#0A101F"/>')
svg.append('<defs>')
svg.append('  <linearGradient id="acc_dark" x1="0" y1="0" x2="1" y2="0">')
svg.append('    <stop offset="0" stop-color="#7C3AED">')
svg.append('      <animate attributeName="stop-color" values="#7C3AED;#22D3EE;#10B981;#7C3AED" dur="10s" repeatCount="indefinite"/>')
svg.append('    </stop>')
svg.append('    <stop offset="1" stop-color="#10B981">')
svg.append('      <animate attributeName="stop-color" values="#10B981;#7C3AED;#22D3EE;#10B981" dur="10s" repeatCount="indefinite"/>')
svg.append('    </stop>')
svg.append('  </linearGradient>')
svg.append('</defs>')

svg.append('<text x="7" y="18" font-size="11" letter-spacing="2" fill="#22D3EE">PROJECTS.LIST</text>')
svg.append('<text x="135" y="18" font-size="10" fill="#475569">./projects.sh --all</text>')
svg.append('<line x1="5" y1="28" x2="1175" y2="28" stroke="url(#acc_dark)" stroke-width="1.5" opacity="0.7"/>')

grid = [
    {"tx": 5, "ty": 42, "delay": 0.25},
    {"tx": 597, "ty": 42, "delay": 0.40},
    {"tx": 5, "ty": 224, "delay": 0.55},
    {"tx": 597, "ty": 224, "delay": 0.70},
    {"tx": 5, "ty": 406, "delay": 0.85},
    {"tx": 597, "ty": 406, "delay": 1.00}
]

for idx, p in enumerate(projects):
    pos = grid[idx]
    tx, ty, delay = pos["tx"], pos["ty"], pos["delay"]
    blink = delay + 0.35
    
    # Format tags
    tags_svg = []
    curr_tag_x = 68
    for t in p["tags"]:
        tag_w = len(t) * 6 + 16
        tags_svg.append(f'<g transform="translate({curr_tag_x}, 104)">')
        tags_svg.append(f'  <rect width="{tag_w}" height="18" rx="9" fill="#1E293B"/>')
        tags_svg.append(f'  <text x="{tag_w // 2}" y="12" font-size="9" fill="#A78BFA" text-anchor="middle">{t}</text>')
        tags_svg.append('</g>')
        curr_tag_x += tag_w + 6
    tags_str = "\n".join(tags_svg)
    
    # Format circle slices
    circle_slices = []
    acc_percent = 0
    for idx_l, l in enumerate(p["langs"]):
        p_val = l["percent"]
        dash_len = p_val * circumference / 100
        space_len = circumference - dash_len
        offset = -acc_percent * circumference / 100
        circle_slices.append(f'      <circle cx="520" cy="90" r="27" fill="none" stroke="{l["color"]}" stroke-width="9" stroke-dasharray="{dash_len:.2f} {space_len:.2f}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90 520 90)" opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze"/></circle>')
        acc_percent += p_val
    circle_slices_str = "\n".join(circle_slices)
    
    # Format legend
    legend_svg = []
    y_start = 68
    for idx_l, l in enumerate(p["langs"]):
        y_pos = y_start + idx_l * 18
        legend_svg.append(f'      <circle cx="401" cy="{y_pos}" r="3.5" fill="{l["color"]}"/>')
        legend_svg.append(f'      <text x="410" y="{y_pos + 4}" font-size="10" fill="#94A3B8">{l["name"]} {l["percent"]}%</text>')
    legend_str = "\n".join(legend_svg)
    
    card = f"""
<a href="https://github.com/{p["repo"]}" target="_blank">
  <g opacity="0" transform="translate({tx},{ty})">
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze"/>
    <rect width="578" height="168" rx="12" fill="#0C1426" stroke="rgba(34,211,238,0.28)">
      <animate attributeName="stroke" values="rgba(34,211,238,0.22);rgba(34,211,238,0.5);rgba(34,211,238,0.22)" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
    <rect width="578" height="30" rx="12" fill="#0B1222"/>
    <rect y="18" width="578" height="12" fill="#0B1222"/>
    <line x1="0" y1="30" x2="578" y2="30" stroke="rgba(255,255,255,0.08)"/>
    <text x="16" y="19" font-size="10" fill="#94A3B8"><tspan fill="#22D3EE">&#8226;</tspan> {p["repo"]}</text>
    <circle cx="562" cy="15" r="3.5" fill="#10B981"><animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -2.5; 0 0" dur="5s" begin="{delay}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>
      {p["icon"]}
      
      <text x="68" y="60" font-size="15" font-weight="bold" fill="#F8FAFC">{p["title"]}<tspan fill="#22D3EE">_<animate attributeName="opacity" values="1;0;1" dur="1.2s" begin="{blink}s" repeatCount="indefinite"/></tspan></text>
      <text x="68" y="78" font-size="11" fill="#94A3B8">{p["desc"]}</text>
      
      {tags_str}
      
      <text x="68" y="145" font-size="10" fill="#94A3B8"><tspan fill="#22D3EE">&#9733;</tspan> {p["stars"]}<tspan fill="#475569" dx="14">{p["updated"]}</tspan></text>
      
      <circle cx="520" cy="90" r="27" fill="none" stroke="rgba(148,163,184,0.15)" stroke-width="9"/>
      {circle_slices_str}
      <text x="520" y="94" text-anchor="middle" font-size="11" font-weight="700" fill="#F8FAFC">{p["langs"][0]["percent"]}%</text>
      
      {legend_str}
    </g>
  </g>
</a>
"""
    svg.append(card)

svg.append("</svg>")

with open("projects.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print("projects.svg generated successfully.")
