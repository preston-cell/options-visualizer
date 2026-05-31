import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

function PayoffChart({ payoff }) {
  const svgRef = useRef(null)

  useEffect(() => {
    if (!payoff) return

    const width = 600
    const height = 400
    const margin = { top: 20, right: 20, bottom: 40, left: 60 }

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const x = d3.scaleLinear()
      .domain(d3.extent(payoff, d => d.stock_price))
      .range([margin.left, width - margin.right])

    const y = d3.scaleLinear()
      .domain(d3.extent(payoff, d => d.pnl))
      .range([height - margin.bottom, margin.top])

    svg.append('g')
      .attr('transform', `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(x))

    svg.append('g')
      .attr('transform', `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(y))

    svg.append('line')
        .attr('x1', margin.left)
        .attr('x2', width - margin.right)
        .attr('y1', y(0))
        .attr('y2', y(0))
        .attr('stroke', '#ccc')
        .attr('stroke-dasharray', '4,4')

    const line = d3.line()
      .x(d => x(d.stock_price))
      .y(d => y(d.pnl))

    svg.append('path')
      .datum(payoff)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 2)
      .attr('d', line)

  }, [payoff])

  return <svg ref={svgRef} width={600} height={400} />
}

export default PayoffChart
