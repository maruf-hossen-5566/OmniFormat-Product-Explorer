import streamlit as st


def hero_section():
    st.title(
        ":red[OmniFormat] Product Explorer",
    )
    st.subheader(
        "Search once. View results as cards, tables, or JSON.",
    )

    st.markdown(
        """
        OmniFormat Product Explorer lets you enter any product keyword and instantly fetch structured product data.
        Choose your viewing format — card previews, tables, JSON, or structured text.
        """,
    )
    st.space()
