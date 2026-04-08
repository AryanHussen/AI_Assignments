// Function that takes a callback (like console.log) to report performance metrics
const reportWebVitals = onPerfEntry => {
  // Check if the callback exists and is a valid function
  if (onPerfEntry && onPerfEntry instanceof Function) {
    // Dynamically imports the web-vitals library only when needed to save initial load time
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);  // Layout Shift
      getFID(onPerfEntry);  // Input Delay
      getFCP(onPerfEntry);  // First Paint
      getLCP(onPerfEntry);  // Largest Paint
      getTTFB(onPerfEntry); // Server Response Time
    });
  }
};

export default reportWebVitals;
