import { useState, useEffect } from 'react'
import PricingInputs from './components/PricingInputs'
import GreeksDisplay from './components/GreeksDisplay'
import PayoffChart from './components/PayoffChart'

function App() {
  const [inputs, setInputs] = useState({
    stock_price: 100,
    strike_price: 105,
    time_to_expiry_days: 30,
    volatility: 0.2,
    risk_free_rate: 0.05,
    option_type: 'call'
  })

  const [results, setResults] = useState(null)

  function handleInputChange(field, value) {
    setInputs({ ...inputs, [field]: value })
  }

  useEffect(() => {
    fetch('http://localhost:8000/price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputs)
    })
      .then(res => res.json())
      .then(data => setResults(data))
  }, [inputs])

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <h1>Options Visualizer</h1>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <div style={{ flex: '0 0 280px' }}>
          <PricingInputs inputs={inputs} onInputChange={handleInputChange} />
          <GreeksDisplay results={results} />
        </div>
        <div style={{ flex: 1 }}>
          <PayoffChart payoff={results?.payoff} />
        </div>
      </div>
    </div>
  )
}

export default App
