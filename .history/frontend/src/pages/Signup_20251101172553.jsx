import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Alert, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/GlassBootstrap.css';

function Signup() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await axios.post('http://localhost:8000/api/auth/signup', formData);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-container">
      <div className="glass-background">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>

      <Container>
        <Row className="justify-content-center align-items-center min-vh-100">
          <Col xs={12} sm={10} md={8} lg={5}>
            <Card className="glass-card border-0 shadow-lg">
              <Card.Body className="p-4 p-sm-5">
                <div className="text-center mb-4">
                  <div style={{fontSize: '4rem'}} className="mb-3">🧠</div>
                  <h1 className="text-white fw-bold mb-2 fs-1">MindCare</h1>
                  <p className="text-white-50 mb-0">Your AI-Powered Wellness Journal</p>
                </div>

                <h2 className="text-white text-center mb-4 h5">Create Account</h2>

                {error && (
                  <Alert variant="danger" dismissible onClose={() => setError('')}>
                    {error}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label className="text-white fw-medium">Email</Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      placeholder="your.email@example.com"
                      className="glass-input"
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label className="text-white fw-medium">Username</Form.Label>
                    <Form.Control
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      placeholder="Choose a username"
                      className="glass-input"
                    />
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label className="text-white fw-medium">Password</Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      minLength="8"
                      placeholder="Min 8 characters"
                      className="glass-input"
                    />
                  </Form.Group>

                  <Button 
                    variant="light" 
                    type="submit" 
                    disabled={loading}
                    className="w-100 fw-bold py-2"
                  >
                    {loading ? 'Creating account...' : 'Sign Up'}
                  </Button>
                </Form>

                <p className="text-center text-white mt-4 mb-0">
                  Already have an account?{' '}
                  <Link to="/login" className="text-white fw-bold text-decoration-none">
                    Login
                  </Link>
                </p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Signup;
