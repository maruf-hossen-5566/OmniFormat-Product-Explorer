from dotenv import load_dotenv
import streamlit as st
import pandas as pd


def product_card(data):
    if data:
        with st.container(border=True):
            col1, col2 = st.columns([2, 4])
            if data.get("thumbnail") != "--":
                with col1:
                    st.image(data["thumbnail"], width=200, clamp=True)

            with col2:
                with st.container(horizontal=True):
                    asin = data.get("asin")
                    title = data.get("title")
                    price = data.get("price")
                    ratings = data.get("ratings")
                    reviews_count = data.get("reviews_count")
                    link = data.get("link")

                    st.markdown(f"**{title}**")
                    if asin:
                        st.markdown(f"**:red[ASIN]**: {asin}")
                    if price:
                        st.markdown(f"**:red[Price]**: {price}")
                with st.container(horizontal=True):
                    if ratings:
                        st.markdown(
                            f"""**:red[Ratings]**: {f'⭐{ratings}' if ratings != '--' else ratings}"""
                        )
                    if reviews_count:
                        st.markdown(f"**:red[Reviews count]**: {reviews_count}")
                if link:
                    st.markdown(f"**:red[Link]**: [{link[:50]}]({link})...")


def data_preview_tabs():
    return st.tabs(["Card", "JSON", "CSV", "STC"])


def tab_title():
    query = st.session_state.query
    st.markdown(f"### Showing results for :red[{query if query else '--Empty--'}]")
    st.space("stretch")


def json_preview_tab(query, data=[]):
    tab_title()
    if data:
        with st.container(border=True):
            st.json(data)


def card_preview_tab(query, data=[]):
    tab_title()
    if data:
        with st.container():
            for item in data:
                product_card(item)


def csv_preview_tab(query, data=[]):
    tab_title()
    df = pd.DataFrame(data)
    st.dataframe(df, placeholder="--")


def stc_preview_tab(query, data=[]):
    tab_title()
    if data:
        with st.container(border=True):
            st.space("stretch")
            for item in data:
                asin = item.get("asin")
                title = item.get("title")
                thumbnail = item.get("thumbnail")
                ratings = item.get("ratings")
                price = item.get("price")
                reviews_count = item.get("reviews_count")
                link = item.get("link")

                if asin:
                    st.markdown(f"""**:red[ASIN]**: {asin}""")
                if title:
                    st.markdown(f"""**:red[Title]**: {title}""")
                if thumbnail:
                    st.markdown(
                        f"""**:red[Thumbnail]**: [{thumbnail[:50]}]({thumbnail})..."""
                    )
                if ratings:
                    st.markdown(
                        f"""**:red[Ratings]**: {f'⭐{ratings}' if ratings != '--' else ratings}"""
                    )
                if price:
                    st.markdown(f"""**:red[Price]**: {price}""")
                if reviews_count:
                    st.markdown(f"""**:red[Reviews count]**: {reviews_count}""")
                if link:
                    st.markdown(f"""**:red[Link]**: [{link[:50]}...]({link})""")
                st.markdown("***")
