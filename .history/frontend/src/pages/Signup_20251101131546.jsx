import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/Auth.css';

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
    <div className="auth-container">
      <div className="auth-background">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>
      
      <div className="auth-card">
        <div className="auth-logo">
          <div className="logo-icon">🧠</div>
          <h1>MindCare</h1>
        </div>
        
        <h2>Create Account</h2>
        <p className="auth-subtitle">Start your mental wellness journey today</p>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">
              <span className="label-icon">📧</span>
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your.email@example.com"
              className="input-field"
            />
          </div>

          <div className="form-group">
            <label htmlFor="username">
              <span className="label-icon">👤</span>
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Choose a unique username"
              className="input-field"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <span className="label-icon">🔒</span>
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength="8"
              placeholder="Min 8 characters"
              className="input-field"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? (
              <span className="btn-loader">
                <span className="spinner"></span>
                Creating account...
              </span>
            ) : (
              <>
                <span>Sign Up</span>
                <span className="btn-arrow">→</span>
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login" className="auth-link">Login here</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
