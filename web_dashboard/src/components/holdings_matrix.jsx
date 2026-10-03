import React from 'react';

export default function HoldingsMatrix({ holdings }) {
  return (
    <div className="holdings-matrix" style={{ background: '#161b22', color: '#fff', padding: '16px' }}>
      <h2>Real-Time Holdings Matrix</h2>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #30363d' }}>
            <th>Asset</th>
            <th>Market</th>
            <th>Allocation ($)</th>
            <th>Unrealized PnL</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #21262d' }}>
              <td>{item.asset}</td>
              <td>{item.market}</td>
              <td>${item.allocation.toLocaleString()}</td>
              <td style={{ color: item.pnl >= 0 ? '#3fb950' : '#f85149' }}>
                {item.pnl >= 0 ? `+${item.pnl}%` : `${item.pnl}%`}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
