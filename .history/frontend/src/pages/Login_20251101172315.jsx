import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Alert, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/GlassBootstrap.css';

function Login() {
  const [formData, setFormData] = useState({
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
      const response = await axios.post('http://localhost:8000/api/auth/login', 
        new URLSearchParams({
          username: formData.username,
          password: formData.password
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('username', formData.username);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
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

      <Container fluid>
        <Row className="justify-content-center align-items-center min-vh-100 px-2">
          <Col xs={11} sm={10} md={8} lg={5} xl={4}>
            <Card className="glass-card border-0 shadow-lg">
              <Card.Body className="p-4 p-sm-5">
                <div className="text-center mb-4">
                  <div style={{fontSize: '4rem'}} className="mb-3">🧠</div>
                  <h1 className="text-white fw-bold mb-2 display-6">
                    MindCare
                  </h1>
                  <p className="text-white-50 mb-0">
                    Your AI-Powered Wellness Journal
                  </p>
                </div>

                <h2 className="text-white text-center mb-4 h5">Welcome Back</h2>

                {error && (
                  <Alert variant="danger" dismissible onClose={() => setError('')}>
                    {error}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label className="text-white fw-medium small">Username</Form.Label>
                    <Form.Control
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      placeholder="Enter your username"
                      className="glass-input"
                    />
                  </Form.Group>

                  <Form.Group className="mb-4">
                    <Form.Label className="text-white fw-medium small">Password</Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      placeholder="Enter your password"
                      className="glass-input"
                    />
                  </Form.Group>

                  <Button 
                    variant="light" 
                    type="submit" 
                    disabled={loading}
                    className="w-100 fw-bold py-2"
                  >
                    {loading ? 'Logging in...' : 'Login'}
                  </Button>
                </Form>

                <p className="text-center text-white mt-4 mb-0 small">
                  Don't have an account?{' '}
                  <Link to="/signup" className="text-white fw-bold text-decoration-none">
                    Sign up
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

export default Login;
