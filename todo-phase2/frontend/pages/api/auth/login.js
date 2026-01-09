export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Forward the request to the backend
    const backendResponse = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
    });

    const data = await backendResponse.json();

    res.status(backendResponse.status).json(data);
  } catch (error) {
    console.error('Error forwarding request to backend:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}