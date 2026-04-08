// Import render function and screen object from React Testing Library
// render() is used to render a component in a fake test DOM
// screen is used to search elements inside the rendered component
import { render, screen } from '@testing-library/react';

// Import the App component that we want to test
import App from './App';

// Define a test case
// The first parameter is the test name (description)
// The second parameter is a function that runs the test
test('renders learn react link', () => {

  // Render the App component in a virtual DOM environment
  render(<App />);

  // Try to find text that matches "learn react" (case insensitive)
  // /learn react/i → regex (i means ignore case)
  const linkElement = screen.getByText(/learn react/i);

  // Check (expect) that this element exists in the document
  expect(linkElement).toBeInTheDocument();
});
