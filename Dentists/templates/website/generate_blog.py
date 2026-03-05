#!/usr/bin/env python3
"""Generate blog pages for all 20 templates, matching each template's design.

Reads template-1's blog files as source content, then for each template N:
  1. Extracts design elements (fonts, CSS, nav, footer, primary color) from template_example-N.html
  2. Transforms the blog content to use template N's design
  3. Writes blog.html + 3 article files to template-N/
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

BLOG_FILES = [
    'blog.html',
    'blog/tipulim/hashtalat-shinayim-tel-aviv.html',
    'blog/briut-hapeh/tzviat-shinayim-nechona.html',
    'blog/sipurei-metuplim/hashtalat-shinayim-shinu-et-hayim-sheli.html',
]


# ── Color Utilities ──────────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def darken(h, factor=0.80):
    r, g, b = hex_to_rgb(h)
    return f'#{max(0,int(r*factor)):02x}{max(0,int(g*factor)):02x}{max(0,int(b*factor)):02x}'

def lighten(h):
    r, g, b = hex_to_rgb(h)
    r = min(255, r + int((255 - r) * 0.88))
    g = min(255, g + int((255 - g) * 0.88))
    b = min(255, b + int((255 - b) * 0.88))
    return f'#{r:02x}{g:02x}{b:02x}'

def luminance(h):
    """Relative luminance (0=black, 1=white)."""
    r, g, b = hex_to_rgb(h)
    def srgb(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


# ── Extraction Helpers ───────────────────────────────────────────────

def extract_font_css_link(html):
    """Extract Google Fonts CSS link (not preconnect)."""
    links = re.findall(r'<link[^>]*fonts\.googleapis\.com/css2[^>]*>', html)
    return links[0] if links else ''

def extract_font_preconnects(html):
    """Extract font preconnect links."""
    return re.findall(r'<link\s+rel="preconnect"[^>]*>', html)

def extract_style(html):
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

def extract_nav(html):
    m = re.search(r'(<nav\b[^>]*>.*?</nav>)', html, re.DOTALL)
    return m.group(1) if m else ''

def extract_footer(html):
    m = re.search(r'(<footer\b[^>]*>.*?</footer>)', html, re.DOTALL)
    return m.group(1) if m else ''

def is_dark_theme(css):
    """Detect if template uses a dark body background."""
    # Build variable map from :root
    root_match = re.search(r':root\s*\{([^}]+)\}', css)
    var_map = {}
    if root_match:
        for m in re.finditer(r'--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})', root_match.group(1)):
            var_map[m.group(1)] = m.group(2)

    # Find body background value
    body_match = re.search(r'body\s*\{[^}]*background\s*:\s*([^;\n]+)', css)
    if not body_match:
        return False

    bg_val = body_match.group(1).strip()

    # Resolve var() reference
    var_ref = re.match(r'var\(--([^)]+)\)', bg_val)
    if var_ref:
        var_name = var_ref.group(1)
        bg_color = var_map.get(var_name)
        if not bg_color:
            return False
    elif bg_val.startswith('#'):
        bg_color = bg_val
    else:
        return False

    return luminance(bg_color) < 0.05


def extract_primary_color(css):
    """Find the primary accent color from :root CSS variables."""
    root_match = re.search(r':root\s*\{([^}]+)\}', css)
    if not root_match:
        return '#2563EB', '#1d4ed8'

    root_content = root_match.group(1)
    colors = re.findall(r'--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})', root_content)

    # Skip non-accent colors
    skip = ['white', 'black', 'ink', 'gray', 'grey', 'slate', 'cream',
            'warm-white', 'sand', 'border', 'bg', 'text', 'muted', 'warm',
            'shadow', 'radius', 'max', 'col']
    light_suffixes = ['light', 'soft', 'mist', '50', '100']

    primary = None
    primary_dark = None

    for name, value in colors:
        nl = name.lower()

        if any(s in nl for s in skip):
            continue
        # Skip font/size variables that accidentally match
        if any(nl.startswith(p) for p in ['sans', 'serif', 'display', 'dm', 'syne',
                                           'radius', 'transition', 'max']):
            continue
        # Skip light/soft variations
        if any(nl.endswith(f'-{s}') or nl.endswith(s) for s in light_suffixes):
            continue

        if 'dark' in nl or 'deep' in nl:
            if primary and not primary_dark:
                primary_dark = value
        elif primary is None:
            primary = value

        if primary and primary_dark:
            break

    # Fallback: also check for 'gold' as accent for templates that use gold prominently
    if not primary:
        for name, value in colors:
            if 'gold' in name.lower() and 'light' not in name.lower():
                primary = value
                break

    if not primary:
        primary = '#2563EB'
    if not primary_dark:
        primary_dark = darken(primary)

    return primary, primary_dark


# ── Nav/Footer Modification ──────────────────────────────────────────

def modify_nav_for_blog(nav_html, n, is_article=False):
    """Adapt template nav for blog pages: fix hrefs, activate blog link."""
    prefix = '../../' if is_article else ''
    home = f'{prefix}template_example-{n}.html'
    blog = f'{prefix}blog.html'

    nav = nav_html

    # Replace href="#" (home + logo links) → home URL
    nav = re.sub(r'href="#"', f'href="{home}"', nav)

    # Replace href="#section" → home#section
    nav = re.sub(r'href="#(\w[\w-]*)"', rf'href="{home}#\1"', nav)

    # Replace blog.html → correct relative path
    nav = re.sub(r'href="blog\.html"', f'href="{blog}"', nav)

    # Add nav-active class to blog link
    # Match <a href="...blog.html">בלוג</a> or <a href="...blog.html" ...>בלוג</a>
    nav = nav.replace(f'href="{blog}">בלוג', f'href="{blog}" class="nav-active">בלוג')

    return nav


def modify_footer_for_blog(footer_html, n, is_article=False):
    """Adapt template footer for blog pages: fix hrefs."""
    prefix = '../../' if is_article else ''
    home = f'{prefix}template_example-{n}.html'
    blog = f'{prefix}blog.html'

    ft = footer_html
    ft = re.sub(r'href="#"', f'href="{home}"', ft)
    ft = re.sub(r'href="#(\w[\w-]*)"', rf'href="{home}#\1"', ft)
    ft = re.sub(r'href="blog\.html"', f'href="{blog}"', ft)
    return ft


# ── CSS Processing ───────────────────────────────────────────────────

def strip_root_and_body(css):
    """Remove :root{} and body{} from blog CSS (template CSS provides these)."""
    # Remove :root block (greedy within braces)
    css = re.sub(r':root\s*\{[^}]+\}', '', css, count=1)
    # Remove body block (first occurrence, not inside @media)
    css = re.sub(r'\nbody\s*\{[^}]+\}', '', css, count=1)
    # Also handle body at very start
    css = re.sub(r'^body\s*\{[^}]+\}', '', css, count=1)
    return css.strip()


def build_color_override(primary, primary_dark, dark=False):
    """Create CSS :root override that maps --blue to the template's primary color."""
    primary_light = lighten(primary)
    r, g, b = hex_to_rgb(primary)
    css = f"""
/* ── Blog-Template Color Mapping ── */
:root{{
  --blue:{primary};
  --blue-dark:{primary_dark};
  --blue-deeper:{primary_dark};
  --blue-light:{primary_light};
  --blue-mist:{primary_light};
  --blue-soft:{primary_light};
  --shadow-glow:0 4px 20px rgba({r},{g},{b},.25);
}}
"""
    if dark:
        css += f"""
/* ── Dark Theme Overrides ── */
:root{{
  --white:#111118;
  --ink:#f0f0f4;
  --ink-soft:#d0d0d8;
  --gray:#a0a0b0;
  --gray-light:#808090;
  --gray-border:rgba(255,255,255,.1);
  --slate-50:#161620;
  --slate-100:#1a1a26;
  --shadow-sm:0 2px 12px rgba(0,0,0,.2);
  --shadow-md:0 8px 32px rgba(0,0,0,.3);
  --shadow-lg:0 16px 48px rgba(0,0,0,.4);
}}
body{{background:#111118;color:#f0f0f4}}
.blog-card{{background:#1a1a26;border-color:rgba(255,255,255,.08)}}
.blog-card:hover{{box-shadow:0 8px 32px rgba(0,0,0,.4)}}
.category-bar{{background:#111118;border-color:rgba(255,255,255,.08)}}
.cat-pill{{background:#1a1a26;border-color:rgba(255,255,255,.1);color:#a0a0b0}}
.cat-pill:hover{{border-color:{primary};color:#f0f0f4}}
.blog-grid-section{{background:#111118}}
.blog-hero{{background:#161620}}
/* Article dark overrides */
.article-body h2,.article-body h3{{color:#f0f0f4}}
.article-body p,.article-body li{{color:#d0d0d8}}
.article-body strong{{color:#f0f0f4}}
.article-header{{background:#161620}}
.article-header .article-title{{color:#f0f0f4}}
.article-header .article-meta span{{color:#a0a0b0}}
.breadcrumb a{{color:#a0a0b0}}
.breadcrumb a:hover{{color:{primary}}}
.sidebar-card{{background:#1a1a26;border-color:rgba(255,255,255,.08)}}
.sidebar-card .sidebar-title{{color:#f0f0f4}}
.sidebar-related-title{{color:#d0d0d8}}
.sidebar-related-cat{{color:{primary}}}
.faq-toggle{{color:#f0f0f4;border-color:rgba(255,255,255,.08)}}
.faq-toggle[open] summary{{color:{primary}}}
.faq-toggle p{{color:#d0d0d8}}
.article-cta{{background:linear-gradient(135deg,{primary},{primary_dark})}}
.tip-box,.technique-box,.warning-box{{background:#1a1a26;border-color:rgba(255,255,255,.1)}}
.tip-box h4,.technique-box h4,.warning-box h4{{color:#f0f0f4}}
.tip-box p,.technique-box p,.warning-box p,.tip-box li,.technique-box li{{color:#d0d0d8}}
blockquote{{background:#1a1a26;border-color:{primary};color:#d0d0d8}}
"""
    return css


# ── Main Transform ───────────────────────────────────────────────────

def transform_blog_file(src_html, n, tpl_fonts, tpl_style, tpl_nav, tpl_footer,
                        primary, primary_dark, rel_path, dark=False):
    """Transform a template-1 blog file to match template-N's design."""
    is_article = rel_path != 'blog.html'
    html = src_html

    # 1. Replace Google Fonts CSS link
    src_font = extract_font_css_link(html)
    if src_font and tpl_fonts:
        html = html.replace(src_font, tpl_fonts)

    # 2. Replace style block
    #    Order: blog CSS (first, lower priority) → template CSS → color override
    blog_css = extract_style(html)
    blog_css_clean = strip_root_and_body(blog_css)
    color_override = build_color_override(primary, primary_dark, dark=dark)
    new_style = blog_css_clean + '\n\n' + tpl_style + '\n' + color_override
    html = re.sub(r'<style>.*?</style>', f'<style>\n{new_style}\n</style>', html, flags=re.DOTALL)

    # 3. Replace nav
    nav = modify_nav_for_blog(tpl_nav, n, is_article)
    html = re.sub(r'<nav\b[^>]*>.*?</nav>', lambda m: nav, html, count=1, flags=re.DOTALL)

    # 4. Replace footer
    footer = modify_footer_for_blog(tpl_footer, n, is_article)
    html = re.sub(r'<footer\b[^>]*>.*?</footer>', lambda m: footer, html, count=1, flags=re.DOTALL)

    # 5. Fix path references (template_example-1 → template_example-N)
    html = html.replace('template_example-1.html', f'template_example-{n}.html')

    # 6. Fix structured data references
    html = re.sub(r'"item"\s*:\s*"[^"]*template-1', f'"item":"template-{n}', html)

    return html


# ── Main Entry Point ─────────────────────────────────────────────────

def generate_blog():
    src_dir = os.path.join(BASE, 'template-1')

    # Read source blog files from template-1
    blog_sources = {}
    for rel_path in BLOG_FILES:
        full_path = os.path.join(src_dir, rel_path)
        if not os.path.exists(full_path):
            print(f'  ⚠ Source not found: {full_path}')
            continue
        with open(full_path, 'r', encoding='utf-8') as f:
            blog_sources[rel_path] = f.read()

    if not blog_sources:
        print('Error: No source blog files found in template-1/')
        return

    print(f'Loaded {len(blog_sources)} blog source files from template-1/')

    total = 0
    for n in range(1, 21):
        tpl_dir = os.path.join(BASE, f'template-{n}')
        example_path = os.path.join(tpl_dir, f'template_example-{n}.html')

        if not os.path.exists(example_path):
            print(f'  ⚠ template-{n}: example not found, skipping')
            continue

        with open(example_path, 'r', encoding='utf-8') as f:
            tpl_html = f.read()

        # Extract template design elements
        tpl_fonts = extract_font_css_link(tpl_html)
        tpl_style = extract_style(tpl_html)
        tpl_nav = extract_nav(tpl_html)
        tpl_footer = extract_footer(tpl_html)
        primary, primary_dark = extract_primary_color(tpl_style)
        dark = is_dark_theme(tpl_style)

        count = 0
        for rel_path, src_html in blog_sources.items():
            result = transform_blog_file(
                src_html, n, tpl_fonts, tpl_style, tpl_nav, tpl_footer,
                primary, primary_dark, rel_path, dark=dark
            )

            out_path = os.path.join(tpl_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(result)
            count += 1

        dark_label = ' [DARK]' if dark else ''
        print(f'  ✓ template-{n} ({primary}{dark_label}): {count} blog files')
        total += count

    print(f'\nDone! Generated {total} blog files across 20 templates.')


if __name__ == '__main__':
    generate_blog()
