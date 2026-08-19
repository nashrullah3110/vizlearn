"""The HTML frame shared by every generated page.

Module pages were hand-written and each carries its own copy of the header,
the theme toggle and the footer. The pages this build generates - topic
landings and the about/contact/privacy set - all come from here instead, so
they cannot drift from each other.

`build_seo.py` still owns everything inside <head> below the title; this only
produces the frame it writes into.
"""

import html

from lib_pages import GITHUB, KAGGLE, LINKEDIN

# The site's own icons, inlined (Font Awesome was removed from the project).
SEARCH_ICON = (
    '<svg class="vz-icon text-sm" viewBox="0 0 512 512" fill="currentColor" '
    'aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M416 208c0 45.9-14.9 '
    '88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 '
    '25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 '
    '144 0 1 0 0-288 144 144 0 1 0 0 288z"/></svg>'
)

BACK_ICON = (
    '<svg class="vz-icon text-xs" viewBox="0 0 448 512" fill="currentColor" aria-hidden="true" '
    'xmlns="http://www.w3.org/2000/svg"><path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 '
    '160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 '
    '32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 '
    '0l-160 160z"/></svg>'
)

SUN_ICON = (
    '<svg class="vz-icon hidden dark-icon" viewBox="0 0 512 512" fill="currentColor" '
    'aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M361.5 1.2c5 2.1 8.6 6.6 '
    '9.6 11.9L391 121l107.9 19.8c5.3 1 9.8 4.6 11.9 9.6s1.5 10.7-1.6 15.2L446.9 256l62.3 '
    '90.3c3.1 4.5 3.7 10.2 1.6 15.2s-6.6 8.6-11.9 9.6L391 391 371.1 498.9c-1 5.3-4.6 9.8-9.6 '
    '11.9s-10.7 1.5-15.2-1.6L256 446.9l-90.3 62.3c-4.5 3.1-10.2 3.7-15.2 1.6s-8.6-6.6-9.6-11.9L121 '
    '391 13.1 371.1c-5.3-1-9.8-4.6-11.9-9.6s-1.5-10.7 1.6-15.2L65.1 256 2.8 165.7c-3.1-4.5-3.7-10.2-1.6-15.2s6.6-8.6 '
    '11.9-9.6L121 121 140.9 13.1c1-5.3 4.6-9.8 9.6-11.9s10.7-1.5 15.2 1.6L256 65.1 346.3 2.8c4.5-3.1 '
    '10.2-3.7 15.2-1.6zM160 256a96 96 0 1 1 192 0 96 96 0 1 1 -192 0zm224 0a128 128 0 1 0 -256 0 '
    '128 128 0 1 0 256 0z"/></svg>'
)

MOON_ICON = (
    '<svg class="vz-icon hidden light-icon" viewBox="0 0 384 512" fill="currentColor" '
    'aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M223.5 32C100 32 0 132.3 0 '
    '256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 '
    '1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 '
    '7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"/></svg>'
)

GA_ID = "G-ZT6JM33V5J"


def head_top(title, prefix):
    """Everything above the generated SEO block.

    build_seo.py inserts its block immediately before the page's own <style>,
    so the frame has to open one even when it has no rules of its own.
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>%s</title>
    <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '%s');
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <script>
        (function(){
            const apply = (t)=>{
                if(t==='light') document.body.classList.add('light-mode');
                else document.body.classList.remove('light-mode');
            };
            const t = localStorage.getItem('theme') || 'light';
            if(document.body) apply(t); else document.addEventListener('DOMContentLoaded', ()=>apply(t));
        })();
    </script>
    <style>
        /* page-specific rules go here; the shared system is in vizlearn.css */
    </style>
</head>
""" % (html.escape(title), GA_ID, GA_ID)


def header(prefix, back_label="Home"):
    """Sticky header: logo, site search, back link, theme toggle."""
    return """<body class="flex flex-col min-h-screen light-mode">
<!-- Light is the default, so it ships on the tag: the theme script runs at the
     bottom of the body, and waiting for it would flash dark on every load.
     This removes the class before any content is parsed for readers who chose
     dark, so neither theme flashes the other. -->
<script>if(localStorage.getItem("theme")==="dark")document.body.classList.remove("light-mode");</script>

    <!-- Header -->
    <header class="glass-header sticky top-0 z-50">
        <div class="flex justify-center py-3 px-4 md:px-8">
            <div class="flex flex-col md:flex-row items-center justify-between w-full max-w-7xl gap-3 md:gap-4">
                <a href="%(p)sindex.html" class="text-2xl font-bold flex-shrink-0 tracking-tight flex items-center gap-3 select-none cursor-pointer no-underline" style="color: var(--text-main)">
                    <div class="w-3 h-3 rounded-full bg-green-400 shadow-[0_0_15px_rgba(74,222,128,0.8)] animate-pulse"></div>
                    <span>viz<span style="color: var(--text-muted); font-weight: 300;">learn</span></span>
                </a>

                <div class="search-input-wrapper rounded-full flex items-center w-full max-w-md px-4 py-2.5 mx-auto md:mx-0">
                    %(search)s
                    <input type="text" id="appSearchInput" aria-label="Search all articles" placeholder="Search all articles..." class="bg-transparent text-sm focus:outline-none ml-3 w-full font-sans tracking-wide">
                    <div id="searchDropdown" class="search-dropdown"></div>
                </div>

                <div class="flex items-center gap-3">
                    <a href="%(p)sindex.html" class="hidden md:flex items-center gap-2 text-sm font-medium mono-font hover:text-green-400 transition-colors px-3 py-2 rounded-full" style="color: var(--text-muted)" aria-label="Back to %(back)s">
                        %(backicon)s
                    </a>
                    <button id="themeToggle" class="w-10 h-10 rounded-full flex items-center justify-center focus:outline-none transition-colors flex-shrink-0" style="color: var(--text-muted)" aria-label="Toggle Dark/Light Mode">
                        %(sun)s
                        %(moon)s
                    </button>
                </div>
            </div>
        </div>
    </header>
""" % {"p": prefix, "search": SEARCH_ICON, "back": html.escape(back_label),
       "backicon": BACK_ICON, "sun": SUN_ICON, "moon": MOON_ICON}


THEME_SCRIPT = """
    <script>
        (function () {
            var btn = document.getElementById('themeToggle');
            if (!btn) return;
            var sun = btn.querySelector('.dark-icon');
            var moon = btn.querySelector('.light-icon');

            function paint(theme) {
                if (theme === 'light') {
                    document.body.classList.add('light-mode');
                    moon.classList.remove('hidden');
                    sun.classList.add('hidden');
                } else {
                    document.body.classList.remove('light-mode');
                    sun.classList.remove('hidden');
                    moon.classList.add('hidden');
                }
            }

            paint(localStorage.getItem('theme') || 'light');

            btn.addEventListener('click', function () {
                var next = document.body.classList.contains('light-mode') ? 'dark' : 'light';
                localStorage.setItem('theme', next);
                paint(next);
            });
        })();
    </script>
"""


def close(prefix):
    """Theme wiring and </body>. The shared scripts are appended by build_seo."""
    return THEME_SCRIPT + "\n</body>\n</html>\n"


def breadcrumb_bar(items):
    """Visible breadcrumb trail. `items` is [(label, href-or-None), ...]."""
    out = ['<nav class="flex flex-wrap items-center gap-2 text-sm mono-font mb-2" '
           'style="color: var(--text-muted)" aria-label="Breadcrumb">']
    for i, (label, href) in enumerate(items):
        if i:
            out.append('<span aria-hidden="true">/</span>')
        if href:
            out.append('<a href="%s" class="hover:text-green-400 transition-colors">%s</a>'
                       % (href, html.escape(label)))
        else:
            out.append('<span aria-current="page">%s</span>' % html.escape(label))
    out.append("</nav>")
    return "".join(out)
