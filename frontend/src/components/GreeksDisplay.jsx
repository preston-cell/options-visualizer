function GreeksDisplay({ results }) {
  if (!results) return null

  return (
    <div>
      <h2>Option Price: ${results.price}</h2>
      <h3>Greeks</h3>
      <p>Delta: {results.greeks.delta}</p>
      <p>Gamma: {results.greeks.gamma}</p>
      <p>Theta: {results.greeks.theta}</p>
      <p>Vega: {results.greeks.vega}</p>
      <p>Rho: {results.greeks.rho}</p>
    </div>
  )
}

export default GreeksDisplay
