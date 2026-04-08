import { useState } from 'react';
import { Brain, Sparkles, AlertTriangle, CheckCircle2, Info } from 'lucide-react';
import Header from '../components/layout/Header';
import { usePrediction, usePredictionHistory, useModelInfo } from '../hooks/useApi';

const AIRLINES = [
  { code: 'AA', name: 'American Airlines' },
  { code: 'DL', name: 'Delta Air Lines' },
  { code: 'UA', name: 'United Airlines' },
  { code: 'WN', name: 'Southwest Airlines' },
  { code: 'B6', name: 'JetBlue Airways' },
  { code: 'AS', name: 'Alaska Airlines' },
  { code: 'NK', name: 'Spirit Airlines' },
  { code: 'F9', name: 'Frontier Airlines' },
  { code: 'VN', name: 'Vietnam Airlines' },
  { code: 'VJ', name: 'VietJet Air' },
];

const WEATHER = ['Clear', 'Cloudy', 'Rain', 'Fog', 'Snow'];

export default function Prediction() {
  const [form, setForm] = useState({
    airline: '',
    origin: '',
    destination: '',
    departure_datetime: '',
    weather_condition: 'Clear',
  });

  const { result, loading, error, predict } = usePrediction();
  const {
    data: history,
    loading: historyLoading,
    error: historyError,
    refetch: refetchHistory,
  } = usePredictionHistory(1, 5);
  const { data: modelInfo } = useModelInfo();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await predict({
      airline: form.airline,
      origin: form.origin.toUpperCase(),
      destination: form.destination.toUpperCase(),
      departure_datetime: form.departure_datetime.replace('T', ' ') + ':00',
      weather_condition: form.weather_condition,
    });
    await refetchHistory();
  };

  const getProbabilityClass = (prob: number) => {
    if (prob < 0.3) return 'low';
    if (prob < 0.6) return 'medium';
    return 'high';
  };

  const getProbabilityLabel = (prob: number) => {
    if (prob < 0.2) return { text: 'Very Low Risk', icon: <CheckCircle2 size={20} /> };
    if (prob < 0.4) return { text: 'Low Risk', icon: <CheckCircle2 size={20} /> };
    if (prob < 0.6) return { text: 'Moderate Risk', icon: <AlertTriangle size={20} /> };
    if (prob < 0.8) return { text: 'High Risk', icon: <AlertTriangle size={20} /> };
    return { text: 'Very High Risk', icon: <AlertTriangle size={20} /> };
  };

  const formatDateTime = (value: string | null) => {
    if (!value) return 'N/A';
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
  };

  const getBandStyle = (band: string) => {
    const normalizedBand = band.toLowerCase();

    if (['very high', 'high', 'severe', 'major'].includes(normalizedBand)) {
      return {
        background: 'var(--danger-bg)',
        color: 'var(--danger)',
      };
    }
    if (normalizedBand === 'moderate' || normalizedBand === 'medium') {
      return {
        background: 'var(--warning-bg)',
        color: 'var(--warning)',
      };
    }
    return {
      background: 'var(--success-bg)',
      color: 'var(--success)',
    };
  };

  const renderBand = (label: string, value: string) => (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      padding: '6px 10px',
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 700,
      letterSpacing: 0.2,
      ...getBandStyle(value),
    }}>
      <span style={{ opacity: 0.75 }}>{label}</span>
      <span>{value}</span>
    </span>
  );

  const renderImpactBadge = (impact: string) => (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '5px 10px',
      borderRadius: 999,
      fontSize: 11,
      fontWeight: 700,
      textTransform: 'uppercase',
      letterSpacing: 0.4,
      ...getBandStyle(impact),
    }}>
      {impact}
    </span>
  );

  return (
    <>
      <Header title="Prediction" subtitle="AI-powered flight delay prediction" />
      <div className="animate-fade-in">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
          {/* Form */}
          <div className="card">
            <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Brain size={16} />
              Prediction Input
            </h2>

            {modelInfo.status !== 'trained' && (
              <div style={{
                padding: '10px 14px', borderRadius: 'var(--radius-md)',
                background: 'var(--warning-bg)', color: 'var(--warning)',
                fontSize: 13, marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8,
              }}>
                <Info size={14} />
                Model not trained. Go to Data page to train first.
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Airline</label>
                <select className="form-select" value={form.airline}
                  onChange={(e) => setForm({ ...form, airline: e.target.value })} required>
                  <option value="">Select airline...</option>
                  {AIRLINES.map((a) => (
                    <option key={a.code} value={a.code}>{a.name} ({a.code})</option>
                  ))}
                </select>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div className="form-group">
                  <label className="form-label">Origin Airport</label>
                  <input className="form-input" type="text" placeholder="e.g., JFK"
                    value={form.origin} maxLength={5} required
                    onChange={(e) => setForm({ ...form, origin: e.target.value.toUpperCase() })} />
                </div>
                <div className="form-group">
                  <label className="form-label">Destination Airport</label>
                  <input className="form-input" type="text" placeholder="e.g., LAX"
                    value={form.destination} maxLength={5} required
                    onChange={(e) => setForm({ ...form, destination: e.target.value.toUpperCase() })} />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Departure Date & Time</label>
                <input className="form-input" type="datetime-local"
                  value={form.departure_datetime} required
                  onChange={(e) => setForm({ ...form, departure_datetime: e.target.value })} />
              </div>

              <div className="form-group">
                <label className="form-label">Weather Condition</label>
                <select className="form-select" value={form.weather_condition}
                  onChange={(e) => setForm({ ...form, weather_condition: e.target.value })}>
                  {WEATHER.map((w) => (
                    <option key={w} value={w}>{w}</option>
                  ))}
                </select>
              </div>

              <button type="submit" className="btn btn-primary btn-lg" style={{ width: '100%', marginTop: 8 }}
                disabled={loading}>
                {loading ? (
                  <><div className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} /> Predicting...</>
                ) : (
                  <><Sparkles size={18} /> Predict Delay</>
                )}
              </button>
            </form>

            {error && (
              <div style={{
                marginTop: 16, padding: '10px 14px', borderRadius: 'var(--radius-md)',
                background: 'var(--danger-bg)', color: 'var(--danger)', fontSize: 13,
              }}>
                {error}
              </div>
            )}
          </div>

          {/* Result */}
          <div>
            {result ? (
              <>
                <div className="prediction-result animate-scale-in">
                  <div style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                    color: 'var(--text-secondary)', marginBottom: 8,
                  }}>
                    {getProbabilityLabel(result.delay_probability).icon}
                    <span style={{ fontSize: 14, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>
                      {getProbabilityLabel(result.delay_probability).text}
                    </span>
                  </div>

                  <div className={`result-probability ${getProbabilityClass(result.delay_probability)}`}>
                    {(result.delay_probability * 100).toFixed(1)}%
                  </div>

                  <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 20 }}>
                    Delay Probability
                  </p>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    gap: 8,
                    flexWrap: 'wrap',
                    marginBottom: 20,
                  }}>
                    {renderBand('Risk', result.risk_band)}
                  </div>

                  <div className="result-detail">
                    <div className="result-item">
                      <span className="label">Est. Delay</span>
                      <span className="value">{result.estimated_delay_minutes}m</span>
                    </div>
                    <div className="result-item">
                      <span className="label">Severity</span>
                      <span className="value">{result.severity_band}</span>
                    </div>
                    <div className="result-item">
                      <span className="label">Confidence</span>
                      <span className="value">{result.confidence}</span>
                    </div>
                  </div>

                  {result.model_scores && (
                    <div style={{
                      marginTop: 24, padding: 16, background: 'var(--bg-input)',
                      borderRadius: 'var(--radius-md)', textAlign: 'left',
                    }}>
                      <p style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 8 }}>
                        MODEL SCORES
                      </p>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13 }}>
                        <span style={{ color: 'var(--text-muted)' }}>XGBoost</span>
                        <span style={{ fontWeight: 600 }}>{(result.model_scores.xgboost * 100).toFixed(1)}%</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginTop: 4 }}>
                        <span style={{ color: 'var(--text-muted)' }}>Random Forest</span>
                        <span style={{ fontWeight: 600 }}>{(result.model_scores.random_forest * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  )}
                </div>

                {result.recommendations.length > 0 && (
                  <div className="card" style={{ marginTop: 16 }}>
                    <h3 className="card-title">Recommended Actions</h3>
                    <ul style={{
                      margin: 0,
                      paddingLeft: 18,
                      display: 'grid',
                      gap: 10,
                      color: 'var(--text-secondary)',
                      fontSize: 14,
                    }}>
                      {result.recommendations.map((recommendation) => (
                        <li key={recommendation}>{recommendation}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.explanations.length > 0 && (
                  <div className="card" style={{ marginTop: 16 }}>
                    <h3 className="card-title">Why this prediction?</h3>
                    <div style={{ display: 'grid', gap: 12 }}>
                      {result.explanations.map((explanation) => (
                        <div
                          key={`${explanation.factor}-${explanation.message}`}
                          style={{
                            padding: 14,
                            borderRadius: 'var(--radius-md)',
                            background: 'var(--bg-input)',
                            border: '1px solid var(--border)',
                          }}
                        >
                          <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            gap: 12,
                            alignItems: 'center',
                            flexWrap: 'wrap',
                            marginBottom: 8,
                          }}>
                            <div style={{ fontSize: 14, fontWeight: 700 }}>{explanation.factor}</div>
                            {renderImpactBadge(explanation.impact)}
                          </div>
                          <div style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                            {explanation.message}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="card">
                <div className="empty-state">
                  <div className="empty-icon">🔮</div>
                  <div className="empty-title">Ready to Predict</div>
                  <div className="empty-desc">
                    Fill in flight details and click "Predict Delay" to get an AI-powered prediction
                  </div>
                </div>
              </div>
            )}

            {/* Model Info Card */}
            {modelInfo.status === 'trained' && modelInfo.ensemble && (
              <div className="card" style={{ marginTop: 16 }}>
                <h3 className="card-title">Model Performance</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
                  {[
                    { label: 'Accuracy', value: `${((modelInfo.ensemble.accuracy ?? 0) * 100).toFixed(1)}%` },
                    { label: 'Precision', value: `${((modelInfo.ensemble.precision ?? 0) * 100).toFixed(1)}%` },
                    { label: 'Recall', value: `${((modelInfo.ensemble.recall ?? 0) * 100).toFixed(1)}%` },
                    { label: 'F1 Score', value: `${((modelInfo.ensemble.f1_score ?? 0) * 100).toFixed(1)}%` },
                  ].map((m) => (
                    <div key={m.label} style={{
                      padding: '12px', background: 'var(--bg-input)',
                      borderRadius: 'var(--radius-md)', textAlign: 'center',
                    }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>{m.label}</div>
                      <div style={{ fontSize: 18, fontWeight: 700 }}>{m.value}</div>
                    </div>
                  ))}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 12, textAlign: 'center' }}>
                  Trained on {modelInfo.dataset_size?.toLocaleString()} flights
                  {modelInfo.trained_at && ` • ${new Date(modelInfo.trained_at).toLocaleDateString()}`}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="card" style={{ marginTop: 24 }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 12,
            marginBottom: 16,
            flexWrap: 'wrap',
          }}>
            <div>
              <h2 className="card-title" style={{ marginBottom: 4 }}>Recent Predictions</h2>
              <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                Latest saved prediction results from the single-flight workflow.
              </p>
            </div>
            <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
              {history.total > 0 ? `${history.total} saved` : 'No saved predictions yet'}
            </div>
          </div>

          {historyError && (
            <div style={{
              marginBottom: 16,
              padding: '10px 14px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--danger-bg)',
              color: 'var(--danger)',
              fontSize: 13,
            }}>
              {historyError}
            </div>
          )}

          {historyLoading ? (
            <div className="empty-state" style={{ minHeight: 180 }}>
              <div className="spinner" />
              <div className="empty-title">Loading recent predictions</div>
              <div className="empty-desc">
                Fetching the latest saved prediction history from the backend.
              </div>
            </div>
          ) : history.items.length === 0 ? (
            <div className="empty-state" style={{ minHeight: 180 }}>
              <div className="empty-icon">History</div>
              <div className="empty-title">No prediction history yet</div>
              <div className="empty-desc">
                Successful single predictions will appear here once they are saved.
              </div>
            </div>
          ) : (
            <div style={{ display: 'grid', gap: 12 }}>
              {history.items.map((item) => (
                <div
                  key={item.id}
                  style={{
                    padding: 16,
                    borderRadius: 'var(--radius-md)',
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border)',
                  }}
                >
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    gap: 12,
                    flexWrap: 'wrap',
                    marginBottom: 12,
                  }}>
                    <div>
                      <div style={{ fontSize: 16, fontWeight: 700 }}>
                        {item.origin} {'->'} {item.destination}
                      </div>
                      <div style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 4 }}>
                        {item.airline} • Departure {formatDateTime(item.departure_datetime)}
                      </div>
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      Saved {formatDateTime(item.created_at)}
                    </div>
                  </div>

                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
                    gap: 12,
                  }}>
                    <div style={{ padding: 12, borderRadius: 'var(--radius-md)', background: 'var(--bg-card)' }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Delay Probability</div>
                      <div style={{ fontSize: 18, fontWeight: 700 }}>
                        {(item.delay_probability * 100).toFixed(1)}%
                      </div>
                    </div>
                    <div style={{ padding: 12, borderRadius: 'var(--radius-md)', background: 'var(--bg-card)' }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 8 }}>Risk Band</div>
                      {renderBand('Risk', item.risk_band)}
                    </div>
                    <div style={{ padding: 12, borderRadius: 'var(--radius-md)', background: 'var(--bg-card)' }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Estimated Delay</div>
                      <div style={{ fontSize: 18, fontWeight: 700 }}>{item.estimated_delay_minutes}m</div>
                    </div>
                    <div style={{ padding: 12, borderRadius: 'var(--radius-md)', background: 'var(--bg-card)' }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 8 }}>Severity</div>
                      {renderBand('Severity', item.severity_band)}
                    </div>
                    <div style={{ padding: 12, borderRadius: 'var(--radius-md)', background: 'var(--bg-card)' }}>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Confidence</div>
                      <div style={{ fontSize: 18, fontWeight: 700 }}>{item.confidence}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
