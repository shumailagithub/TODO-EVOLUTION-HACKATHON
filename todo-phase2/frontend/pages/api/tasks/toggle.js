// This file handles /api/tasks/[id]/toggle routes
export default async function handler(req, res) {
  const { id } = req.query;

  if (req.method !== 'PATCH') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  try {
    // Forward the request to the backend
    const backendResponse = await fetch(`http://localhost:8001/api/tasks/${id}/toggle`, {
      method: 'PATCH',
      headers: {
        'Authorization': req.headers.authorization || '',
        'Content-Type': 'application/json',
      },
    });

    const data = await backendResponse.json();

    res.status(backendResponse.status).json(data);
  } catch (error) {
    console.error('Error forwarding request to backend:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}