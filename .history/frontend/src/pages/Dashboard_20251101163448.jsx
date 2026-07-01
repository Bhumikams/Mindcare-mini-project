import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Glass.css';

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
    } catch (error) {
      console.error('Error fetching entries:', error);
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
    } catch (error) {
      console.error('Error fetching activities:', error);
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
    } catch (error) {
      setError('Failed to create entry');
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
      'positive': 'var(--color-success)',
      'negative': 'var(--color-error)',
      'neutral': 'var(--color-neutral)'
    }[sentiment] || 'var(--color-neutral)';
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

      <header className="glass-header">
        <div className="header-content">
          <div className="header-left">
            <div className="app-icon-small">🧠</div>
            <h1>MindCare</h1>
          </div>
          <div className="header-right">
            <div className="user-info">
              <span className="user-avatar">👤</span>
              <span>{username}</span>
            </div>
            <button onClick={handleLogout} className="glass-btn secondary small">
              Logout →
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-content">
        <div className="glass-section">
          <div className="glass-card large">
            <h2 className="section-title">✍️ How are you feeling?</h2>
            <p className="section-subtitle">Let AI understand your emotions</p>

            {error && (
              <div className="glass-alert error">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="glass-alert success">
                <span>✅</span>
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Share your thoughts, feelings, and experiences..."
                rows="5"
                required
                className="glass-textarea"
              />
              <button type="submit" className="glass-btn primary full-width" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner-small"></span>
                    <span>Analyzing...</span>
                  </>
                ) : (
                  '💾 Save Entry'
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="glass-section">
          <div className="section-header">
            <h2>📖 Your Journal ({entries.length})</h2>
          </div>

          {entries.length === 0 ? (
            <div className="glass-card empty-state">
              <div className="empty-icon">📝</div>
              <h3>No entries yet</h3>
              <p>Start journaling to track your mental wellness</p>
            </div>
          ) : (
            <div className="entries-grid">
              {entries.map((entry) => (
                <div key={entry.id} className="glass-card entry-card">
                  <div className="entry-header">
                    <span className="entry-date">📅 {formatDate(entry.created_at)}</span>
                    <span className="sentiment-badge" style={{background: getSentimentColor(entry.sentiment)}}>
                      {getSentimentEmoji(entry.sentiment)} {entry.sentiment}
                    </span>
                  </div>

                  <p className="entry-text">{entry.content}</p>

                  <div className="entry-meta">
                    <span className="emotion-tag">💭 {entry.primary_emotion}</span>
                    <span className="confidence-score">{(entry.sentiment_score * 100).toFixed(0)}%</span>
                  </div>

                  <button 
                    className="glass-btn secondary full-width small"
                    onClick={() => fetchActivities(entry.id)}
                  >
                    💡 Get Suggestions
                  </button>

                  {selectedEntry === entry.id && activities && (
                    <div className="activities-panel">
                      <h4>{activities.message}</h4>
                      {activities.recommendations.map((activity, idx) => (
                        <div key={idx} className="activity-card">
                          <span className="activity-icon">{activity.icon}</span>
                          <div>
                            <strong>{activity.activity}</strong>
                            <p>{activity.description}</p>
                          </div>
                        </div>
                      ))}
                      <div className="activity-tip">{activities.additional_tip}</div>
                    </div>
                  )}
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
