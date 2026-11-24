from pathlib import Path
from urllib.parse import urlparse
import json

from playwright.sync_api import sync_playwright


class PlaywrightService:

    def __init__(self):

        self.screenshot_dir = Path(
            "data/screenshots"
        )

        self.page_dir = Path(
            "data/pages"
        )

        self.screenshot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.page_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ----------------------------------
    # Extract Internal Links
    # ----------------------------------

    def get_internal_links(
        self,
        page,
        base_url
    ):

        try:

            links = page.eval_on_selector_all(
                "a[href]",
                """
                elements =>
                elements.map(
                    e => e.href
                )
                """
            )

        except Exception:

            return []

        domain = (
            urlparse(base_url)
            .netloc
            .replace("www.", "")
        )

        results = []

        for link in links:

            try:

                parsed = urlparse(link)

                link_domain = (
                    parsed.netloc
                    .replace("www.", "")
                )

                if domain in link_domain:

                    results.append(
                        link
                    )

            except:
                pass

        return list(
            dict.fromkeys(
                results
            )
        )

    # ----------------------------------
    # Product Link Detection
    # ----------------------------------

    def get_product_links(
        self,
        links
    ):

        product_patterns = [

            "/product/",
            "/products/",
            "/p/",
            "/item/",
            "/buy/",
            "/shop/",

            "-p-"
        ]

        bad_patterns = [

            "legal",
            "privacy",
            "terms",
            "policy",
            "support",
            "help",
            "contact",
            "career",
            "press",
            "blog",
            "news",
            "faq"
        ]

        product_links = []

        for link in links:

            lower = link.lower()

            if any(
                bad in lower
                for bad in bad_patterns
            ):
                continue


            if any(
                pattern in lower
                for pattern in product_patterns
            ):

                product_links.append(
                    link
                )

        return list(
            dict.fromkeys(
                product_links
            )
        )

    # ----------------------------------
    # Save Page
    # ----------------------------------

    def save_page(
        self,
        page,
        index
    ):

        if index == 0:

            filename = "homepage.png"

        else:

            filename = (
                f"product_{index}.png"
        )

        screenshot_path = (
            self.screenshot_dir /
            filename
        )

        try:

            page.screenshot(
                path=str(
                    screenshot_path
                ),
                full_page=False
            )

        except:
            pass

        try:

            headings = page.locator(
                "h1,h2,h3"
            ).all_text_contents()

        except:

            headings = []

        try:

            page_text = (
                page.locator(
                    "body"
                ).inner_text()
            )

        except:

            page_text = ""

        try:

            images = page.eval_on_selector_all(
                "img",
                """
                elements =>
                elements
                .map(img => img.src)
                .slice(0,20)
                """
            )

        except:

            images = []

        page_data = {

            "url":
            page.url,

            "title":
            page.title(),

            "headings":
            headings,

            "text":
            page_text[:3000],

            "images":
            images,

            "screenshot":
            str(
                screenshot_path
            )
        }

        json_path = (
            self.page_dir /
            f"page_{index}.json"
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                page_data,
                f,
                indent=2,
                ensure_ascii=False
            )

        return page_data

    # ----------------------------------
    # Safe Navigation
    # ----------------------------------

    def safe_goto(
        self,
        page,
        url
    ):

        strategies = [

            "domcontentloaded",
            "commit"
        ]

        for strategy in strategies:

            try:

                page.goto(
                    url,
                    wait_until=strategy,
                    timeout=30000
                )

                page.wait_for_timeout(
                    3000
                )

                return True

            except Exception:

                continue

        return False

    # ----------------------------------
    # Main Crawl Function
    # ----------------------------------

    def capture_brand_pages(
        self,
        website_url,
        max_pages=3
    ):

        pages = []

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(

                user_agent=(
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0.0.0 "
                    "Safari/537.36"
                )

            )

            page = context.new_page()

            print(
                "\nLoading Homepage..."
            )

            success = self.safe_goto(
                page,
                website_url
            )

            if not success:

                browser.close()

                return []

            homepage = self.save_page(
                page,
                0
            )

            pages.append(
                homepage
            )

            internal_links = (
                self.get_internal_links(
                    page,
                    website_url
                )
            )

            product_links = (
                self.get_product_links(
                    internal_links
                )
            )

            product_links = list(
                dict.fromkeys(
                    product_links
                )
            )

            product_links = (
                product_links[:max_pages]
            )

            print(
                f"\nProduct Links Found: "
                f"{len(product_links)}"
            )

            for idx, link in enumerate(
                product_links,
                start=1
            ):

                try:

                    print(
                        f"\nVisiting:"
                    )

                    print(link)

                    success = (
                        self.safe_goto(
                            page,
                            link
                        )
                    )

                    if not success:

                        continue

                    page_data = (
                        self.save_page(
                            page,
                            idx
                        )
                    )

                    pages.append(
                        page_data
                    )

                except Exception as e:

                    print(
                        f"Failed: {link}"
                    )

                    print(e)

            browser.close()

        return pages