import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/Glass.css';

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
      
      <div className="glass-card">
        <div className="glass-card-header">
          <div className="app-icon">🧠</div>
          <h1 className="app-title">MindCare</h1>
          <p className="app-subtitle">Your AI-Powered Wellness Journal</p>
        </div>

        <h2 className="form-title">Create Account</h2>
        
        {error && (
          <div className="glass-alert error">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="glass-form">
          <div className="form-field">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your.email@example.com"
              className="glass-input"
            />
          </div>

          <div className="form-field">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Choose a username"
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
              minLength="8"
              placeholder="Min 8 characters"
              className="glass-input"
            />
          </div>

          <button type="submit" className="glass-btn primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner-small"></span>
                <span>Creating account...</span>
              </>
            ) : (
              'Sign Up'
            )}
          </button>
        </form>

        <p className="form-footer">
          Already have an account? <Link to="/login" className="link-primary">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
