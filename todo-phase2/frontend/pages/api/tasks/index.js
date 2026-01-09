export default async function handler(req, res) {
  try {
    let backendResponse;

    if (req.method === 'GET') {
      // Forward GET request to backend
      backendResponse = await fetch('http://localhost:8000/api/tasks', {
        method: 'GET',
        headers: {
          'Authorization': req.headers.authorization || '',
          'Content-Type': 'application/json'
        },
      });
    } else if (req.method === 'POST') {
      // Forward POST request to backend
      backendResponse = await fetch('http://localhost:8000/api/tasks', {
        method: 'POST',
        headers: {
          'Authorization': req.headers.authorization || '',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(req.body),
      });
    } else {
      return res.status(405).json({ message: 'Method not allowed' });
    }

    const data = await backendResponse.json();

    res.status(backendResponse.status).json(data);
  } catch (error) {
    console.error('Error forwarding request to backend:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}