import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/Auth.css';

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
        
        <h2>Welcome Back</h2>
        <p className="auth-subtitle">Continue your mental wellness journey</p>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
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
              placeholder="Enter your username"
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
              placeholder="Enter your password"
              className="input-field"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? (
              <span className="btn-loader">
                <span className="spinner"></span>
                Logging in...
              </span>
            ) : (
              <>
                <span>Login</span>
                <span className="btn-arrow">→</span>
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          Don't have an account? <Link to="/signup" className="auth-link">Sign up now</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
