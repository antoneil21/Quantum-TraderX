import React from 'react';

export default function SentimentGauge({ score }) {
  // Score range: 0 (Extreme Fear) to 100 (Extreme Greed)
  const getGaugeColor = (val) => {
    if (val < 25) return '#f85149'; // Red
    if (val < 50) return '#d29922'; // Orange
    if (val < 75) return '#e3b341'; // Yellow
    return '#3fb950';               // Green
  };

  return (
    <div style={{ background: '#161b22', padding: '20px', borderRadius: '8px', color: '#fff', textAlign: 'center' }}>
      <h3>Fear & Greed Index</h3>
      <div style={{ fontSize: '48px', fontWeight: 'bold', color: getGaugeColor(score) }}>
        {score} / 100
      </div>
      <p>{score >= 50 ? 'Greed Driven Market' : 'Fear Driven Market'}</p>
    </div>
  );
}
