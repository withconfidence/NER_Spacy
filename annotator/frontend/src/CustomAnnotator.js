import React, { useEffect, useState } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";
import {TextAnnotator} from 'react-text-annotate'

const MyAnnotator = (props) => {
  const { text, tags } = props.args;
  const [value, setValue] = useState([]);
  const [tag, setTag] = useState(tags[0]);
  const colors = [
    '#ff0000', '#ffa500', '#008000', '#ffa39e', '#d4380d', '#ffc069',
    '#d3f261', '#ff8c00', '#389e0d', '#5cdbd3', '#096dd9', '#adc6ff', 
    '#9254de', '#f759ab', '#ffa39e', '#d4380d', '#ffc069', '#ad8b00',
    '#d3f261']

  useEffect(() => Streamlit.setFrameHeight());

  return (
    <>
      <select onChange={(e)=> setTag(e.target.value)} value={tag}>
        {  tags.map((tag) => <option value={tag} key={tag}>{ tag }</option>)}
      </select>
      <TextAnnotator
        style={{
          maxWidth: 800,
          lineHeight: 2,
        }}
        content={ text }
        value={value}
        onChange={( value ) => {
          value && setValue(value);
          Streamlit.setComponentValue(value)
        }
        }
        getSpan={span => ({
          ...span,
          tag: tag,
          color: colors[tags.indexOf(tag)%19],
        })}
      />
    </>
  );
};

export default withStreamlitConnection(MyAnnotator);