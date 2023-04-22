import React from 'react';
import ReactDOM from 'react-dom';
import Page from './page';
import Search from './search';
import Create from './create';
import Graph from './graph'

// This method is only called once

const page = document.getElementById('react').getAttribute('data-page');

if (page === "Writing") {
  ReactDOM.render(
    <Search/>,
    document.getElementById('reactEntryWriting'),
  );
} else if (page === "Create") {
  ReactDOM.render(
    <Create/>,
    document.getElementById('reactEntryCreate'),
  );
} else if (page === "Graph") {
  ReactDOM.render(
    <Graph/>,
    document.getElementById('reactEntryGraph'),
  );
} else {
  ReactDOM.render(
    <Page/>,
    document.getElementById('reactEntryPost'),
  );
}