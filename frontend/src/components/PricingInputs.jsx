function PricingInputs({ inputs, onInputChange }) {
  return (
    <div>
      <div>
        <label>Stock Price: {inputs.stock_price}</label>
        <input
          type="range"
          min="10"
          max="500"
          value={inputs.stock_price}
          onChange={(e) => onInputChange('stock_price', Number(e.target.value))}
        />
      </div>

      <div>
        <label>Strike Price: {inputs.strike_price}</label>
        <input
          type="range"
          min="10"
          max="500"
          value={inputs.strike_price}
          onChange={(e) => onInputChange('strike_price', Number(e.target.value))}
        />
      </div>

      <div>
        <label>Days to Expiry: {inputs.time_to_expiry_days}</label>
        <input
          type="range"
          min="1"
          max="365"
          value={inputs.time_to_expiry_days}
          onChange={(e) => onInputChange('time_to_expiry_days', Number(e.target.value))}
        />
      </div>

      <div>
        <label>Volatility: {(inputs.volatility * 100).toFixed(0)}%</label>
        <input
          type="range"
          min="1"
          max="100"
          value={inputs.volatility * 100}
          onChange={(e) => onInputChange('volatility', Number(e.target.value) / 100)}
        />
      </div>

      <div>
        <label>Risk-free Rate: {(inputs.risk_free_rate * 100).toFixed(1)}%</label>
        <input
          type="range"
          min="0"
          max="15"
          step="0.1"
          value={inputs.risk_free_rate * 100}
          onChange={(e) => onInputChange('risk_free_rate', Number(e.target.value) / 100)}
        />
      </div>

      <div>
        <label>Option Type:</label>
        <select
          value={inputs.option_type}
          onChange={(e) => onInputChange('option_type', e.target.value)}
        >
          <option value="call">Call</option>
          <option value="put">Put</option>
        </select>
      </div>
    </div>
  )
}

export default PricingInputs
