#!/usr/bin/env node
/**
 * Section Scanner — Extracts sections from all template HTML files
 * Outputs: tools/builder/sections-data.js
 *
 * Usage: node tools/section-scanner.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TEMPLATES_DIR = path.join(ROOT, 'templates');
const OUTPUT_FILE = path.join(__dirname, 'builder', 'sections-data.js');

// Verticals to scan
const VERTICALS = ['dentists', 'auto-repair', 'landscaping', 'hvac', 'med-spas', 'veterinarians'];

// Section type normalization map
const SECTION_TYPE_MAP = {
  // Hero
  'hero': 'hero', 'hero-bento': 'hero', 'hero-wrap': 'hero', 'chapter-hero': 'hero',
  'ch-hero': 'hero',
  // About
  'about': 'about', 'about-section': 'about', 'ch-about': 'about',
  'editorial-intro': 'about',
  // Services
  'services': 'services', 'features': 'services', 'specs': 'services',
  'ch-services': 'services',
  // Testimonials
  'testimonials': 'testimonials', 'reviews': 'testimonials',
  'testimonials-section': 'testimonials',
  // CTA / Contact
  'cta-section': 'cta', 'cta-banner': 'cta', 'contact': 'cta', 'cta-map': 'cta',
  'contact-cta': 'cta', 'cta': 'cta', 'cta-contact': 'cta',
  'mid-section': 'cta', 'specials': 'cta',
  'footer-cta': 'cta', 'cta-band': 'cta', 'ch-cta': 'cta',
  // Blog
  'blog': 'blog', 'blog-preview': 'blog',
  // Trust Bar
  'trust-bar': 'trust-bar', 'trust': 'trust-bar', 'certs': 'trust-bar',
  // Why Us
  'why-us': 'why-us', 'why': 'why-us',
  // Stats
  'stats': 'stats', 'stats-bar': 'stats', 'stats-section': 'stats',
  'chapter-stats': 'stats',
  // Gallery / Portfolio
  'gallery': 'gallery', 'gallery-section': 'gallery',
  'portfolio': 'gallery', 'ch-port': 'gallery', 'filmstrip': 'gallery',
  // Process
  'process': 'process', 'how-it-works': 'process',
  // Before/After
  'before-after': 'before-after', 'before-after-section': 'before-after',
  'beforeafter': 'before-after', 'ba': 'before-after', 'ch-ba': 'before-after',
  'results': 'before-after',
  // Team
  'team': 'team', 'doctors': 'team',
  // Service Area
  'service-area': 'service-area', 'area': 'service-area',
  // Other
  'faq': 'faq', 'pricing': 'pricing', 'brands': 'brands',
  'map': 'map', 'map-section': 'map',
  'hours': 'hours',
  'footer': 'footer', 'site-footer': 'footer',
  'nav': 'nav', 'navbar': 'nav',
};

function classifySection(tagName, className, id) {
  // Try class names first
  const classes = (className || '').split(/\s+/).filter(Boolean);
  for (const cls of classes) {
    const normalized = cls.toLowerCase().replace(/\s+/g, '-');
    if (SECTION_TYPE_MAP[normalized]) return SECTION_TYPE_MAP[normalized];
  }
  // Try id
  if (id) {
    const normalizedId = id.toLowerCase().replace(/\s+/g, '-');
    if (SECTION_TYPE_MAP[normalizedId]) return SECTION_TYPE_MAP[normalizedId];
  }
  // Tag-based fallback
  if (tagName === 'nav') return 'nav';
  if (tagName === 'footer') return 'footer';
  // Unknown
  return classes[0] || id || 'unknown';
}

function extractFontLinks(html) {
  const fontLinks = [];
  const linkRegex = /<link[^>]*href=["']([^"']*fonts[^"']*)["'][^>]*>/gi;
  let m;
  while ((m = linkRegex.exec(html)) !== null) {
    fontLinks.push(m[0]);
  }
  // Also get preconnect links for fonts
  const preconnectRegex = /<link[^>]*rel=["']preconnect["'][^>]*href=["'][^"']*font[^"']*["'][^>]*>/gi;
  while ((m = preconnectRegex.exec(html)) !== null) {
    if (!fontLinks.includes(m[0])) fontLinks.push(m[0]);
  }
  return fontLinks.join('\n');
}

function extractStyles(html) {
  const styles = [];
  const styleRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let m;
  while ((m = styleRegex.exec(html)) !== null) {
    styles.push(m[1]);
  }
  return styles.join('\n');
}

function extractSections(html) {
  const sections = [];
  // Match <section ...>...</section>, <nav ...>...</nav>, <footer ...>...</footer>
  // Handle nested tags by counting open/close
  const tagTypes = ['section', 'nav', 'footer'];

  for (const tag of tagTypes) {
    const openRegex = new RegExp(`<${tag}(\\s[^>]*)?>`, 'gi');
    let match;
    while ((match = openRegex.exec(html)) !== null) {
      const startIdx = match.index;
      const attrs = match[1] || '';

      // Extract class and id from attributes
      const classMatch = attrs.match(/class=["']([^"']*?)["']/i);
      const idMatch = attrs.match(/id=["']([^"']*?)["']/i);
      const className = classMatch ? classMatch[1] : '';
      const id = idMatch ? idMatch[1] : '';

      // Find the matching close tag (handle nesting)
      let depth = 1;
      let searchIdx = startIdx + match[0].length;
      const openPattern = new RegExp(`<${tag}(\\s|>)`, 'gi');
      const closePattern = new RegExp(`</${tag}>`, 'gi');

      let endIdx = -1;
      while (depth > 0 && searchIdx < html.length) {
        openPattern.lastIndex = searchIdx;
        closePattern.lastIndex = searchIdx;

        const nextOpen = openPattern.exec(html);
        const nextClose = closePattern.exec(html);

        if (!nextClose) break;

        if (nextOpen && nextOpen.index < nextClose.index) {
          depth++;
          searchIdx = nextOpen.index + nextOpen[0].length;
        } else {
          depth--;
          if (depth === 0) {
            endIdx = nextClose.index + nextClose[0].length;
          }
          searchIdx = nextClose.index + nextClose[0].length;
        }
      }

      if (endIdx === -1) continue;

      const sectionHtml = html.substring(startIdx, endIdx);
      const type = classifySection(tag, className, id);

      // Skip mobile menus, hidden elements
      if (className.includes('mobile-menu')) continue;

      sections.push({
        tag,
        className,
        id,
        type,
        html: sectionHtml,
      });
    }
  }

  return sections;
}

function getDirection(html) {
  const dirMatch = html.match(/dir=["'](rtl|ltr)["']/i);
  return dirMatch ? dirMatch[1] : 'ltr';
}

function getLang(html) {
  const langMatch = html.match(/lang=["']([^"']+)["']/i);
  return langMatch ? langMatch[1] : 'en';
}

function scanTemplates() {
  const allSections = [];
  let sectionId = 0;

  for (const vertical of VERTICALS) {
    const verticalDir = path.join(TEMPLATES_DIR, vertical, 'website');
    if (!fs.existsSync(verticalDir)) continue;

    const templateDirs = fs.readdirSync(verticalDir)
      .filter(d => d.startsWith('template-') && fs.statSync(path.join(verticalDir, d)).isDirectory())
      .sort((a, b) => {
        const na = parseInt(a.replace('template-', ''));
        const nb = parseInt(b.replace('template-', ''));
        return na - nb;
      });

    for (const templateDir of templateDirs) {
      const templateNum = parseInt(templateDir.replace('template-', ''));
      const dirPath = path.join(verticalDir, templateDir);

      // Find the main template HTML (prefer English for dentists)
      const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.html'));
      let mainFile = files.find(f => f.match(/template_example-\d+\.html$/));

      // For dentists, prefer English version for readability
      const enFile = files.find(f => f.match(/template_example-\d+-en\.html$/));
      if (vertical === 'dentists' && enFile) {
        mainFile = enFile;
      }

      if (!mainFile) continue;

      const filePath = path.join(dirPath, mainFile);
      const html = fs.readFileSync(filePath, 'utf8');
      // Relative path from project root to template directory (for <base href>)
      const templateRelDir = path.relative(ROOT, dirPath).replace(/\\/g, '/') + '/';

      const fontLinks = extractFontLinks(html);
      const styles = extractStyles(html);
      const direction = getDirection(html);
      const lang = getLang(html);
      const sections = extractSections(html);

      for (const section of sections) {
        sectionId++;
        allSections.push({
          id: `${vertical}-${templateNum}-${section.type}`,
          sectionId,
          vertical,
          template: templateNum,
          type: section.type,
          tag: section.tag,
          className: section.className,
          elementId: section.id,
          direction,
          lang,
          fontLinks,
          css: styles,
          html: section.html,
          basePath: templateRelDir,
          templateFile: templateRelDir + mainFile,
          rating: null,
        });
      }

      console.log(`  Scanned ${vertical}/template-${templateNum}: ${sections.length} sections`);
    }
  }

  return allSections;
}

// Main
console.log('Scanning templates...\n');
const sections = scanTemplates();

// Count by type
const typeCounts = {};
for (const s of sections) {
  typeCounts[s.type] = (typeCounts[s.type] || 0) + 1;
}

console.log(`\nTotal sections: ${sections.length}`);
console.log('By type:', JSON.stringify(typeCounts, null, 2));

// Write output
const output = `// Auto-generated by section-scanner.js — ${new Date().toISOString()}
// Total: ${sections.length} sections from ${VERTICALS.join(', ')}
const SECTIONS_DATA = ${JSON.stringify(sections, null, 2)};
`;

fs.writeFileSync(OUTPUT_FILE, output, 'utf8');
console.log(`\nWritten to ${OUTPUT_FILE}`);
console.log(`File size: ${(fs.statSync(OUTPUT_FILE).size / 1024 / 1024).toFixed(1)} MB`);
