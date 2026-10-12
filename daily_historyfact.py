from playwright.sync_api import sync_playwright

URL = "https://historyfacts.com/todays-fact/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    page.add_style_tag(content="""
        /* Hide cookie/privacy overlays and popups */
        #cmpwrapper,
        .cmpwrapper,
        .cmpbox,
        .cmpboxBG,
        .cmpboxrecall,
        .popup-modal,
        .gateway-drawer,
        .ft-post-like,
        .network-trending-posts,
        .related,
        .ft-bredscrumb,
        .shape-line-title,
        .toast-msg,
        [id*="subscribe-modal"],
        [id*="subscription-drawer"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* Hide ads and promo blocks from actual History Facts markup */
        .ft-post-advertisement-bg,
        .ad-img-wrap.ad-full,
        .crw-leaderboard-desktop-adblock,
        .crw-leaderboard-mobile-adblock,
        .is-floating-footer-adblock,
        .advertisement-label-style,
        .joinus-main,
        .related-posts,
        .article-loader,
        .ft-right-menu,
        .cate-list,
        .mega-menu,
        .footer-pages-menu,
        .footer-menu,
        .ArticleContent__vidContainer,
        .site-footer {
            display: none !important;
        }

        /* Remove header/nav clutter for PDF */
        #masthead,
        #site-navigation,
        .site-header,
        .header-wrap,
        .right-menu,
        .ft-expand-icon,
        .love-like,
        .wp-element-caption,
        .sticky-logo-wrap {
            display: none !important;
        }
        

        /* Expand article area */
        #page,
        #primary,
        .site-main,
        article.post,
        .ft-post-main,
        .post-container,
        .ft-post-wrap,
        .ft-post-conyent-wrap,
        .ft-post-conyent-left {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            float: none !important;
        }

        /* Keep body text readable */
        .ft-post-conyent-left p,
        .ft-post-conyent-left li,
        .ft-post-conyent-left h1,
        .ft-post-conyent-left h2,
        .ft-post-conyent-left h3,
        .author-info,
        .publish-date {
            max-width: 100% !important;
        }

        body {
            background: white !important;
        }

        .ft-post-conyent-left p {
            display: block !important;
            font-size: 11pt !important;
            line-height: 1.8 !important;
            margin-top: 0 !important;
            margin-bottom: 0.1in !important;
            break-inside: auto !important;
            page-break-inside: auto !important;
            orphans: 2 !important;
            widows: 2 !important;
        }

        .ft-post-conyent-left h2,
        .ft-post-conyent-left h3,
        .ft-post-conyent-left h4 {
            margin-top: 0.3in !important;
            margin-bottom: 0.15in !important;
            break-after: avoid !important;
            page-break-after: avoid !important;
        }

        .number-grid-list {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }

        .ft-post-conyent-left ul,
        .ft-post-conyent-left ol {
            margin-top: 0.08in !important;
            margin-bottom: 0.12in !important;
            padding-left: 0.22in !important;
        }

        /* Common wrappers that may add blank space */
        .ft-post-wrap,
        .ft-post-main,
        .post-container,
        .ft-post-conyent-wrap,
        .ArticleContentvidContainer,
        .ft-post-metadata-wrap {
            margin: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        .ft-post-conyent-left img,
        .ft-post-conyent-left figure,
        .ft-post-conyent-left .wp-block-image {
            display: block !important;
            break-before: page !important;
            page-break-before: always !important;
        }

        /* Keep the featured (cover) image on the first page with the title */
        .ft-post-conyent-left .single-featured-image,
        .ft-post-conyent-left .single-featured-image img {
            break-before: auto !important;
            page-break-before: auto !important;
        }

        /* Cover page: big centered title, tall image, author/date, then break */
        .ft-post-conyent-left h1.entry-title {
            text-align: center !important;
            font-size: 49px !important;
            line-height: 1.05 !important;
            margin: 0 0 24px 0 !important;
        }

        .ft-post-conyent-left .single-featured-image {
            margin: 0 !important;
        }

        .ft-post-conyent-left .single-featured-image img {
            width: 100% !important;
            max-width: 100% !important;
            height: 375px !important;
            object-fit: cover !important;
        }

        /* Image description overlaid on the bottom-right corner of the image */
        .ft-post-conyent-left .single-featured-image {
            position: relative !important;
        }

        .ft-post-conyent-left .single-featured-image figcaption {
            position: absolute !important;
            right: 0 !important;
            bottom: 0 !important;
            margin: 0 !important;
            padding: 3px 8px !important;
            background: rgba(255, 255, 255, 0.85) !important;
            color: #555 !important;
            font-style: normal !important;
            font-size: 10px !important;
            line-height: 1.3 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.15em !important;
        }

        .ft-post-conyent-left .author-info {
            margin-top: 48px !important;
            break-after: page !important;
            page-break-after: always !important;
        }
    """)

    # Wait for web fonts, otherwise the PDF can fall back to a wider font
    # (ads can keep the page from ever finishing loading, so don't fail on that)
    try:
        page.wait_for_load_state("load", timeout=15000)
    except Exception:
        pass
    page.evaluate("document.fonts.ready.then(() => true)")

    # Lay out at the printed content width so measurements match the PDF,
    # then shrink the cover image so title + image + author fit on page 1
    page.emulate_media(media="print")
    page.set_viewport_size({"width": 443, "height": 699})
    page.evaluate("""() => {
        const PAGE_H = 699;  // (8.28in - 0.4in - 0.6in) * 96px
        const img = document.querySelector('.ft-post-conyent-left .single-featured-image img');
        const author = document.querySelector('.ft-post-conyent-left .author-info');
        if (!img || !author) return;

        // Show the image description instead of the photo credit, in the
        // same font as the author name
        const caption = img.closest('figure').querySelector('figcaption');
        if (caption) {
            if (img.alt) {
                caption.textContent = img.alt;
                const name = document.querySelector('.author-info__name');
                if (name) caption.style.fontFamily = getComputedStyle(name).fontFamily;
            } else {
                caption.remove();
            }
        }

        const imgTop = img.getBoundingClientRect().top + window.scrollY;
        const below = author.getBoundingClientRect().bottom - img.getBoundingClientRect().bottom;
        const h = Math.max(200, Math.min(375, PAGE_H - imgTop - below - 10));
        img.style.setProperty('height', h + 'px', 'important');
    }""")

    page.pdf(
        path="daily_historyfact.pdf",
        width="6.21in",
        height="8.28in",
        print_background=True,
        margin={"top": "0.4in", "right": "0.8in",
                "bottom": "0.6in", "left": "0.8in"}
    )

    browser.close()
