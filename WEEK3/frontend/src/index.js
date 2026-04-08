import React from 'react';
import ReactDOM from 'react-dom/client'; // React 18+ way of managing the root
import './index.css'; // Global styles
import App from './App'; // Your main application component
import reportWebVitals from './reportWebVitals'; // Performance monitoring tool

// Finds the <div id="root"> from your index.html and creates the React Root
const root = ReactDOM.createRoot(document.getElementById('root'));

// Renders the App component inside StrictMode (which helps catch bugs during development)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

/* Initializes performance tracking. You can pass a console.log 
   or an analytics service to see how fast your app loads.
*/
reportWebVitals();
