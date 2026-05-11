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
    """)

    page.pdf(
        path="daily_historyfact.pdf",
        width="6.21in",
        height="8.28in",
        print_background=True,
        margin={"top": "0.4in", "right": "0.8in",
                "bottom": "0.6in", "left": "0.8in"}
    )

    browser.close()
