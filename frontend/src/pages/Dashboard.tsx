import { Plane, TrendingDown, Clock, CheckCircle } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area, CartesianGrid,
} from 'recharts';
import Header from '../components/layout/Header';
import { useFlightStats, useRouteDelays, useWeatherDelays, useTimeDelays } from '../hooks/useApi';

const CHART_COLORS = ['#3B82F6', '#7C3AED', '#06B6D4', '#22C55E', '#F59E0B', '#EF4444'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#1E293B', border: '1px solid rgba(148,163,184,0.1)',
      borderRadius: 8, padding: '10px 14px', fontSize: 12,
    }}>
      <p style={{ fontWeight: 600, marginBottom: 4 }}>{label}</p>
      {payload.map((p: any, i: number) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: {typeof p.value === 'number' ? p.value.toFixed(1) : p.value}
          {p.name === 'Delay Rate' ? '%' : ''}
        </p>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const { data: stats, loading: statsLoading } = useFlightStats();
  const { data: routeData } = useRouteDelays(8);
  const { data: weatherData } = useWeatherDelays();
  const { data: monthData } = useTimeDelays('month');
  const { data: hourData } = useTimeDelays('hour');

  const hasData = stats.total_flights > 0;

  const formatNumber = (n: number) => {
    if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
    return n.toString();
  };

  return (
    <>
      <Header title="Dashboard" subtitle="Flight Delay Analytics Overview" />
      <div className="animate-fade-in">
        {/* KPI Cards */}
        <div className="kpi-grid">
          <div className="kpi-card blue">
            <div className="kpi-icon"><Plane size={20} /></div>
            <div className="kpi-label">Total Flights</div>
            <div className="kpi-value">
              {statsLoading ? <div className="skeleton" style={{ width: 80, height: 32 }} /> : formatNumber(stats.total_flights)}
            </div>
            <div className="kpi-change" style={{ color: 'var(--text-muted)' }}>
              {hasData ? `${stats.delayed_count} delayed` : 'No data imported yet'}
            </div>
          </div>

          <div className="kpi-card purple">
            <div className="kpi-icon"><TrendingDown size={20} /></div>
            <div className="kpi-label">Delay Rate</div>
            <div className="kpi-value">
              {statsLoading ? <div className="skeleton" style={{ width: 60, height: 32 }} /> : `${stats.delay_rate}%`}
            </div>
            <div className={`kpi-change ${stats.delay_rate > 30 ? 'negative' : 'positive'}`}>
              {hasData ? (stats.delay_rate > 30 ? 'Above average' : 'Below average') : 'Upload data to see stats'}
            </div>
          </div>

          <div className="kpi-card cyan">
            <div className="kpi-icon"><Clock size={20} /></div>
            <div className="kpi-label">Avg Delay</div>
            <div className="kpi-value">
              {statsLoading ? <div className="skeleton" style={{ width: 60, height: 32 }} /> : `${stats.avg_delay_minutes}m`}
            </div>
            <div className="kpi-change" style={{ color: 'var(--text-muted)' }}>
              {hasData ? 'Average delay minutes' : 'No data'}
            </div>
          </div>

          <div className="kpi-card green">
            <div className="kpi-icon"><CheckCircle size={20} /></div>
            <div className="kpi-label">On-Time Rate</div>
            <div className="kpi-value">
              {statsLoading ? <div className="skeleton" style={{ width: 60, height: 32 }} /> : `${stats.ontime_rate}%`}
            </div>
            <div className="kpi-change positive">
              {hasData ? 'Flights on schedule' : 'No data'}
            </div>
          </div>
        </div>

        {/* Charts */}
        {hasData ? (
          <div className="charts-grid">
            {/* Top Routes by Delay Rate */}
            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">Top Routes by Delay Rate</h3>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={routeData} layout="vertical"
                  margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.08)" />
                  <XAxis type="number" domain={[0, 'auto']} tick={{ fill: '#94A3B8', fontSize: 11 }}
                    tickFormatter={(v) => `${v}%`} />
                  <YAxis type="category" dataKey="route" width={100}
                    tick={{ fill: '#94A3B8', fontSize: 11 }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="delay_rate" name="Delay Rate" radius={[0, 4, 4, 0]}>
                    {routeData.map((_: any, i: number) => (
                      <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Weather Impact - Pie Chart */}
            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">Delay by Weather Condition</h3>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={weatherData} cx="50%" cy="50%" innerRadius={60} outerRadius={100}
                    dataKey="delayed" nameKey="weather" paddingAngle={3}
                    label={({ weather, rate }: any) => `${weather}: ${rate}%`}>
                    {weatherData.map((_: any, i: number) => (
                      <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Monthly Trend */}
            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">Delay Trend by Month</h3>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={monthData}
                  margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <defs>
                    <linearGradient id="gradBlue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.08)" />
                  <XAxis dataKey="label" tick={{ fill: '#94A3B8', fontSize: 11 }} />
                  <YAxis tick={{ fill: '#94A3B8', fontSize: 11 }}
                    tickFormatter={(v) => `${v}%`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="rate" name="Delay Rate"
                    stroke="#3B82F6" strokeWidth={2}
                    fill="url(#gradBlue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Hourly Pattern */}
            <div className="chart-card">
              <div className="chart-header">
                <h3 className="chart-title">Delay by Time of Day</h3>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={hourData}
                  margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.08)" />
                  <XAxis dataKey="label" tick={{ fill: '#94A3B8', fontSize: 10 }}
                    interval={1} />
                  <YAxis tick={{ fill: '#94A3B8', fontSize: 11 }}
                    tickFormatter={(v) => `${v}%`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="rate" name="Delay Rate" fill="#7C3AED"
                    radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <div className="charts-grid">
            {['Top Routes by Delay Rate', 'Delay by Weather', 'Monthly Trend', 'Hourly Pattern'].map((title, i) => (
              <div className="chart-card" key={i}>
                <div className="chart-header"><h3 className="chart-title">{title}</h3></div>
                <div className="empty-state" style={{ padding: '32px 16px' }}>
                  <div className="empty-icon">{['📊', '🌦️', '📈', '🕐'][i]}</div>
                  <div className="empty-title">No Data Yet</div>
                  <div className="empty-desc">Import flight data to see analytics</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
