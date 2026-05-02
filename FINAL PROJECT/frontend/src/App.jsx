import React, { useState } from 'react'; // Imports React and the useState hook for managing data
import axios from 'axios'; // Imports Axios to handle HTTP requests to the backend
import { Activity, Droplet, Weight, Calendar, Dna, AlertCircle, CheckCircle2 } from 'lucide-react'; // Imports beautiful icons

function App() {
  // State to store input values from the user form
  const [formData, setFormData] = useState({
    Glucose: '',
    BMI: '',
    Age: '',
    Pregnancies: '',
    DiabetesPedigreeFunction: ''
  });

  // States for handling the result from the API, loading animation, and error messages
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Updates the formData state whenever a user types in an input field
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Function called when the "Analyze" button is clicked
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the page from refreshing
    setLoading(true);   // Starts the loading spinner
    setError('');       // Resets any previous errors
    setResult(null);    // Clears previous results

    try {
      // Formats the data into numbers before sending it to the FastAPI backend
      const payload = {
        Glucose: parseFloat(formData.Glucose),
        BMI: parseFloat(formData.BMI),
        Age: parseFloat(formData.Age),
        Pregnancies: parseFloat(formData.Pregnancies),
        DiabetesPedigreeFunction: parseFloat(formData.DiabetesPedigreeFunction)
      };

      // Sends a POST request to the FastAPI server running on localhost:8000
      const response = await axios.post('http://localhost:8000/predict', payload);
      setResult(response.data); // Stores the prediction result (outcome and probability)
    } catch (err) {
      // Handles connection issues if the backend is not running
      setError('Failed to connect to the prediction server. Ensure the backend is running.');
    } finally {
      setLoading(false); // Stops the loading spinner
    }
  };

  return (
    // Main background with a gradient style
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center p-4 font-sans">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        
        {/* Header Section: Title and Subtitle */}
        <div className="bg-indigo-600 p-6 text-white text-center">
          <Activity className="w-12 h-12 mx-auto mb-3 text-indigo-200" />
          <h1 className="text-3xl font-bold tracking-tight">Diabetes Risk Assessment</h1>
          <p className="text-indigo-200 mt-2 text-sm">
            Powered by Machine Learning (SVM / Neural Networks)
          </p>
        </div>

        <div className="p-8">
          {/* The form for patient data entry */}
          <form onSubmit={handleSubmit} className="space-y-6">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Each Input Field (Glucose, BMI, Age, etc.) is handled here */}
              <div className="space-y-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Droplet className="w-4 h-4 mr-2 text-indigo-500" /> Glucose Level
                </label>
                <input required type="number" step="any" name="Glucose" value={formData.Glucose} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all"
                  placeholder="e.g. 120" />
              </div>
              {/* ... Other input fields follow the same pattern ... */}
            </div>

            {/* The Submit Button: Shows a spinner when loading */}
            <button type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg shadow-md disabled:opacity-70 flex justify-center items-center">
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                "Analyze Patient Data"
              )}
            </button>
          </form>

          {/* Results Section: Only shows if the 'result' state is not null */}
          {result && (
            <div className={`mt-6 p-6 rounded-xl border ${result.outcome === 1 ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  {/* Dynamic Icon: Red circle for High Risk, Green for Low Risk */}
                  {result.outcome === 1 ? (
                    <AlertCircle className="w-8 h-8 text-red-600" />
                  ) : (
                    <CheckCircle2 className="w-8 h-8 text-emerald-600" />
                  )}
                  <h3 className={`text-xl font-bold ${result.outcome === 1 ? 'text-red-800' : 'text-emerald-800'}`}>
                    {result.message}
                  </h3>
                </div>
              </div>
              
              {/* Probability Bar: Shows how confident the Machine Learning model is */}
              <div className="mt-4 pt-4 border-t border-slate-200 border-opacity-50">
                <p className="text-slate-600 text-sm font-medium mb-1">Model Confidence (Probability)</p>
                <div className="w-full bg-slate-200 rounded-full h-2.5 mb-1">
                  <div 
                    className={`h-2.5 rounded-full ${result.outcome === 1 ? 'bg-red-500' : 'bg-emerald-500'}`} 
                    style={{ width: `${(result.probability * 100).toFixed(1)}%` }}>
                  </div>
                </div>
                <p className="text-right text-xs font-bold text-slate-500">
                  {(result.probability * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
