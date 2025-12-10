import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from logger import setup_logger

logger = setup_logger(__name__)

load_dotenv()


def extract_ratings(product):
    try:
        elem = product.select_one("[data-cy='reviews-ratings-slot']>span")
        rating = f"{elem.get_text(strip=True).split(' ')[0]} stars" if elem else "--"
        return rating
    except Exception as e:
        logger.exception("Failed at 'ratings' extraction.")
        raise e


def extract_reviews_count(product):
    try:
        rating_elem = product.select_one("[data-cy='reviews-ratings-slot']")
        if rating_elem:
            elem = rating_elem.find_parent("span").find_next_sibling("span")
            reviews = f"{elem.get_text(strip=True)[1:-1]}" if elem else "--"
            return reviews
        return "--"
    except Exception as e:
        logger.exception("Failed at 'reviews' extraction.")
        raise e


def extract_asin_and_title(product):
    try:
        asin = product.attrs.get("data-asin") if product and product.has_attr("data-asin") else "--"

        title_elem = product.select_one("[data-cy='title-recipe'] h2 span")
        title = title_elem.get_text(strip=True) if title_elem else None
        return asin, title
    except Exception as e:
        logger.exception("Failed at 'asin and title' extraction.")
        raise e


def extract_thumbnail(product):
    try:
        thumbnail_elem = product.select_one("img.s-image")
        thumbnail = (
            thumbnail_elem.get("src")
            if thumbnail_elem and thumbnail_elem.has_attr("src")
            else "--"
        )
        return thumbnail
    except Exception as e:
        logger.exception("Failed at 'thumbnail' extraction.")
        raise e


def extract_price(product):
    try:
        price_elem = product.select_one(
            "[data-cy='price-recipe'] .a-price .a-offscreen"
        )
        currency = price_elem.get_text(strip=True)[0] if price_elem else "--"
        price = price_elem.get_text(strip=True)[1:] if price_elem else "--"
        return currency, price
    except Exception as e:
        logger.exception("Failed at 'price' extraction.")
        raise e


def extract_link(product):
    try:
        elem = product.select_one("[data-cy='title-recipe'] a")
        link = (
            f"{os.getenv('BASE_URL') + elem.get('href')}"
            if elem and elem.get("href")
            else "--"
        )
        return link
    except Exception as e:
        logger.exception("Failed at 'link' extraction.")
        raise e


def parse_product(product):
    try:
        asin, title = extract_asin_and_title(product) or ["--", None]
        thumbnail = extract_thumbnail(product) or "--"
        ratings = extract_ratings(product) or "--"
        currency, price = extract_price(product) or ["--", "--"]
        reviews_count = extract_reviews_count(product) or "--"
        if asin and asin != "--":
            link = f"{os.getenv('BASE_URL')}/dp/{asin}"
        else:
            link = extract_link(product) or "--"

        return {
            "asin": asin,
            "title": title,
            "thumbnail": thumbnail,
            "currency": currency,
            "price": price,
            "ratings": ratings,
            "reviews_count": reviews_count,
            "link": link,
        }
    except Exception as e:
        raise e


def parser(html):
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select("[data-component-type='s-search-result']") or soup.select("[data-asin]:not([data-asin=''])")

    parsed_data = []
    for product in products:
        try:
            parsed = parse_product(product)
            if parsed and all(parsed.values()):
                parsed_data.append(parsed)

        except Exception as e:
            logger.exception("Failed at 'product' parsing.")
            raise e

    return parsed_data
