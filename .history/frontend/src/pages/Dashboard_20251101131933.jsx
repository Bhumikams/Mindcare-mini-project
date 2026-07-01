import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Dashboard.css';

function Dashboard() {
  const [entries, setEntries] = useState([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/journal/entries', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setEntries(response.data);
    } catch (error) {
      console.error('Error fetching entries:', error);
      setError('Failed to load entries');
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
      setSuccess('Journal entry saved successfully! ✨');
      setTimeout(() => setSuccess(''), 3000);
      fetchEntries();
    } catch (error) {
      setError('Failed to create entry. Please try again.');
      console.error('Error creating entry:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const getSentimentColor = (sentiment) => {
    const colors = {
      'positive': '#10b981',
      'negative': '#ef4444',
      'neutral': '#6b7280'
    };
    return colors[sentiment] || '#6b7280';
  };

  const getSentimentEmoji = (sentiment) => {
    const emojis = {
      'positive': '😊',
      'negative': '😔',
      'neutral': '😐'
    };
    return emojis[sentiment] || '😐';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-left">
          <div className="logo-small">🧠</div>
          <h1>MindCare</h1>
        </div>
        <div className="header-right">
          <div className="user-badge">
            <span className="user-avatar">👤</span>
            <span className="user-name">{username}</span>
          </div>
          <button onClick={handleLogout} className="btn-logout">
            <span>Logout</span>
            <span className="logout-icon">→</span>
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="journal-form-section">
          <div className="journal-form-card">
            <div className="form-header">
              <h2>✍️ How are you feeling today?</h2>
              <p>Share your thoughts and let AI analyze your emotions</p>
            </div>
            
            {error && (
              <div className="alert alert-error">
                <span className="alert-icon">⚠️</span>
                {error}
              </div>
            )}
            
            {success && (
              <div className="alert alert-success">
                <span className="alert-icon">✅</span>
                {success}
              </div>
            )}
            
            <form onSubmit={handleSubmit}>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write your thoughts, feelings, and experiences here..."
                rows="6"
                required
                className="journal-textarea"
              />
              <button type="submit" className="btn btn-primary-large" disabled={loading}>
                {loading ? (
                  <span className="btn-loader">
                    <span className="spinner"></span>
                    Analyzing...
                  </span>
                ) : (
                  <>
                    <span>💾 Save Journal Entry</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="entries-section">
          <div className="section-header">
            <h2>📖 Your Journal Entries</h2>
            <span className="entry-count">{entries.length} {entries.length === 1 ? 'entry' : 'entries'}</span>
          </div>
          
          {entries.length === 0 ? (
            <div className="no-entries">
              <div className="empty-icon">📝</div>
              <h3>No entries yet</h3>
              <p>Start by writing your first journal entry above!</p>
            </div>
          ) : (
            <div className="entries-grid">
              {entries.map((entry) => (
                <div key={entry.id} className="entry-card" style={{'--sentiment-color': getSentimentColor(entry.sentiment)}}>
                  <div className="entry-header">
                    <span className="entry-date">
                      <span className="date-icon">📅</span>
                      {formatDate(entry.created_at)}
                    </span>
                    <span className="entry-sentiment-badge" style={{background: getSentimentColor(entry.sentiment)}}>
                      {getSentimentEmoji(entry.sentiment)} {entry.sentiment}
                    </span>
                  </div>
                  <p className="entry-content">{entry.content}</p>
                  <div className="entry-footer">
                    <div className="emotion-info">
                      <span className="emotion-badge">
                        💭 {entry.primary_emotion}
                      </span>
                    </div>
                    <div className="score-badge">
                      <span className="score-label">Confidence</span>
                      <span className="score-value">{(entry.sentiment_score * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
