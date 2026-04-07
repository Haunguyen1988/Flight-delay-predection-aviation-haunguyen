import { useState, useRef } from 'react';
import { Upload, FileSpreadsheet, Database, Brain, RefreshCw } from 'lucide-react';
import Header from '../components/layout/Header';
import { useUpload, useFlightList } from '../hooks/useApi';

export default function DataManagement() {
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { progress, result, loading, error, upload, generateSample, trainModel } = useUpload();
  const [page, setPage] = useState(1);
  const { data: flightData, loading: listLoading, refetch } = useFlightList(page, 15);

  const handleDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragging(true); };
  const handleDragLeave = () => setDragging(false);
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };
  const handleFile = async (file: File) => {
    if (!file.name.endsWith('.csv')) return;
    await upload(file);
    refetch();
  };

  const handleGenerateSample = async () => {
    await generateSample();
    refetch();
  };

  const handleTrainModel = async () => {
    await trainModel();
  };

  return (
    <>
      <Header title="Data Management" subtitle="Import datasets and manage ML model" />
      <div className="animate-fade-in">
        {/* Action Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
          {/* Upload */}
          <div className="card" style={{ textAlign: 'center' }}>
            <FileSpreadsheet size={28} style={{ color: 'var(--accent-blue)', marginBottom: 8 }} />
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>Upload CSV</h3>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12 }}>
              Import your flight dataset
            </p>
            <button className="btn btn-primary btn-sm" onClick={() => fileInputRef.current?.click()}
              disabled={loading}>
              <Upload size={14} /> Choose File
            </button>
          </div>

          {/* Generate Sample */}
          <div className="card" style={{ textAlign: 'center' }}>
            <Database size={28} style={{ color: 'var(--accent-purple)', marginBottom: 8 }} />
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>Generate Sample</h3>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12 }}>
              Create 50K sample flights
            </p>
            <button className="btn btn-secondary btn-sm" onClick={handleGenerateSample}
              disabled={loading}>
              {loading && !result ? <><div className="spinner" style={{ width: 12, height: 12, borderWidth: 2 }} /> Generating...</>
                : <><RefreshCw size={14} /> Generate</>}
            </button>
          </div>

          {/* Train Model */}
          <div className="card" style={{ textAlign: 'center' }}>
            <Brain size={28} style={{ color: 'var(--accent-cyan)', marginBottom: 8 }} />
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>Train ML Model</h3>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12 }}>
              Train XGBoost + Random Forest
            </p>
            <button className="btn btn-secondary btn-sm" onClick={handleTrainModel}
              disabled={loading}>
              {loading && result?.type === 'training'
                ? <><div className="spinner" style={{ width: 12, height: 12, borderWidth: 2 }} /> Training...</>
                : <><Brain size={14} /> Train</>}
            </button>
          </div>
        </div>

        {/* Upload Zone (hidden file input) */}
        <input ref={fileInputRef} type="file" accept=".csv" style={{ display: 'none' }}
          onChange={handleFileSelect} />

        {/* Drop Zone */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className={`upload-zone ${dragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver} onDragLeave={handleDragLeave}
            onDrop={handleDrop} onClick={() => fileInputRef.current?.click()}
            style={{ padding: '32px 24px' }}>
            <div className="upload-icon"><Upload size={36} /></div>
            <div className="upload-text">Drag & drop CSV file here</div>
            <div className="upload-hint">or click to browse</div>
          </div>

          {loading && progress > 0 && (
            <div style={{ marginTop: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                <span>Uploading...</span><span>{progress}%</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }} />
              </div>
            </div>
          )}

          {result && (
            <div style={{
              marginTop: 12, padding: '10px 14px', borderRadius: 'var(--radius-md)',
              background: 'var(--success-bg)', color: 'var(--success)', fontSize: 13,
            }}>
              {result.type === 'training'
                ? `Model trained! Accuracy: ${(result.ensemble?.accuracy * 100).toFixed(1)}% (${result.duration_seconds}s)`
                : `Imported ${result.rows_imported?.toLocaleString()} flights in ${result.duration_seconds}s`}
            </div>
          )}

          {error && (
            <div style={{
              marginTop: 12, padding: '10px 14px', borderRadius: 'var(--radius-md)',
              background: 'var(--danger-bg)', color: 'var(--danger)', fontSize: 13,
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Flight Data Table */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h2 className="card-title" style={{ margin: 0 }}>Flight Data</h2>
            {flightData.total > 0 && (
              <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                {flightData.total.toLocaleString()} flights total
              </span>
            )}
          </div>

          {flightData.flights.length > 0 ? (
            <>
              <div style={{ overflowX: 'auto' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Flight</th>
                      <th>Airline</th>
                      <th>Route</th>
                      <th>Departure</th>
                      <th>Weather</th>
                      <th>Delay</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {flightData.flights.map((f: any) => (
                      <tr key={f.id}>
                        <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{f.flight_number}</td>
                        <td>{f.airline_code}</td>
                        <td>{f.origin} → {f.destination}</td>
                        <td>{f.scheduled_departure ? new Date(f.scheduled_departure).toLocaleDateString() : '-'}</td>
                        <td>{f.weather || '-'}</td>
                        <td>{f.delay_minutes > 0 ? `${f.delay_minutes}m` : '-'}</td>
                        <td>
                          <span className={`badge ${f.is_delayed ? 'badge-danger' : 'badge-success'}`}>
                            {f.is_delayed ? 'Delayed' : 'On Time'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              {flightData.total_pages > 1 && (
                <div className="pagination">
                  <button className="pagination-btn" disabled={page <= 1}
                    onClick={() => setPage(p => Math.max(1, p - 1))}>Prev</button>
                  {Array.from({ length: Math.min(5, flightData.total_pages) }, (_, i) => {
                    const start = Math.max(1, Math.min(page - 2, flightData.total_pages - 4));
                    const p = start + i;
                    return p <= flightData.total_pages ? (
                      <button key={p} className={`pagination-btn ${page === p ? 'active' : ''}`}
                        onClick={() => setPage(p)}>{p}</button>
                    ) : null;
                  })}
                  <button className="pagination-btn" disabled={page >= flightData.total_pages}
                    onClick={() => setPage(p => Math.min(flightData.total_pages, p + 1))}>Next</button>
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">📁</div>
              <div className="empty-title">{listLoading ? 'Loading...' : 'No Data Loaded'}</div>
              <div className="empty-desc">
                Upload a CSV or generate sample data to get started
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
