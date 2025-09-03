// testBackend.ts
import express from 'express';
import searchRoutes from '../routes/searchRoutes';

const app = express();
app.use(express.json());
app.use('/api', searchRoutes);

// Simple test endpoint
app.get('/test', (req, res) => {
  res.json({ message: 'Backend is running' });
});

app.listen(3002, () => {
  console.log('Test server running on port 3002');
});