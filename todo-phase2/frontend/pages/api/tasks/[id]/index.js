// This file handles /api/tasks/[id] routes using dynamic routing for DELETE and PUT
export default async function handler(req, res) {
  const { id } = req.query;

  if (!id) {
    return res.status(400).json({ message: 'Task ID is required' });
  }

  try {
    let backendResponse;

    if (req.method === 'DELETE') {
      // Forward DELETE request to backend
      backendResponse = await fetch(`http://localhost:8000/api/tasks/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': req.headers.authorization || '',
          'Content-Type': 'application/json',
        },
      });
    } else if (req.method === 'PUT') {
      // Forward PUT request to backend
      backendResponse = await fetch(`http://localhost:8000/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': req.headers.authorization || '',
          'Content-Type': 'application/json',
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