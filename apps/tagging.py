import json
import os
import streamlit as st
import spacy
from annotated_text import annotated_text
nlp = spacy.load('en_core_web_sm')
json_data = None


def get_tagging(doc):
    result_list = {}
    if doc is None:
        print("Failed to initialize the text.")
        return result_list

    # token list
    result_list['token'] = []
    for token in doc:
        info = {
            'text': token.text,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'shape': token.shape_,
            'is_alpha': token.is_alpha,
            'is_stop': token.is_stop
        }
        result_list['token'].append(info)
        # print(json.dumps(info, indent=2))

    # exp list
    result_list['explain'] = []
    for ent in doc.ents:
        info = {
            'text': ent.text,
            'label_': ent.label_,
            'exp': spacy.explain(ent.label_)
        }
        result_list['explain'].append(info)

    # Setting entity annotations
    entities = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
    result_list['entities'] = entities

    return result_list


def get_doc(text):
    return nlp(text)


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Please choose text file for tagging', filenames)
    return os.path.join(folder_path, selected_filename)


def app():
    global json_data
    st.title('Text annotation')
    option = st.selectbox(
        'How would you like to input text data?',
        ('File Browser', 'copy & paste'))

    if option == 'File Browser':
        filename = file_selector()
        if os.path.basename(filename).lower().endswith(".txt"):
            st.write("- Reading text data ...")

            # load the training data
            with open(filename) as fp:
                text_list = fp.readlines()
                text_data = ' '.join([x.strip() for x in text_list])
        else:
            st.write("Invalid file format.")
            return
    else:
        text_data = st.text_area('Put your text here (at least 10 sentences):')
        text_list = text_data.split('\n')

    st.write(text_list)

    if st.button("click here to start"):
        doc = get_doc(text_data)

        tokens = []
        entities_list = ["LOC", "PER", "ORG", "NORP", "DATE"]
        for token in doc:
            if (token.ent_type_ == "PERSON") & ("PER" in entities_list):
                tokens.append((token.text, "Person", "#faa"))
            elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in entities_list):
                tokens.append((token.text, "Location", "#fda"))
            elif (token.ent_type_ == "ORG") & ("ORG" in entities_list):
                tokens.append((token.text, "Organization", "#afa"))
            elif (token.ent_type_ == "DATE") & ("DATE" in entities_list):
                tokens.append((token.text, "DATE", "#caa"))
            elif (token.ent_type_ == "NORP") & ("NORP" in entities_list):
                tokens.append((token.text, "NORP", "#aca"))
            else:
                tokens.append(" " + token.text + " ")
        annotated_text(*tokens)

        tag_data = get_tagging(doc)
        # text_length = [len(x) for x in text_list]
        # st.write("entities:")
        # st.write(["{} : {}".format(x[0], x[3])for x in tag_data["entities"]])

        json_data = {
            "classes": list(set([x[3] for x in tag_data["entities"]])),
            "annotations": []
        }
        _pass_length = 0
        for i, one_line in enumerate(text_list):
            one_item = [one_line.strip()]
            cur_length = len(one_line)
            entity = []
            for (word, start_char, end_char, _label) in tag_data["entities"]:
                if _pass_length <= start_char <= end_char <= _pass_length + cur_length:
                    entity.append([start_char, end_char, _label])
            if len(entity) > 0:
                one_item.append({"entities": entity})

                json_data["annotations"].append(one_item)

            _pass_length += cur_length

        # st.write("tagging json:")
        # st.write(json_data)

    st.markdown("---")
    if st.button("save to JSON"):
        if json_data is None:
            st.write("Invalid JSON data!")
            return
        if os.path.isfile("./training_data.json"):
            os.remove("./training_data.json")
        with open("./training_data.json", "w") as jsp:
            jsp.write(json.dumps(json_data, indent=2))

            st.write("Successfully saved. You can forward to training with 'training_data.json'.")
