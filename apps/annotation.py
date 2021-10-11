import streamlit as st
import spacy
from annotated_text import annotated_text

nlp = spacy.load('en_core_web_sm')
cur_line = 0
sentence_num = 0


def process_text(doc, selected_entities, anonymize=False):
    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append((token.text, "Person", "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append((token.text, "Location", "#fda"))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append((token.text, "Organization", "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    if anonymize:
        anonmized_tokens = []
        for token in tokens:
            if type(token) == tuple:
                anonmized_tokens.append(("X" * len(token[0]), token[1], token[2]))
            else:
                anonmized_tokens.append(token)
        return anonmized_tokens

    return tokens


def app():
    global sentence_num, cur_line
    selected_entities = st.sidebar.multiselect(
        "Select the entities you want to detect",
        options=["LOC", "PER", "ORG", "COMPANY", "EVENT"],
        default=["LOC", "PER", "ORG"],
    )

    text_input = st.text_area("Type a text to anonymize")

    uploaded_file = st.file_uploader("or Upload a file", type=["doc", "docx", "pdf", "txt"])
    if uploaded_file is not None:
        text_input = uploaded_file.getvalue()
        text_input = text_input.decode("utf-8")

    if len(text_input) > 0:
        split_text = text_input.split('\n')
        sentence_num = len(split_text)

        doc = nlp(text_input)
        tokens = process_text(doc, selected_entities)

        annotated_text(*tokens)

        st.markdown("---")
        tag_box = st.empty()
        tag_box.text_area("tagging: ", split_text[cur_line])

        if st.sidebar.button('Prev'):
            if cur_line > 0:
                cur_line = cur_line - 1
                tag_box.text_area("tagging: ", split_text[cur_line])
        if st.sidebar.button('Next'):
            if cur_line < sentence_num - 1:
                cur_line = cur_line + 1
                tag_box.text_area("tagging: ", split_text[cur_line])
