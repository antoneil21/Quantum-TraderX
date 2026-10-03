import React, { useEffect, useState } from 'react';
import Backtester3D from '../components/3d_backtester';
import HoldingsMatrix from '../components/holdings_matrix';
import SentimentGauge from '../components/sentiment_gauge';

export default function QuantumDashboard() {
  const [marketData, setMarketData] = useState(null);

  useEffect(() => {
    // Poll the Next.js API route connecting to Redis
    const fetchData = async () => {
      const res = await fetch('/api/state');
      const data = await res.json();
      setMarketData(data);
    };
    
    const interval = setInterval(fetchData, 1000); // 1-second UI pulse
    return () => clearInterval(interval);
  }, []);

  // Placeholder data fallback
  const mockHoldings = [
    { asset: 'ETH', market: 'DeFi', allocation: 45000, pnl: 4.2 },
    { asset: 'NFL: KC vs LV', market: 'Sports', allocation: 10000, pnl: -1.5 }
  ];

  return (
    <div style={{ padding: '24px', background: '#010409', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ borderBottom: '1px solid #30363d', paddingBottom: '12px' }}>
        Quantum-TraderX Command Center
      </h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px', marginTop: '24px' }}>
        <div>
          <h2>Optimization Surface</h2>
          <Backtester3D />
        </div>
        <div>
          <SentimentGauge score={marketData?.sentimentScore || 65} />
        </div>
      </div>
      
      <div style={{ marginTop: '24px' }}>
        <HoldingsMatrix holdings={marketData?.holdings || mockHoldings} />
      </div>
    </div>
  );
}
