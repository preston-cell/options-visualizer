function GreeksDisplay({ results }) {
  if (!results) return null

  return (
    <div className="card">
      <h3>Option Price</h3>
      <h2>${results.price}</h2>
      <h3 style={{ marginTop: '1rem' }}>Greeks</h3>
      <div className="greeks-grid">
        {Object.entries(results.greeks).map(([key, value]) => (
          <div className="greek-item" key={key}>
            <div className="greek-label">{key.charAt(0).toUpperCase() + key.slice(1)}</div>
            <div className="greek-value">{value}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default GreeksDisplay
