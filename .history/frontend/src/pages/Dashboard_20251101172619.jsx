import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Card, Badge, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/GlassBootstrap.css';

function Dashboard() {
  const [entries, setEntries] = useState([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [activities, setActivities] = useState(null);
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/journal/entries', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setEntries(response.data);
    } catch (err) {
      console.error('Error fetching entries:', err);
    }
  };

  const fetchActivities = async (entryId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/api/journal/activities/${entryId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setActivities(response.data);
      setSelectedEntry(entryId);
    } catch (err) {
      console.error('Error fetching activities:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8000/api/journal/entries', 
        { content },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      setContent('');
      setSuccess('✨ Entry saved successfully!');
      setTimeout(() => setSuccess(''), 3000);
      fetchEntries();
    } catch (err) {
      setError('Failed to create entry');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const getSentimentColor = (sentiment) => {
    return {
      'positive': 'success',
      'negative': 'danger',
      'neutral': 'secondary'
    }[sentiment] || 'secondary';
  };

  const getSentimentEmoji = (sentiment) => {
    return {
      'positive': '😊',
      'negative': '😔',
      'neutral': '😐'
    }[sentiment] || '😐';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  };

  return (
    <div className="glass-dashboard">
      <div className="glass-background">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>

      <div className="glass-header">
        <Container>
          <Row className="align-items-center">
            <Col xs={6} md={8}>
              <div className="d-flex align-items-center">
                <span className="app-icon-small me-2">🧠</span>
                <h1 className="mb-0 text-white fs-4">MindCare</h1>
              </div>
            </Col>
            <Col xs={6} md={4} className="text-end">
              <span className="text-white me-2 d-none d-md-inline">👤 {username}</span>
              <Button variant="light" size="sm" onClick={handleLogout}>
                Logout
              </Button>
            </Col>
          </Row>
        </Container>
      </div>

      <Container className="py-4">
        <Row className="justify-content-center mb-4">
          <Col xs={12} lg={8}>
            <Card className="glass-card shadow-lg">
              <Card.Body className="p-4">
                <h2 className="text-white mb-2">✍️ How are you feeling?</h2>
                <p className="text-white-50 mb-4">Let AI understand your emotions</p>

                {error && <Alert variant="danger">{error}</Alert>}
                {success && <Alert variant="success">{success}</Alert>}

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Control
                      as="textarea"
                      rows={5}
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                      placeholder="Share your thoughts, feelings, and experiences..."
                      required
                      className="glass-input"
                    />
                  </Form.Group>
                  <Button 
                    variant="light" 
                    type="submit" 
                    disabled={loading}
                    className="w-100 fw-bold"
                  >
                    {loading ? 'Analyzing...' : '💾 Save Entry'}
                  </Button>
                </Form>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Row>
          <Col xs={12}>
            <h2 className="text-white mb-3">📖 Your Journal ({entries.length})</h2>
          </Col>
        </Row>

        {entries.length === 0 ? (
          <Row>
            <Col xs={12}>
              <Card className="glass-card text-center py-5">
                <Card.Body>
                  <div style={{fontSize: '4rem'}}>📝</div>
                  <h3 className="text-white">No entries yet</h3>
                  <p className="text-white-50">Start journaling to track your mental wellness</p>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        ) : (
          <Row className="g-3">
            {entries.map((entry) => (
              <Col xs={12} md={6} lg={4} key={entry.id}>
                <Card className="glass-card h-100">
                  <Card.Body>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <small className="text-white-50">
                        📅 {formatDate(entry.created_at)}
                      </small>
                      <Badge bg={getSentimentColor(entry.sentiment)}>
                        {getSentimentEmoji(entry.sentiment)} {entry.sentiment}
                      </Badge>
                    </div>

                    <Card.Text className="text-white">
                      {entry.content}
                    </Card.Text>

                    <div className="d-flex justify-content-between align-items-center mt-3 pt-3 border-top border-white-50">
                      <Badge bg="secondary">
                        💭 {entry.primary_emotion}
                      </Badge>
                      <strong className="text-white">
                        {(entry.sentiment_score * 100).toFixed(0)}%
                      </strong>
                    </div>

                    <Button 
                      variant="outline-light" 
                      size="sm" 
                      className="w-100 mt-3"
                      onClick={() => fetchActivities(entry.id)}
                    >
                      💡 Get Suggestions
                    </Button>

                    {selectedEntry === entry.id && activities && (
                      <div className="mt-3 pt-3 border-top border-white-50">
                        <h6 className="text-white">{activities.message}</h6>
                        {activities.recommendations.map((activity, idx) => (
                          <div key={idx} className="activity-item p-2 mb-2 rounded">
                            <div className="d-flex">
                              <span className="me-2" style={{fontSize: '1.5rem'}}>
                                {activity.icon}
                              </span>
                              <div>
                                <strong className="text-white d-block">
                                  {activity.activity}
                                </strong>
                                <small className="text-white-50">
                                  {activity.description}
                                </small>
                              </div>
                            </div>
                          </div>
                        ))}
                        <Alert variant="warning" className="mt-2 mb-0 small">
                          {activities.additional_tip}
                        </Alert>
                      </div>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Container>
    </div>
  );
}

export default Dashboard;
