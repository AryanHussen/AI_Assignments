import React, { useState } from 'react';
import axios from 'axios';
import { Activity, Droplet, Weight, Calendar, Dna, AlertCircle, CheckCircle2 } from 'lucide-react';

function App() {
  const [formData, setFormData] = useState({
    Glucose: '',
    BMI: '',
    Age: '',
    Pregnancies: '',
    DiabetesPedigreeFunction: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      // Convert string inputs to numbers for the backend
      const payload = {
        Glucose: parseFloat(formData.Glucose),
        BMI: parseFloat(formData.BMI),
        Age: parseFloat(formData.Age),
        Pregnancies: parseFloat(formData.Pregnancies),
        DiabetesPedigreeFunction: parseFloat(formData.DiabetesPedigreeFunction)
      };

      // Send POST request to FastAPI backend
      const response = await axios.post('http://localhost:8000/predict', payload);
      setResult(response.data);
    } catch (err) {
      setError('Failed to connect to the prediction server. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center p-4 font-sans">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        
        {/* Header Section */}
        <div className="bg-indigo-600 p-6 text-white text-center">
          <Activity className="w-12 h-12 mx-auto mb-3 text-indigo-200" />
          <h1 className="text-3xl font-bold tracking-tight">Diabetes Risk Assessment</h1>
          <p className="text-indigo-200 mt-2 text-sm">
            Powered by Machine Learning (SVM / Neural Networks)
          </p>
        </div>

        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Input Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <div className="space-y-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Droplet className="w-4 h-4 mr-2 text-indigo-500" /> Glucose Level
                </label>
                <input required type="number" step="any" name="Glucose" value={formData.Glucose} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                  placeholder="e.g. 120" />
              </div>

              <div className="space-y-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Weight className="w-4 h-4 mr-2 text-indigo-500" /> BMI
                </label>
                <input required type="number" step="any" name="BMI" value={formData.BMI} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                  placeholder="e.g. 25.5" />
              </div>

              <div className="space-y-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Calendar className="w-4 h-4 mr-2 text-indigo-500" /> Age
                </label>
                <input required type="number" step="any" name="Age" value={formData.Age} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                  placeholder="e.g. 45" />
              </div>

              <div className="space-y-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Activity className="w-4 h-4 mr-2 text-indigo-500" /> Pregnancies
                </label>
                <input required type="number" step="any" name="Pregnancies" value={formData.Pregnancies} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                  placeholder="e.g. 2" />
              </div>

              <div className="space-y-2 md:col-span-2">
                <label className="flex items-center text-sm font-medium text-slate-700">
                  <Dna className="w-4 h-4 mr-2 text-indigo-500" /> Diabetes Pedigree Function
                </label>
                <input required type="number" step="any" name="DiabetesPedigreeFunction" value={formData.DiabetesPedigreeFunction} onChange={handleChange}
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
                  placeholder="e.g. 0.52" />
              </div>

            </div>

            {/* Submit Button */}
            <button type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 shadow-md disabled:opacity-70 flex justify-center items-center">
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                "Analyze Patient Data"
              )}
            </button>
          </form>

          {/* Error State */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-start">
              <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0 mt-0.5" />
              <p className="text-sm">{error}</p>
            </div>
          )}

          {/* Results State */}
          {result && (
            <div className={`mt-6 p-6 rounded-xl border ${result.outcome === 1 ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
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
              
              <div className="mt-4 pt-4 border-t border-slate-200 border-opacity-50">
                <p className="text-slate-600 text-sm font-medium mb-1">Model Confidence (Probability)</p>
                <div className="w-full bg-slate-200 rounded-full h-2.5 mb-1 shadow-inner">
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