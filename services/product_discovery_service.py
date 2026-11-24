from urllib.parse import urlparse


class ProductDiscoveryService:

    def __init__(self):

        self.product_signals = {

            "add to cart": 5,
            "buy now": 5,
            "wishlist": 3,
            "price": 3,
            "mrp": 3,
            "reviews": 2,
            "ratings": 2,
            "sizes": 2,
            "size": 2,
            "colors": 2,
            "color": 2,
            "quantity": 1,
            "shipping": 1
        }

        self.product_url_signals = [

            "/product/",
            "/products/",
            "/p/",
            "/item/",
            "/shop/",
            "/buy/"
        ]

    def calculate_score(self, page):

        score = 0

        text = page.get(
            "text",
            ""
        ).lower()

        for signal, weight in self.product_signals.items():

            if signal in text:

                score += weight

        url = page.get(
            "url",
            ""
        ).lower()

        for signal in self.product_url_signals:

            if signal in url:

                score += 4

        path = urlparse(url).path

        segments = [

            p
            for p in path.split("/")
            if p
        ]

        if len(segments) >= 2:

            score += 1

        return score

    def discover_products(
        self,
        pages,
        limit=5
    ):

        candidates = []

        for page in pages:

            score = self.calculate_score(page)

            if score >= 5:

                candidates.append({

                    "score": score,
                    **page
                })

        candidates.sort(

            key=lambda x: x["score"],
            reverse=True
        )

        return candidates[:limit]