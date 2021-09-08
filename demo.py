import streamlit as st
import os
import json
import spacy

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select training JSON data', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()

if os.path.basename(filename).endswith(".json"):
    st.write("- Reading train data ...")

    # load the training data
    with open(filename) as fp:
        training_data = json.load(fp)
    
    st.write(training_data)

    # prepare an empty model to train
    st.write("- Preparing an empty model with English language to train ...")
    nlp = spacy.blank('en')
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
        # ner = nlp.get_pipe('ner')
    else:
        ner = nlp.get_pipe('ner')
        
    nlp.vocab.vectors.name = 'demo'

    # add the custom NER tags as entities into the model
    st.write("- Adding tags into model ...")
    label_list = []
    for label in training_data["classes"]:
        label_list.append(label)
        # nlp.entity.add_label(label)
        ner.add_label(label)

    st.write("    label added: [{}]".format(', '.join(label_list)))
    
    # train the model
    iters = st.sidebar.number_input('Train iteration number', 5, format='%d')
    st.write("- Start training the model now ...")
    optimizer = nlp.begin_training()
    for iter in range(iters):
        losses = {}
        for text, annotations in training_data["annotations"]:
            if len(text) > 0:
                nlp.update([text], [annotations], sgd=optimizer, losses=losses)
        st.write("{}: {}".format(iter+1, losses))

    # Test
    st.write("- Test with sentence.")
    default_value_goes_here = "Linclon led the nation through the American Civil War, he succeeded in preserving the Union, abolishing slavery and modernizing the U.S. economy."
    test_sentence = st.text_input("Input your text", default_value_goes_here)

    st.write("- Result:")
    doc = nlp(test_sentence)
    for ent in doc.ents:
        st.write("{} : {}".format(ent.text, ent.label_))