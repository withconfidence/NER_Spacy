import os
import json
import streamlit as st
import streamlit.components.v1 as stc
from annotated_text import annotated_text
from annotator import custom_annotator
import pandas as pd
import docx2txt
from PyPDF2 import PdfFileReader
import pdfplumber
import spacy
nlp = spacy.load('en_core_web_sm')
_tag_list = ["PERSON", "ORG"]
cur_line = 0
sentence_num = 0


def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text


def read_pdf_with_pdfplumber(file):
	with pdfplumber.open(file) as pdf:
	    page = pdf.pages[0]
	    return page.extract_text()


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
    global _tag_list, cur_line, sentence_num
    is_show = False
    uploaded_file = st.sidebar.file_uploader("Upload File",type=['txt','docx','pdf'])
    if uploaded_file is None:
        return
    text_input = uploaded_file.getvalue()
    text_input = text_input.decode("utf-8")

    if len(text_input) > 0:
        split_text = text_input.split('\n')
        sentence_num = len(split_text)
    else:
        return

    state_value = []
    text_changed = True
    save_command = False

    doc = nlp(text_input)
    for token in doc:
        tag = str(token.ent_type_).upper()
        if tag != '' and tag not in _tag_list:
            _tag_list.append(tag)

    # add tag
    tag = st.sidebar.text_input('Add new TAG', '')
    if st.sidebar.button("ADD"):
        tag = str(tag).upper()
        if tag != '' and tag not in _tag_list:
            _tag_list.append(tag)
  
    selected_entities = st.multiselect(
        "Select the entities you want to detect",
        options=_tag_list,
        default=_tag_list,
    )

    tag_box = st.empty()
    tag_box.text_area("tagging: ", split_text[cur_line])

    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button('Prev'):
            if cur_line > 0:
                cur_line = cur_line - 1
                tag_box.text_area("tagging: ", split_text[cur_line])
                text_changed = True
    with col2:
        if st.button('Next'):
            if cur_line < sentence_num - 1:
                cur_line = cur_line + 1
                tag_box.text_area("tagging: ", split_text[cur_line])
                text_changed = True
    with col3:
        show_flag = st.checkbox('Show')
        is_show = show_flag
    with col4:
        if st.button('Submit'):
            save_command = True

    
    st.markdown("---")
    if text_changed:
        state_value = []
    else:
        pass

    state_value = custom_annotator(text_input, selected_entities, "annotator")

    st.markdown("---")
    if is_show:
        st.write(state_value)

    if save_command:
        json_data = {
            "classes": selected_entities,
            "annotations": []
        }
        
        one_item = [text_input]
        entity = []
        for it in state_value:
            entity.append([it['start'], it['end'], it['tag']])
        one_item.append({"entities": entity})
        json_data["annotations"].append(one_item)

        if os.path.isfile("./training_data.json"):
            os.remove("./training_data.json")
        with open("./training_data.json", "w") as jsp:
            jsp.write(json.dumps(json_data, indent=2))
        
        save_command = False
