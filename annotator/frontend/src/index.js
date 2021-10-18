import React from "react";
import ReactDOM from "react-dom";
import MyAnnotator from "./CustomAnnotator";

// Wrap your MyAnnotator with the baseui light theme
ReactDOM.render(
  <React.StrictMode>
    <div>
        <MyAnnotator />
    </div>
  </React.StrictMode>,
  document.getElementById("root")
);
