import json
import os
import streamlit as st
import spacy
nlp = spacy.load('en_core_web_sm')
anal_data = {}


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
    st.title('Text annotation')
    option = st.selectbox(
        'How would you like to input text data?',
        ('File Browser', 'copy & paste'))

    global anal_data

    if option == 'File Browser':
        filename = file_selector()
        if os.path.basename(filename).lower().endswith(".txt"):
            st.write("- Reading text data ...")

            # load the training data
            with open(filename) as fp:
                text_data = ' '.join(fp.readlines())
        else:
            st.write("Invalid file format.")
            return
    else:
        text_data = st.text_input('Put your text here:')

    if st.button("click here to start"):
        st.write("- Annotating now ...")
        doc = get_doc(text_data)
        anal_data = get_tagging(doc)

        print_txt = []
        for ent in anal_data['token']:
            print_txt.append("{}[{}]".format(ent['text'], ent['tag']))
        st.write(" ".join(print_txt))

        st.write("- The Named Entity is ...")
        copy_text_data = text_data
        for ent in anal_data['entities']:
            copy_text_data = copy_text_data.replace(ent[0], "({})[{}]".format(ent[0], ent[3]))
        st.write(copy_text_data)

    if st.button("save to JSON"):
        json_data = {
            "classes": [x[3] for x in anal_data["entities"]],
            "annotations": []
        }
        one_item = [text_data.strip(), {"entities": [x[1], x[2], x[3]] for x in anal_data["entities"]}]
        json_data["annotations"].append(one_item)

        with open("training_data.json", "w") as jsp:
            jsp.write(json.dumps(json_data, indent=2))


"""
with open('../sample.txt') as fp:
    text_data = ' '.join(fp.readlines())

    st.write("- Annotating now ...")
    doc = get_doc(text_data)
    anal_data = get_tagging(doc)
    print(anal_data)
# """
