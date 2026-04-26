import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Mountain, Flame, BarChart3, Home as HomeIcon, LayoutDashboard } from 'lucide-react';
import HillClimbing from './components/HillClimbing/HillClimbing';
import SimulatedAnnealing from './components/SimulatedAnnealing/SimulatedAnnealing';
import Comparison from './components/Comparison/Comparison';

const Home = () => (
  <div style={homeContainerStyle}>
    <header style={headerStyle}>
      <h1 style={titleStyle}>Algoritmos de Optimización</h1>
      <p style={subtitleStyle}>Plataforma de visualización para heurísticas de búsqueda local.</p>
    </header>
    
    <div style={gridStyle}>
      <Link to="/hill-climbing" style={cardStyle}>
        <div style={iconWrapperStyle}><Mountain size={40} color="#2563eb" /></div>
        <h3 style={cardTitleStyle}>Hill Climbing</h3>
        <p style={cardTextStyle}>Algoritmo de ascenso infinito que busca el óptimo local más cercano mediante movimientos codiciosos.</p>
        <span style={btnStyle}>Explorar Módulo</span>
      </Link>

      <Link to="/simulated-annealing" style={cardStyle}>
        <div style={iconWrapperStyle}><Flame size={40} color="#f59e0b" /></div>
        <h3 style={cardTitleStyle}>Simulated Annealing</h3>
        <p style={cardTextStyle}>Técnica probabilística que permite saltos a estados peores para escapar de máximos locales.</p>
        <span style={btnStyle}>Explorar Módulo</span>
      </Link>

      <Link to="/comparison" style={cardStyle}>
        <div style={iconWrapperStyle}><BarChart3 size={40} color="#10b981" /></div>
        <h3 style={cardTitleStyle}>Comparativa</h3>
        <p style={cardTextStyle}>Análisis cuantitativo de rendimiento, tiempo de ejecución y calidad de la solución encontrada.</p>
        <span style={btnStyle}>Ver Resultados</span>
      </Link>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div style={appShellStyle}>
        <nav style={navStyle}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <LayoutDashboard size={24} color="#38bdf8" />
            <Link to="/" style={navLogoStyle}>IA Lab 2026</Link>
          </div>
          <div style={navLinksStyle}>
            <Link to="/" style={navLinkItem}><HomeIcon size={18} /> Inicio</Link>
            <Link to="/hill-climbing" style={navLinkItem}>Hill Climbing</Link>
            <Link to="/simulated-annealing" style={navLinkItem}>Simulated Annealing</Link>
            <Link to="/comparison" style={navLinkItem}>Comparativa</Link>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/hill-climbing" element={<HillClimbing />} />
            <Route path="/simulated-annealing" element={<SimulatedAnnealing />} />
            <Route path="/comparison" element={<Comparison />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

const appShellStyle = {
  minHeight: '100vh',
  backgroundColor: '#f8fafc',
  fontFamily: "'Inter', sans-serif",
  color: '#1e293b'
};

const navStyle = {
  backgroundColor: '#0f172a',
  padding: '0.75rem 2rem',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  position: 'sticky',
  top: 0,
  zIndex: 100
};

const navLogoStyle = {
  color: '#f8fafc',
  textDecoration: 'none',
  fontWeight: '700',
  fontSize: '1.1rem'
};

const navLinksStyle = { 
  display: 'flex', 
  gap: '1.5rem',
  alignItems: 'center'
};

const navLinkItem = {
  color: '#94a3b8',
  textDecoration: 'none',
  fontSize: '0.85rem',
  fontWeight: '500',
  display: 'flex',
  alignItems: 'center',
  gap: '6px'
};

const homeContainerStyle = {
  maxWidth: '1100px',
  margin: '0 auto',
  padding: '5rem 1.5rem'
};

const headerStyle = { textAlign: 'center', marginBottom: '4rem' };

const titleStyle = {
  fontSize: '2.5rem',
  fontWeight: '800',
  color: '#0f172a',
  letterSpacing: '-0.02em',
  marginBottom: '0.5rem'
};

const subtitleStyle = { color: '#64748b', fontSize: '1.1rem' };

const gridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
  gap: '1.5rem'
};

const cardStyle = {
  backgroundColor: '#ffffff',
  padding: '2.5rem 2rem',
  borderRadius: '16px',
  textDecoration: 'none',
  color: 'inherit',
  border: '1px solid #e2e8f0',
  transition: 'all 0.2s ease',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  textAlign: 'center',
  boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  cursor: 'pointer'
};

const iconWrapperStyle = {
  backgroundColor: '#f1f5f9',
  width: '72px',
  height: '72px',
  borderRadius: '16px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  marginBottom: '1.5rem',
  flexShrink: 0
};

const cardTitleStyle = { fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.75rem' };
const cardTextStyle = { color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', marginBottom: '1.5rem', flexGrow: 1 };
const btnStyle = { 
  color: '#2563eb', 
  fontWeight: '600', 
  fontSize: '0.95rem', 
  borderTop: '1px solid #f1f5f9', 
  paddingTop: '1.25rem',
  marginTop: 'auto',
  width: '100%',
  textAlign: 'center'
};

export default App;