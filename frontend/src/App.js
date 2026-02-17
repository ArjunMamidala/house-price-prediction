import { useState } from "react";
import './App.css';

function App() {

  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);

  const [formData, setFormData] = useState({
    bed: "",
    bath: "",
    city: "",
    house_size: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const fetchHistory = () => {
    fetch('http://localhost:8000/history')
      .then(response => response.json())
      .then(data => setHistory(data.history))
      .catch(error => console.error('Error:', error));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        bed: parseInt(formData.bed),
        bath: parseInt(formData.bath),
        city: formData.city,
        house_size: parseInt(formData.house_size)
      }
      )
    })
    .then(response => response.json())
    .then(data => {
      setPrediction(data.prediction);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
  <div className="container">
    <h1>House Price Predictor</h1>
    <p className="subtitle">ML-powered property valuation across 17,000+ cities</p>
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Bedrooms</label>
        <input type="number" name="bed" value={formData.bed} onChange={handleChange} placeholder="e.g. 3" />
      </div>
      <div className="form-group">
        <label>Bathrooms</label>
        <input type="number" name="bath" value={formData.bath} onChange={handleChange} placeholder="e.g. 2" />
      </div>
      <div className="form-group">
        <label>City</label>
        <input type="text" name="city" value={formData.city} onChange={handleChange} placeholder="e.g. San Juan" />
      </div>
      <div className="form-group">
        <label>House Size (sqft)</label>
        <input type="number" name="house_size" value={formData.house_size} onChange={handleChange} placeholder="e.g. 1500" />
      </div>
      <button type="submit" className="submit-btn">Predict Price</button>
    </form>

    {prediction && (
      <div className="result-card">
        <p className="result-label">Estimated Price</p>
        <p className="result-price">${prediction.toLocaleString()}</p>
      </div>
    )}

    <button onClick={fetchHistory} className="submit-btn" style={{marginTop: '24px', background: '#1e1e2e'}}>
      View History
    </button>

    {history.length > 0 && (
      <div style={{marginTop: '24px'}}>
        {history.map(item => (
          <div key={item.id} className="result-card" style={{marginTop: '12px', textAlign: 'left'}}>
            <p style={{color: '#6b6b7b'}}>{item.bed} bed / {item.bath} bath / {item.city} / {item.house_size} sqft</p>
            <p className="result-price" style={{fontSize: '1.4rem'}}>${item.prediction.toLocaleString()}</p>
          </div>
        ))}
      </div>
    )}
    </div>
);
}

export default App;