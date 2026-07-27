import re
import random
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import scipy.ndimage as ndimage

# ==============================================================================
# 1. IMAGE PROCESSING PIPELINE
# ==============================================================================

def dither_serpentine(image_np):
    h, w = image_np.shape
    out = np.zeros((h, w), dtype=np.uint8)
    err = image_np.copy().astype(float)
    
    for y in range(h):
        if y % 2 == 0:
            x_range = range(w)
        else:
            x_range = range(w - 1, -1, -1)
            
        for x in x_range:
            old_val = err[y, x]
            new_val = 255 if old_val > 127 else 0
            out[y, x] = new_val
            diff = old_val - new_val
            
            direction = 1 if y % 2 == 0 else -1
            
            # neighbor 1: right
            nx, ny = x + direction, y
            if 0 <= nx < w and 0 <= ny < h:
                err[ny, nx] += diff * 7 / 16
            # neighbor 2: bottom-left
            nx, ny = x - direction, y + 1
            if 0 <= nx < w and 0 <= ny < h:
                err[ny, nx] += diff * 3 / 16
            # neighbor 3: bottom
            nx, ny = x, y + 1
            if 0 <= nx < w and 0 <= ny < h:
                err[ny, nx] += diff * 5 / 16
            # neighbor 4: bottom-right
            nx, ny = x + direction, y + 1
            if 0 <= nx < w and 0 <= ny < h:
                err[ny, nx] += diff * 1 / 16
                
    return out

def get_dithered_dots(img_path):
    print(f"Loading and preprocessing {img_path}...")
    img = Image.open(img_path)
    w, h = img.size
    
    # Resize and crop to 300x340 (head and shoulders)
    new_w = 300
    new_h = int(h * (new_w / w))
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img_cropped = img_resized.crop((0, 40, 300, 380))
    
    # Preprocess
    gray = ImageOps.grayscale(img_cropped)
    gray_ac = ImageOps.autocontrast(gray, cutoff=1)
    gray_filter = gray_ac.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    # Contrast 1.3x
    np_img = np.array(gray_filter, dtype=float)
    mean = np.mean(np_img)
    np_img = (np_img - mean) * 1.3 + mean
    np_img = np.clip(np_img, 0, 255)
    img_prep = Image.fromarray(np_img.astype(np.uint8))
    
    # Background Segmentation for Dark Mode
    pixels = np.array(img_cropped, dtype=float)
    h_c, w_c, c_c = pixels.shape
    patch_tl = pixels[0:15, 0:15]
    patch_tr = pixels[0:15, w_c-15:w_c]
    bg_color_tl = np.mean(patch_tl, axis=(0,1))
    bg_color_tr = np.mean(patch_tr, axis=(0,1))
    
    dist_tl = np.linalg.norm(pixels - bg_color_tl, axis=2)
    dist_tr = np.linalg.norm(pixels - bg_color_tr, axis=2)
    
    thresh = 60.0
    bg_mask = (dist_tl < thresh) | (dist_tr < thresh)
    fg_mask = ~bg_mask
    
    struct = np.ones((3, 3), dtype=bool)
    fg_closed = ndimage.binary_closing(fg_mask, structure=struct, iterations=3)
    fg_filled = ndimage.binary_fill_holes(fg_closed)
    
    labeled_array, num_features = ndimage.label(fg_filled)
    if num_features > 0:
        component_sizes = ndimage.sum(fg_filled, labeled_array, range(1, num_features + 1))
        largest_component_label = np.argmax(component_sizes) + 1
        fg_largest = (labeled_array == largest_component_label)
    else:
        fg_largest = fg_filled
        
    # Generate Dark dots
    np_dark = np.array(img_prep, dtype=float)
    np_dark[~fg_largest] = 0.0
    dithered_dark = dither_serpentine(np_dark)
    dark_dots = [(x, y) for y in range(340) for x in range(300) if dithered_dark[y, x] == 255]
    
    # Generate Light dots (entire image dithered, dots are dark parts, value=0)
    dithered_light = dither_serpentine(np.array(img_prep, dtype=float))
    light_dots = [(x, y) for y in range(340) for x in range(300) if dithered_light[y, x] == 0]
    
    print(f"Generated {len(dark_dots)} dark dots and {len(light_dots)} light dots.")
    return dark_dots, light_dots

# ==============================================================================
# 2. SVG GENERATION AND PARSING
# ==============================================================================

def parse_svg_paths(svg_content, is_dark):
    # Find all path elements in the first group (intro and drift)
    fill_color = "#A78BFA" if is_dark else "#7C3AED"
    start_tag = f'<g transform="translate(50,86) scale(1.2400,1.4471)" fill="{fill_color}" shape-rendering="crispEdges">'
    start_idx = svg_content.find(start_tag)
    end_idx = svg_content.find('<g transform="translate(50,86) scale(1.2400,1.4471)">')
    group1_content = svg_content[start_idx:end_idx]
    
    # Find subgroups
    groups_matches = re.finditer(r'(<g opacity="(?:0|1)">.*?)(?=</g>\s*(?:<g opacity=|</g>\s*$))', group1_content, re.DOTALL)
    
    subgroups = []
    for m in groups_matches:
        g_text = m.group(1) + "</g>"
        # Parse the paths inside the subgroup
        paths_data = re.findall(r'd="([^"]+)"', g_text)
        dots = []
        for p in paths_data:
            # Parse individual dot runs
            sub_runs = re.findall(r'M(\d+)\s+(\d+)(?:h(\d+))?', p)
            for run in sub_runs:
                x_start = int(run[0])
                y = int(run[1])
                width = int(run[2]) if run[2] != '' else 1
                for dx in range(width):
                    dots.append((x_start + dx, y))
        
        # Check if this group is intro (opacity=0) or drift (opacity=1)
        is_intro = 'opacity="0"' in g_text
        
        # If it is drift, find its translation dx, dy
        dx, dy = 0.0, 0.0
        if not is_intro:
            anim_trans = re.search(r'<animateTransform[^>]*values="[^;]+;[^;]+;([^;]+);', g_text)
            if anim_trans:
                val = anim_trans.group(1).strip()
                dx, dy = map(float, val.split())
                
        subgroups.append({
            'text': g_text,
            'is_intro': is_intro,
            'original_dots': dots,
            'mean_pos': np.mean(dots, axis=0) if len(dots) > 0 else np.array([150.0, 170.0]),
            'dx': dx,
            'dy': dy
        })
        
    return subgroups

def generate_path_data(dots):
    # Sort dots by y, then by x to make it clean
    dots = sorted(dots, key=lambda d: (d[1], d[0]))
    
    # Merge consecutive dots on the same row into a single path run "hW"
    runs = []
    if not dots:
        return ""
        
    current_run = None
    for d in dots:
        x, y = d
        if current_run is None:
            current_run = [x, y, 1]
        elif current_run[1] == y and current_run[0] + current_run[2] == x:
            current_run[2] += 1
        else:
            runs.append(current_run)
            current_run = [x, y, 1]
    if current_run:
        runs.append(current_run)
        
    # Format into path string
    path_strs = []
    for r in runs:
        x, y, w = r
        if w == 1:
            path_strs.append(f"M{x} {y}h1v1h-1z")
        else:
            path_strs.append(f"M{x} {y}h{w}v1h-{w}z")
            
    return "".join(path_strs)

def process_template_svg(template_path, new_dots, output_path, is_dark):
    print(f"Processing template {template_path} -> {output_path}...")
    with open(template_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        
    subgroups = parse_svg_paths(svg_content, is_dark)
    intro_groups = [g for g in subgroups if g['is_intro']]
    drift_groups = [g for g in subgroups if not g['is_intro']]
    
    print(f"Template has {len(intro_groups)} intro groups and {len(drift_groups)} drift groups.")
    
    # 1. Distribute new dots into intro groups randomly
    new_dots_shuffled = new_dots.copy()
    random.seed(42) # deterministic distribution
    random.shuffle(new_dots_shuffled)
    
    intro_dot_bins = [[] for _ in range(len(intro_groups))]
    for idx, dot in enumerate(new_dots_shuffled):
        bin_idx = idx % len(intro_groups)
        intro_dot_bins[bin_idx].append(dot)
        
    # 2. Distribute new dots into drift groups spatially
    drift_dot_bins = [[] for _ in range(len(drift_groups))]
    drift_means = np.array([g['mean_pos'] for g in drift_groups]) # shape (94, 2)
    
    for dot in new_dots:
        # Find closest drift group based on mean position
        dot_pos = np.array(dot)
        dists = np.linalg.norm(drift_means - dot_pos, axis=1)
        best_group_idx = np.argmin(dists)
        drift_dot_bins[best_group_idx].append(dot)
        
    # 3. Replace the subgroup path data in-place inside the svg_content
    svg_content_new = svg_content
    
    # Replace Intro subgroups
    for idx, g in enumerate(intro_groups):
        new_path = generate_path_data(intro_dot_bins[idx])
        g_text_new = re.sub(r'<path d="[^"]+"', f'<path d="{new_path}"', g['text'])
        svg_content_new = svg_content_new.replace(g['text'], g_text_new)
        
    # Replace Drift subgroups
    for idx, g in enumerate(drift_groups):
        new_path = generate_path_data(drift_dot_bins[idx])
        g_text_new = re.sub(r'<path d="[^"]+"', f'<path d="{new_path}"', g['text'])
        svg_content_new = svg_content_new.replace(g['text'], g_text_new)
    
    # 4. Process travelers in Group 157
    # For each traveler <use href="#tvdark" opacity="0"><animate .../><animateTransform ... values="x0 y0; x0 y0; ..."/></use>
    # We want to match traveler starting coordinate x0 y0 to a unique dot in new_dots
    # We will match them to the closest unused dots from new_dots
    travelers_start_idx = svg_content_new.find('<g transform="translate(50,86) scale(1.2400,1.4471)">')
    travelers_end_idx = svg_content_new.find('</g>', travelers_start_idx)
    travelers_content = svg_content_new[travelers_start_idx:travelers_end_idx]
    
    # Find all use elements
    use_elements = re.findall(r'<use[^>]+>.*?</use>', travelers_content, re.DOTALL)
    print(f"Found {len(use_elements)} travelers in Group 157.")
    
    # Greedy matching of travelers to new dots
    matched_dots = set()
    new_use_elements = []
    
    # Pre-build a KDTree or just simple grid matching for speed
    # Since new_dots has ~17,000 items and travelers is ~900, simple nearest-neighbor with a set is fast enough in Python
    new_dots_arr = np.array(new_dots)
    
    for use_el in use_elements:
        # Extract the original x0 y0 from values="..." inside animateTransform specifically
        val_match = re.search(r'<animateTransform[^>]+values="([^"]+)"', use_el)
        if val_match:
            vals_str = val_match.group(1)
            vals = vals_str.split(';')
            # First value is "x0 y0"
            x0_orig, y0_orig = map(float, vals[0].strip().split())
            
            # Find the closest unmatched dot from new_dots
            orig_pos = np.array([x0_orig, y0_orig])
            dists = np.linalg.norm(new_dots_arr - orig_pos, axis=1)
            # Sort indices by distance
            sorted_indices = np.argsort(dists)
            best_dot = None
            for idx in sorted_indices:
                dot_tuple = tuple(new_dots[idx])
                if dot_tuple not in matched_dots:
                    best_dot = dot_tuple
                    matched_dots.add(dot_tuple)
                    break
            
            if best_dot is None:
                # Fallback to absolute closest if all matched
                best_dot = tuple(new_dots[sorted_indices[0]])
                
            new_x0, new_y0 = best_dot
            
            # Reconstruct the values attribute
            vals[0] = f"{new_x0} {new_y0}"
            vals[1] = f"{new_x0} {new_y0}"
            vals[-1] = f"{new_x0} {new_y0}"
            
            new_vals_str = ";".join(vals)
            
            # Find animateTransform tag to replace values only inside it
            anim_trans_match = re.search(r'<animateTransform[^>]+>', use_el)
            if anim_trans_match:
                anim_trans_tag = anim_trans_match.group(0)
                new_anim_trans_tag = re.sub(r'values="[^"]+"', f'values="{new_vals_str}"', anim_trans_tag)
                new_use_el = use_el.replace(anim_trans_tag, new_anim_trans_tag)
            else:
                new_use_el = use_el
            
            # If light mode, make sure use href is '#tvlight'
            if not is_dark:
                new_use_el = new_use_el.replace('href="#tvdark"', 'href="#tvlight"')
                
            new_use_elements.append(new_use_el)
        else:
            new_use_elements.append(use_el)
            
    new_travelers_content = '<g transform="translate(50,86) scale(1.2400,1.4471)">\n' + "\n".join(new_use_elements)
    svg_content_new = svg_content_new[:travelers_start_idx] + new_travelers_content + svg_content_new[travelers_end_idx:]
    
    # 5. Replace SYSTEM.INFO details panel texts
    # We will do regex-based search & replace for tspans
    def replace_tspan_row(label, value, svg_str):
        # We need to compute dotted leader dots
        num_dots = 78 - len(label) - len(value) - 1
        dots = "." * max(1, num_dots)
        
        # Regex to find label tspan, dots tspan, and value tspan
        # Example: <tspan fill="#22D3EE">Subject </tspan><tspan fill="rgba(148,163,184,0.35)">.*?</tspan><tspan fill="#F8FAFC" font-weight="600">.*?</tspan>
        pattern = re.compile(
            r'(<tspan[^>]*>' + re.escape(label) + r'\s*</tspan>\s*)'
            r'(<tspan[^>]*>)\.*(</tspan>\s*)'
            r'(<tspan[^>]*>).*?(</tspan>)',
            re.IGNORECASE
        )
        
        def subst(match):
            color_class = "fill=\"#F8FAFC\" font-weight=\"600\"" if is_dark else "fill=\"#0F172A\" font-weight=\"600\""
            # Keep original tag styling but replace content
            tspan_label = match.group(1)
            tspan_dots_open = match.group(2)
            tspan_dots_close = match.group(3)
            tspan_val_open = match.group(4)
            tspan_val_close = match.group(5)
            
            # Let's clean up val open fill color for light mode if needed
            if not is_dark:
                tspan_val_open = tspan_val_open.replace('#F8FAFC', '#0F172A')
                tspan_dots_open = tspan_dots_open.replace('#22D3EE', '#0891B2')
            
            return f"{tspan_label}{tspan_dots_open}{dots}{tspan_dots_close}{tspan_val_open} {value}{tspan_val_close}"
            
        new_svg, count = re.subn(pattern, subst, svg_str)
        if count == 0:
            print(f"WARNING: Could not replace row: {label}")
        return new_svg

    # Replace rows
    svg_content_new = replace_tspan_row("Subject", "Gourav Patidar", svg_content_new)
    svg_content_new = replace_tspan_row("Role", "Full-Stack Developer", svg_content_new)
    svg_content_new = replace_tspan_row("Origin", "Indore, India", svg_content_new)
    svg_content_new = replace_tspan_row("Education", "B.Tech in Computer Science", svg_content_new)
    svg_content_new = replace_tspan_row("Status", "Building + Learning + Shipping", svg_content_new)
    svg_content_new = replace_tspan_row("ToolChain", "VS Code, Git, React, NestJS, TypeScript, Docker", svg_content_new)
    svg_content_new = replace_tspan_row("Core.Lang", "TypeScript, JavaScript, Python, C++", svg_content_new)
    svg_content_new = replace_tspan_row("Core.Frontend", "React, HTML5, CSS3", svg_content_new)
    svg_content_new = replace_tspan_row("Core.Backend", "NestJS, Node.js", svg_content_new)
    svg_content_new = replace_tspan_row("Core.Database", "PostgreSQL, MongoDB", svg_content_new)
    svg_content_new = replace_tspan_row("Core.Infra", "Docker, AWS, Git", svg_content_new)
    
    svg_content_new = replace_tspan_row("Grid.Mail", "business.gouravpatel@gmail.com", svg_content_new)
    svg_content_new = replace_tspan_row("Grid.Portfolio", "coming soon", svg_content_new)
    svg_content_new = replace_tspan_row("Grid.LinkedIn", "gourav-patidar", svg_content_new)
    svg_content_new = replace_tspan_row("Grid.GitHub", "@GouravPatidar91", svg_content_new)
    
    # We replace Facebook with a placeholder or something else, or if the user doesn't use Facebook, let's replace Facebook with X/Twitter
    # Let's search if they have a Grid.Facebook and replace label and value
    # In arifhaxn_dark.svg, line 107 has Grid.Facebook
    svg_content_new = re.sub(
        r'<tspan fill="#22D3EE">Grid.Facebook </tspan><tspan fill="rgba\(148,163,184,0.35\)">\.*</tspan><tspan fill="[^"]+" font-weight="600">\s*@arifhaxnn</tspan>',
        f'<tspan fill="#22D3EE">Grid.Twitter </tspan><tspan fill="rgba(148,163,184,0.35)">{"." * 41}</tspan><tspan fill="{"#F8FAFC" if is_dark else "#0F172A"}" font-weight="600"> @gourav_patidar</tspan>',
        svg_content_new
    )
    
    # Replace email in title bar and other specific email mentions
    # e.g., arifhasan.connect@gmail.com -> gouravpatidar91@gmail.com
    svg_content_new = svg_content_new.replace("arifhasan.connect@gmail.com", "business.gouravpatel@gmail.com")
    
    # Replace username mentions in other links or titles if any
    svg_content_new = svg_content_new.replace("Arif Hasan", "Gourav Patidar")
    svg_content_new = svg_content_new.replace("arifhaxn", "GouravPatidar91")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content_new)
    print(f"Finished writing to {output_path}.")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    dark_dots, light_dots = get_dithered_dots("gourav.png")
    
    # Process dark mode SVG
    process_template_svg("arifhaxn_dark.svg", dark_dots, "dark.svg", is_dark=True)
    
    # Process light mode SVG
    process_template_svg("arifhaxn_light.svg", light_dots, "light.svg", is_dark=False)
    
    print("All SVGs processed successfully!")
