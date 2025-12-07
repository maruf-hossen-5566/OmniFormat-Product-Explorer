import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def extract_ratings(product):
    try:
        elem = product.select_one("[data-cy='reviews-ratings-slot']>span")
        rating = f"{elem.get_text(strip=True).split(' ')[0]} stars" if elem else "--"
        return rating
    except Exception as e:
        print("Extract rating error: ", e)


def extract_reviews_count(product):
    try:
        rating_elem = product.select_one("[data-cy='reviews-ratings-slot']")
        if rating_elem:
            elem = rating_elem.find_parent("span").find_next_sibling("span")
            reviews = f"{elem.get_text(strip=True)[1:-1]}" if elem else "--"
            return reviews
        return "--"
    except Exception as e:
        print("Extract rating error: ", e)


def extract_asin_and_title(product):
    try:
        asin_elem = product.select_one("[data-asin]")
        asin = asin_elem.attrs.get("data-asin") if asin_elem else "--"

        title_elem = product.select_one("[data-cy='title-recipe']")
        title = title_elem.get_text(strip=True) if title_elem else None
        return asin, title
    except Exception as error:
        print("Extract asin and title error: ", error)
        return "--", None


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
        print("Extract thumbnail error: ", e)


def extract_price(product):
    try:
        price_elem = product.select_one(
            "[data-cy='price-recipe'] .a-price .a-offscreen"
        )
        price = price_elem.get_text(strip=True) if price_elem else "--"
        return price
    except Exception as e:
        print("Extract price error: ", e)


def extract_link(product):
    try:
        elem = product.select_one("[data-cy='title-recipe'] a")
        link = (
            f"{os.getenv('BASE_URL')+elem.get('href')}"
            if elem and elem.get("href")
            else "--"
        )
        return link
    except Exception as e:
        print("Extract link error: ", e)


def parse_product(product):
    try:
        asin, title = extract_asin_and_title(product)
        thumbnail = extract_thumbnail(product)
        ratings = extract_ratings(product)
        price = extract_price(product)
        reviews_count = extract_reviews_count(product)
        link = extract_link(product)

        return {
            "asin": asin,
            "title": title,
            "thumbnail": thumbnail,
            "price": price,
            "ratings": ratings,
            "reviews_count": reviews_count,
            "link": link,
        }
    except:
        return None


def parser(html):
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select("div[data-asin]:not([data-asin=''])")

    parsed_data = []
    print("-" * 100)
    for product in products:
        try:
            parsed = parse_product(product)
            if parsed and all(parsed.values()):
                parsed_data.append(parsed)
        except Exception as error:
            print("Parse products error: ", error)

    return parsed_data
