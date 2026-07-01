import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/Glass.css';

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
      
      <div className="glass-card">
        <div className="glass-card-header">
          <div className="app-icon">🧠</div>
          <h1 className="app-title">MindCare</h1>
          <p className="app-subtitle">Your AI-Powered Wellness Journal</p>
        </div>

        <h2 className="form-title">Welcome Back</h2>
        
        {error && (
          <div className="glass-alert error">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="glass-form">
          <div className="form-field">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Enter your username"
              className="glass-input"
            />
          </div>

          <div className="form-field">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
              className="glass-input"
            />
          </div>

          <button type="submit" className="glass-btn primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner-small"></span>
                <span>Logging in...</span>
              </>
            ) : (
              'Login'
            )}
          </button>
        </form>

        <p className="form-footer">
          Don't have an account? <Link to="/signup" className="link-primary">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
