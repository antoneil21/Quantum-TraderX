import Redis from 'ioredis';

// Connect to the Redis State Manager caching layer
const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const snapshot = await redis.get('state:market_snapshot');
      const holdings = await redis.get('state:holdings');
      
      res.status(200).json({
        snapshot: snapshot ? JSON.parse(snapshot) : {},
        holdings: holdings ? JSON.parse(holdings) : []
      });
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch state from ultra-fast memory' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
