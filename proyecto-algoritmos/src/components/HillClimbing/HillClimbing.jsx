import React, { useEffect, useRef, useState, useCallback } from 'react';

export default function HillClimbing() {
  const mainCanvasRef = useRef(null);
  const treeCanvasRef = useRef(null);
  const graphCanvasRef = useRef(null);
  const timerRef = useRef(null);

  const [position, setPosition] = useState(150);
  const [isRunning, setIsRunning] = useState(false);
  const [iterations, setIterations] = useState(0);
  const [history, setHistory] = useState([]);
  const [stepSize, setStepSize] = useState(2);
  const [converged, setConverged] = useState(false);
  const [treeNodes, setTreeNodes] = useState([]);
  const [treeEdges, setTreeEdges] = useState([]);
  const [status, setStatus] = useState('LISTO');
  const [activeTab, setActiveTab] = useState('landscape');

  // Graph TSP state
  const [numNodes, setNumNodes] = useState(4);
  const [graphMatrix, setGraphMatrix] = useState([
    [0, 200, 600, 100],
    [200, 0, 300, 100],
    [600, 300, 0, 400],
    [100, 100, 400, 0],
  ]);
  const [graphPositions, setGraphPositions] = useState([]);
  const [tspResult, setTspResult] = useState(null);
  const [tspLog, setTspLog] = useState([]);
  const [tspRunning, setTspRunning] = useState(false);
  const [currentTspPath, setCurrentTspPath] = useState(null);
  const [currentTspCost, setCurrentTspCost] = useState(null);
  const [editingCell, setEditingCell] = useState(null);

  const stateRef = useRef({ position: 150, treeNodes: [], treeEdges: [], iterations: 0, history: [], stepSize: 2, converged: false });

  const W = 780, H = 300, TW = 740;
  const NODE_R = 12, V_GAP = 46;
  const GW = 500, GH = 320;

  // ─── Landscape helpers ───────────────────────────────────────────────────────

  function getElevation(x) {
    return 100 + 70 * Math.sin(x / 65) + 38 * Math.cos(x / 28) + 28 * Math.sin(x / 12) + 14 * Math.cos(x / 6);
  }

  // ─── Draw landscape ──────────────────────────────────────────────────────────

  const drawMain = useCallback((pos, nodes) => {
    const canvas = mainCanvasRef.current;
    if (!canvas) return;
    const mc = canvas.getContext('2d');
    mc.clearRect(0, 0, W, H);

    mc.strokeStyle = 'rgba(0,0,0,0.05)';
    mc.lineWidth = 0.5;
    for (let x = 0; x < W; x += 50) { mc.beginPath(); mc.moveTo(x, 0); mc.lineTo(x, H); mc.stroke(); }
    for (let y = 0; y < H; y += 40) { mc.beginPath(); mc.moveTo(0, y); mc.lineTo(W, y); mc.stroke(); }

    mc.beginPath();
    mc.moveTo(0, H);
    for (let x = 0; x <= W; x++) mc.lineTo(x, H - 20 - getElevation(x) * 1.1);
    mc.lineTo(W, H);
    mc.closePath();
    mc.fillStyle = 'rgba(37,99,235,0.07)';
    mc.fill();

    mc.beginPath();
    mc.moveTo(0, H - 20 - getElevation(0) * 1.1);
    for (let x = 1; x <= W; x++) mc.lineTo(x, H - 20 - getElevation(x) * 1.1);
    mc.strokeStyle = '#2563eb';
    mc.lineWidth = 2;
    mc.stroke();

    for (let i = 1; i < nodes.length; i++) {
      const prev = nodes[i - 1], cur = nodes[i];
      if (cur.parent !== null) {
        mc.beginPath();
        mc.moveTo(prev.px, H - 20 - getElevation(prev.px) * 1.1 - 1);
        mc.lineTo(cur.px, H - 20 - getElevation(cur.px) * 1.1 - 1);
        mc.strokeStyle = 'rgba(217,119,6,0.35)';
        mc.lineWidth = 1.5;
        mc.setLineDash([4, 3]);
        mc.stroke();
        mc.setLineDash([]);
      }
    }

    const agentY = H - 20 - getElevation(pos) * 1.1;
    mc.beginPath();
    mc.arc(pos, agentY, 7, 0, Math.PI * 2);
    mc.fillStyle = '#d97706';
    mc.fill();
    mc.strokeStyle = '#1e293b';
    mc.lineWidth = 1.5;
    mc.stroke();

    mc.fillStyle = 'rgba(255,255,255,0.88)';
    mc.fillRect(pos - 26, agentY - 28, 52, 18);
    mc.fillStyle = '#1e293b';
    mc.font = '11px sans-serif';
    mc.textAlign = 'center';
    mc.fillText('x=' + Math.round(pos), pos, agentY - 14);
  }, []);

  // ─── Draw tree ───────────────────────────────────────────────────────────────

  const drawTree = useCallback((nodes, edges, conv) => {
    const canvas = treeCanvasRef.current;
    if (!canvas) return;
    const treeHeight = Math.max(360, (nodes.length + 2) * V_GAP + 60);
    canvas.height = treeHeight;
    const tc = canvas.getContext('2d');
    tc.clearRect(0, 0, TW, treeHeight);
    const chainX = TW / 2;
    const positioned = nodes.map((n, i) => ({ ...n, cx: chainX, cy: 40 + i * V_GAP }));

    edges.forEach(e => {
      const from = positioned[e.from];
      if (!from) return;
      if (e.type === 'main') {
        const to = positioned[e.to];
        if (!to) return;
        tc.beginPath();
        tc.moveTo(from.cx, from.cy + NODE_R);
        tc.lineTo(to.cx, to.cy - NODE_R);
        tc.strokeStyle = '#2563eb';
        tc.lineWidth = 1.5;
        tc.setLineDash([]);
        tc.stroke();
        const angle = Math.atan2(to.cy - from.cy, to.cx - from.cx);
        const ax = to.cx - Math.cos(angle) * (NODE_R + 1);
        const ay = to.cy - Math.sin(angle) * (NODE_R + 1);
        tc.beginPath();
        tc.moveTo(ax, ay);
        tc.lineTo(ax - 6 * Math.cos(angle - 0.4), ay - 6 * Math.sin(angle - 0.4));
        tc.moveTo(ax, ay);
        tc.lineTo(ax - 6 * Math.cos(angle + 0.4), ay - 6 * Math.sin(angle + 0.4));
        tc.strokeStyle = '#2563eb';
        tc.lineWidth = 1;
        tc.stroke();
      } else {
        const sideX = e.side === 'left' ? from.cx - 80 : from.cx + 80;
        const sideY = from.cy + V_GAP * 0.7;
        tc.beginPath();
        tc.moveTo(from.cx, from.cy + NODE_R);
        tc.bezierCurveTo(from.cx, from.cy + 22, sideX, sideY - 12, sideX, sideY);
        tc.strokeStyle = 'rgba(220,38,38,0.3)';
        tc.lineWidth = 1;
        tc.setLineDash([3, 3]);
        tc.stroke();
        tc.setLineDash([]);
        tc.beginPath();
        tc.arc(sideX, sideY, 8, 0, Math.PI * 2);
        tc.fillStyle = 'rgba(254,226,226,1)';
        tc.fill();
        tc.strokeStyle = 'rgba(220,38,38,0.5)';
        tc.lineWidth = 0.5;
        tc.stroke();
        tc.strokeStyle = 'rgba(220,38,38,0.8)';
        tc.lineWidth = 1;
        tc.beginPath();
        tc.moveTo(sideX - 3, sideY - 3); tc.lineTo(sideX + 3, sideY + 3);
        tc.moveTo(sideX + 3, sideY - 3); tc.lineTo(sideX - 3, sideY + 3);
        tc.stroke();
        tc.fillStyle = 'rgba(220,38,38,0.8)';
        tc.font = '10px sans-serif';
        tc.textAlign = e.side === 'left' ? 'end' : 'start';
        tc.fillText('z=' + e.z.toFixed(1), e.side === 'left' ? sideX - 12 : sideX + 12, sideY + 3);
      }
    });

    positioned.forEach((n, i) => {
      const isLast = i === nodes.length - 1;
      tc.beginPath();
      tc.arc(n.cx, n.cy, NODE_R, 0, Math.PI * 2);
      if (isLast && conv) tc.fillStyle = '#16a34a';
      else if (isLast) tc.fillStyle = '#d97706';
      else tc.fillStyle = 'rgba(37,99,235,0.12)';
      tc.fill();
      tc.strokeStyle = isLast ? (conv ? '#16a34a' : '#d97706') : '#2563eb';
      tc.lineWidth = isLast ? 1.5 : 0.5;
      tc.stroke();
      tc.fillStyle = isLast ? '#fff' : '#1e293b';
      tc.font = '10px sans-serif';
      tc.textAlign = 'center';
      tc.fillText(i, n.cx, n.cy + 4);
      tc.fillStyle = '#64748b';
      tc.font = '11px sans-serif';
      tc.textAlign = 'start';
      tc.fillText('z=' + n.z.toFixed(1) + '  x=' + Math.round(n.px), n.cx + NODE_R + 6, n.cy + 4);
    });

    tc.font = '11px sans-serif'; tc.textAlign = 'start';
    tc.beginPath(); tc.arc(22, treeHeight - 28, 7, 0, Math.PI * 2);
    tc.fillStyle = 'rgba(37,99,235,0.12)'; tc.fill();
    tc.strokeStyle = '#2563eb'; tc.lineWidth = 0.5; tc.stroke();
    tc.fillStyle = '#64748b'; tc.fillText('Nodo aceptado', 35, treeHeight - 24);
    tc.beginPath(); tc.arc(160, treeHeight - 28, 7, 0, Math.PI * 2);
    tc.fillStyle = 'rgba(254,226,226,1)'; tc.fill();
    tc.strokeStyle = 'rgba(220,38,38,0.5)'; tc.lineWidth = 0.5; tc.stroke();
    tc.fillStyle = '#64748b'; tc.fillText('Nodo rechazado', 173, treeHeight - 24);
  }, []);

  // ─── Draw graph ──────────────────────────────────────────────────────────────

  const drawGraph = useCallback((positions, matrix, path, highlightBest) => {
    const canvas = graphCanvasRef.current;
    if (!canvas || positions.length === 0) return;
    const gc = canvas.getContext('2d');
    gc.clearRect(0, 0, GW, GH);
    const n = positions.length;
    const COLORS = ['#2563eb', '#d97706', '#16a34a', '#9333ea', '#e11d48', '#0891b2', '#ea580c', '#65a30d'];

    // Draw all edges
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        if (matrix[i][j] === 0) continue;
        gc.beginPath();
        gc.moveTo(positions[i].x, positions[i].y);
        gc.lineTo(positions[j].x, positions[j].y);
        gc.strokeStyle = 'rgba(148,163,184,0.35)';
        gc.lineWidth = 1;
        gc.setLineDash([]);
        gc.stroke();
        const mx = (positions[i].x + positions[j].x) / 2;
        const my = (positions[i].y + positions[j].y) / 2;
        gc.fillStyle = '#94a3b8';
        gc.font = '10px sans-serif';
        gc.textAlign = 'center';
        gc.fillText(matrix[i][j], mx, my - 4);
      }
    }

    // Draw path
    if (path && path.length > 1) {
      for (let k = 0; k < path.length - 1; k++) {
        const a = positions[path[k]], b = positions[path[k + 1]];
        gc.beginPath();
        gc.moveTo(a.x, a.y);
        gc.lineTo(b.x, b.y);
        gc.strokeStyle = highlightBest ? '#16a34a' : '#d97706';
        gc.lineWidth = 2.5;
        gc.setLineDash(highlightBest ? [] : [6, 3]);
        gc.stroke();
        gc.setLineDash([]);

        // Arrow
        const angle = Math.atan2(b.y - a.y, b.x - a.x);
        const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
        gc.beginPath();
        gc.moveTo(mx, my);
        gc.lineTo(mx - 8 * Math.cos(angle - 0.4), my - 8 * Math.sin(angle - 0.4));
        gc.moveTo(mx, my);
        gc.lineTo(mx - 8 * Math.cos(angle + 0.4), my - 8 * Math.sin(angle + 0.4));
        gc.strokeStyle = highlightBest ? '#16a34a' : '#d97706';
        gc.lineWidth = 1.5;
        gc.stroke();
      }
    }

    // Draw nodes
    positions.forEach((p, i) => {
      gc.beginPath();
      gc.arc(p.x, p.y, 18, 0, Math.PI * 2);
      gc.fillStyle = path && path.includes(i) ? COLORS[i % COLORS.length] : '#e2e8f0';
      gc.fill();
      gc.strokeStyle = COLORS[i % COLORS.length];
      gc.lineWidth = 2;
      gc.stroke();
      gc.fillStyle = path && path.includes(i) ? '#fff' : '#1e293b';
      gc.font = '13px sans-serif';
      gc.textAlign = 'center';
      gc.fillText(i, p.x, p.y + 5);
    });
  }, []);

  // ─── Generate circular positions ─────────────────────────────────────────────

  const generatePositions = useCallback((n) => {
    const cx = GW / 2, cy = GH / 2, r = Math.min(GW, GH) / 2 - 40;
    return Array.from({ length: n }, (_, i) => ({
      x: cx + r * Math.cos((2 * Math.PI * i) / n - Math.PI / 2),
      y: cy + r * Math.sin((2 * Math.PI * i) / n - Math.PI / 2),
    }));
  }, []);

  // ─── TSP Hill Climbing logic ─────────────────────────────────────────────────

  function costPath(path, matrix) {
    let cost = 0;
    for (let i = 0; i < path.length - 1; i++) cost += matrix[path[i]][path[i + 1]];
    return cost;
  }

  function generateNeighbors(path) {
    const neighbors = [];
    const n = path.length;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const copy = [...path];
        [copy[i], copy[j]] = [copy[j], copy[i]];
        neighbors.push(copy);
      }
    }
    return neighbors;
  }

  function initialSolution(n) {
    const path = Array.from({ length: n }, (_, i) => i);
    for (let i = path.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [path[i], path[j]] = [path[j], path[i]];
    }
    return path;
  }

  const runTSP = useCallback(() => {
    const matrix = graphMatrix;
    const n = matrix.length;
    const positions = generatePositions(n);
    setGraphPositions(positions);
    setTspResult(null);
    setTspLog([]);
    setTspRunning(true);

    let actual = initialSolution(n);
    let costoActual = costPath(actual, matrix);
    const log = [{ path: [...actual], cost: costoActual, type: 'initial' }];

    let iter = 0;
    const MAX_ITER = 200;

    const interval = setInterval(() => {
      if (iter >= MAX_ITER) {
        clearInterval(interval);
        setTspRunning(false);
        setTspResult({ path: actual, cost: costoActual });
        setCurrentTspPath(actual);
        setCurrentTspCost(costoActual);
        setTspLog(log);
        drawGraph(positions, matrix, actual, true);
        return;
      }

      const neighbors = generateNeighbors(actual);
      let bestNeighbor = actual;
      let bestCost = costoActual;

      for (const neighbor of neighbors) {
        const cost = costPath(neighbor, matrix);
        if (cost < bestCost) {
          bestNeighbor = neighbor;
          bestCost = cost;
        }
      }

      if (bestCost >= costoActual) {
        clearInterval(interval);
        setTspRunning(false);
        setTspResult({ path: actual, cost: costoActual });
        setCurrentTspPath(actual);
        setCurrentTspCost(costoActual);
        setTspLog(log);
        drawGraph(positions, matrix, actual, true);
        return;
      }

      actual = bestNeighbor;
      costoActual = bestCost;
      log.push({ path: [...actual], cost: costoActual, type: 'improvement' });
      iter++;

      setCurrentTspPath([...actual]);
      setCurrentTspCost(costoActual);
      setTspLog([...log]);
      drawGraph(positions, matrix, actual, false);
    }, 120);
  }, [graphMatrix, generatePositions, drawGraph]);

  // ─── Matrix helpers ───────────────────────────────────────────────────────────

  const updateMatrix = (i, j, val) => {
    const v = parseInt(val) || 0;
    const m = graphMatrix.map(r => [...r]);
    m[i][j] = v;
    m[j][i] = v;
    setGraphMatrix(m);
  };

  const resizeMatrix = (newN) => {
    const cur = graphMatrix;
    const m = Array.from({ length: newN }, (_, i) =>
      Array.from({ length: newN }, (_, j) => {
        if (i === j) return 0;
        if (i < cur.length && j < cur.length) return cur[i][j];
        return Math.floor(Math.random() * 500) + 50;
      })
    );
    setGraphMatrix(m);
    setNumNodes(newN);
    setTspResult(null);
    setTspLog([]);
    setCurrentTspPath(null);
    setCurrentTspCost(null);
    const pos = generatePositions(newN);
    setGraphPositions(pos);
    setTimeout(() => drawGraph(pos, m, null, false), 50);
  };

  // ─── Landscape step ──────────────────────────────────────────────────────────

  const doStep = useCallback(() => {
    const s = stateRef.current;
    const curZ = getElevation(s.position);
    const rPos = s.position + s.stepSize;
    const lPos = s.position - s.stepSize;
    const zRight = rPos < W ? getElevation(rPos) : -Infinity;
    const zLeft = lPos > 0 ? getElevation(lPos) : -Infinity;
    const nodeIdx = s.treeNodes.length - 1;
    let newNodes = s.treeNodes, newEdges = s.treeEdges, newPos = s.position;
    let newIter = s.iterations, newHistory = s.history, newConverged = false;

    if (zRight > curZ && zRight >= zLeft) {
      newEdges = [...newEdges, { from: nodeIdx, to: nodeIdx + 1, type: 'main' }];
      if (lPos > 0 && zLeft <= curZ) newEdges = [...newEdges, { from: nodeIdx, type: 'rejected', side: 'left', z: zLeft }];
      newPos = rPos;
      newNodes = [...newNodes, { px: newPos, z: getElevation(newPos), parent: nodeIdx }];
      newHistory = [...newHistory.slice(-24), getElevation(newPos)];
      newIter++;
    } else if (zLeft > curZ) {
      newEdges = [...newEdges, { from: nodeIdx, to: nodeIdx + 1, type: 'main' }];
      if (rPos < W && zRight <= curZ) newEdges = [...newEdges, { from: nodeIdx, type: 'rejected', side: 'right', z: zRight }];
      newPos = lPos;
      newNodes = [...newNodes, { px: newPos, z: getElevation(newPos), parent: nodeIdx }];
      newHistory = [...newHistory.slice(-24), getElevation(newPos)];
      newIter++;
    } else {
      if (lPos > 0) newEdges = [...newEdges, { from: nodeIdx, type: 'rejected', side: 'left', z: zLeft }];
      if (rPos < W) newEdges = [...newEdges, { from: nodeIdx, type: 'rejected', side: 'right', z: zRight }];
      newConverged = true;
      clearInterval(timerRef.current);
      timerRef.current = null;
      setIsRunning(false);
      setConverged(true);
      setStatus('CONVERGIDO');
    }

    stateRef.current = { ...s, position: newPos, treeNodes: newNodes, treeEdges: newEdges, iterations: newIter, history: newHistory, converged: newConverged };
    setPosition(newPos);
    setTreeNodes(newNodes);
    setTreeEdges(newEdges);
    setIterations(newIter);
    setHistory(newHistory);
    drawMain(newPos, newNodes);
    drawTree(newNodes, newEdges, newConverged);
  }, [drawMain, drawTree]);

  const toggleRun = () => {
    if (converged) { resetSim(); return; }
    if (isRunning) {
      clearInterval(timerRef.current); timerRef.current = null;
      setIsRunning(false); setStatus('PAUSADO');
    } else {
      setIsRunning(true); setStatus('EJECUTANDO');
      timerRef.current = setInterval(doStep, 60);
    }
  };

  const resetSim = () => {
    clearInterval(timerRef.current); timerRef.current = null;
    const newPos = 80 + Math.random() * 600;
    const initNodes = [{ px: newPos, z: getElevation(newPos), parent: null }];
    stateRef.current = { position: newPos, treeNodes: initNodes, treeEdges: [], iterations: 0, history: [], stepSize: stateRef.current.stepSize, converged: false };
    setPosition(newPos); setTreeNodes(initNodes); setTreeEdges([]);
    setIterations(0); setHistory([]); setConverged(false);
    setIsRunning(false); setStatus('LISTO');
    drawMain(newPos, initNodes); drawTree(initNodes, [], false);
  };

  // ─── Init ────────────────────────────────────────────────────────────────────

  useEffect(() => {
    const initPos = 150;
    const initNodes = [{ px: initPos, z: getElevation(initPos), parent: null }];
    stateRef.current.treeNodes = initNodes;
    stateRef.current.position = initPos;
    drawMain(initPos, initNodes);
    drawTree(initNodes, [], false);
    const pos = generatePositions(numNodes);
    setGraphPositions(pos);
    setTimeout(() => drawGraph(pos, graphMatrix, null, false), 80);
  }, []);

  useEffect(() => { stateRef.current.stepSize = stepSize; }, [stepSize]);

  useEffect(() => {
    if (activeTab === 'graph' && graphPositions.length > 0) {
      setTimeout(() => drawGraph(graphPositions, graphMatrix, currentTspPath, !!tspResult), 30);
    }
  }, [activeTab]);

  // ─── Styles ──────────────────────────────────────────────────────────────────

  const curZ = getElevation(position);
  const maxZ = Math.max(...history, 1);
  const statusColor = status === 'EJECUTANDO'
    ? { bg: '#dcfce7', color: '#15803d' }
    : status === 'CONVERGIDO'
    ? { bg: '#fef9c3', color: '#854d0e' }
    : { bg: '#f1f5f9', color: '#64748b' };

  const card = { background: 'white', borderRadius: '16px', padding: '16px', border: '1px solid #e2e8f0' };
  const sectionLabel = { fontSize: '11px', fontWeight: '600', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '10px' };
  const statCard = { background: '#f1f5f9', borderRadius: '12px', padding: '12px 14px' };

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", padding: '20px', backgroundColor: '#f8fafc', borderRadius: '20px', color: '#0f172a' }}>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <div style={{ fontSize: '16px', fontWeight: '600' }}>Hill Climbing Solver</div>
          <div style={{ fontSize: '12px', color: '#64748b' }}>Módulo de optimización — v3.0</div>
        </div>
        <span style={{ fontSize: '11px', fontWeight: '600', padding: '4px 12px', borderRadius: '20px', letterSpacing: '0.05em', backgroundColor: statusColor.bg, color: statusColor.color }}>
          {status}
        </span>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '4px', marginBottom: '16px', background: '#f1f5f9', padding: '4px', borderRadius: '10px', width: 'fit-content' }}>
        {[{ key: 'landscape', label: 'Paisaje continuo' }, { key: 'graph', label: 'Grafo TSP' }].map(t => (
          <button key={t.key} onClick={() => setActiveTab(t.key)} style={{
            padding: '7px 18px', borderRadius: '7px', border: 'none', fontSize: '13px', fontWeight: '500', cursor: 'pointer',
            background: activeTab === t.key ? 'white' : 'transparent',
            color: activeTab === t.key ? '#1e293b' : '#64748b',
            boxShadow: activeTab === t.key ? '0 1px 3px rgba(0,0,0,0.08)' : 'none',
          }}>{t.label}</button>
        ))}
      </div>

      {/* ── TAB: LANDSCAPE ── */}
      {activeTab === 'landscape' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 240px', gap: '16px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={card}>
              <div style={sectionLabel}>Simulación en tiempo real</div>
              <canvas ref={mainCanvasRef} width={W} height={H} style={{ width: '100%', height: 'auto', borderRadius: '8px', border: '1px solid #f1f5f9' }} />
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '12px', flexWrap: 'wrap' }}>
                <button onClick={toggleRun} style={{ background: isRunning ? '#ef4444' : '#0f172a', color: 'white', border: 'none', padding: '8px 18px', borderRadius: '8px', fontSize: '13px', fontWeight: '500', cursor: 'pointer' }}>
                  {converged ? '↺ Reiniciar' : isRunning ? '⏸ Pausar' : '▶ Iniciar'}
                </button>
                <button onClick={resetSim} style={{ background: '#f1f5f9', border: 'none', padding: '8px 14px', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' }}>
                  ↺ Reiniciar
                </button>
                <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#64748b' }}>
                  <span>Paso</span>
                  <input type="range" min="1" max="10" value={stepSize} onChange={e => setStepSize(+e.target.value)} style={{ width: '80px' }} />
                  <span>{stepSize}</span>
                </div>
              </div>
            </div>

            <div style={card}>
              <div style={sectionLabel}>Árbol de iteraciones</div>
              <div style={{ overflowY: 'auto', maxHeight: '400px' }}>
                <canvas ref={treeCanvasRef} width={TW} height={360} style={{ width: '100%', display: 'block' }} />
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[{ label: 'Altura Z', value: curZ.toFixed(2) }, { label: 'Posición X', value: Math.round(position) + 'px' }, { label: 'Iteraciones', value: iterations }].map(s => (
              <div key={s.label} style={statCard}>
                <div style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>{s.label}</div>
                <div style={{ fontSize: '22px', fontWeight: '600', color: '#1e293b' }}>{s.value}</div>
              </div>
            ))}

            <div style={{ background: '#0f172a', borderRadius: '12px', padding: '12px 14px' }}>
              <div style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>Convergencia</div>
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '2px', height: '50px' }}>
                {history.map((h, i) => (
                  <div key={i} style={{ flex: 1, background: '#38bdf8', borderRadius: '2px 2px 0 0', height: Math.max(2, (h / maxZ) * 48) + 'px', opacity: 0.7 }} />
                ))}
              </div>
            </div>

            <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '12px', padding: '10px 12px', fontSize: '12px', color: '#1e40af', lineHeight: '1.6' }}>
              El agente evalúa X+paso y X−paso, moviéndose hacia el mayor valor. Se detiene al no encontrar mejora (óptimo local).
            </div>
          </div>
        </div>
      )}

      {/* ── TAB: GRAPH TSP ── */}
      {activeTab === 'graph' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: '16px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>

            {/* Matrix editor */}
            <div style={card}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div style={sectionLabel}>Matriz de costos</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#64748b' }}>
                  <span>Nodos</span>
                  {[3, 4, 5, 6].map(n => (
                    <button key={n} onClick={() => resizeMatrix(n)} style={{
                      width: '28px', height: '28px', borderRadius: '6px', border: '1px solid #e2e8f0',
                      background: numNodes === n ? '#0f172a' : 'white',
                      color: numNodes === n ? 'white' : '#64748b',
                      fontSize: '12px', cursor: 'pointer', fontWeight: '500',
                    }}>{n}</button>
                  ))}
                </div>
              </div>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ borderCollapse: 'collapse', fontSize: '12px' }}>
                  <thead>
                    <tr>
                      <th style={{ width: '28px' }}></th>
                      {Array.from({ length: numNodes }, (_, j) => (
                        <th key={j} style={{ padding: '4px 8px', color: '#64748b', fontWeight: '500', textAlign: 'center' }}>N{j}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {graphMatrix.map((row, i) => (
                      <tr key={i}>
                        <td style={{ padding: '4px 8px', color: '#64748b', fontWeight: '500', textAlign: 'center' }}>N{i}</td>
                        {row.map((val, j) => (
                          <td key={j} style={{ padding: '2px' }}>
                            {i === j ? (
                              <div style={{ width: '52px', height: '28px', background: '#f8fafc', borderRadius: '6px', border: '1px solid #f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#cbd5e1', fontSize: '12px' }}>—</div>
                            ) : (
                              <input
                                type="number"
                                value={editingCell === `${i}-${j}` ? undefined : val}
                                defaultValue={val}
                                onFocus={() => setEditingCell(`${i}-${j}`)}
                                onBlur={e => { updateMatrix(i, j, e.target.value); setEditingCell(null); }}
                                onChange={e => { if (editingCell === `${i}-${j}`) updateMatrix(i, j, e.target.value); }}
                                style={{ width: '52px', height: '28px', border: '1px solid #e2e8f0', borderRadius: '6px', textAlign: 'center', fontSize: '12px', background: 'white', color: '#1e293b', outline: 'none' }}
                              />
                            )}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Graph canvas */}
            <div style={card}>
              <div style={sectionLabel}>Visualización del grafo</div>
              <canvas ref={graphCanvasRef} width={GW} height={GH} style={{ width: '100%', height: 'auto', borderRadius: '8px', border: '1px solid #f1f5f9', background: '#fafafa' }} />
              <div style={{ display: 'flex', gap: '10px', marginTop: '12px' }}>
                <button onClick={runTSP} disabled={tspRunning} style={{
                  background: tspRunning ? '#94a3b8' : '#0f172a', color: 'white', border: 'none',
                  padding: '8px 20px', borderRadius: '8px', fontSize: '13px', fontWeight: '500',
                  cursor: tspRunning ? 'not-allowed' : 'pointer',
                }}>
                  {tspRunning ? '⏳ Ejecutando...' : '▶ Ejecutar Hill Climbing'}
                </button>
                <button onClick={() => {
                  setTspResult(null); setTspLog([]); setCurrentTspPath(null); setCurrentTspCost(null);
                  const pos = generatePositions(numNodes);
                  setGraphPositions(pos);
                  setTimeout(() => drawGraph(pos, graphMatrix, null, false), 30);
                }} style={{ background: '#f1f5f9', border: 'none', padding: '8px 14px', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' }}>
                  ↺ Limpiar
                </button>
              </div>
            </div>
          </div>

          {/* Right panel */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>

            {currentTspPath && (
              <>
                <div style={statCard}>
                  <div style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Costo actual</div>
                  <div style={{ fontSize: '22px', fontWeight: '600', color: tspResult ? '#16a34a' : '#d97706' }}>{currentTspCost}</div>
                </div>
                <div style={statCard}>
                  <div style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px' }}>Ruta actual</div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {currentTspPath.map((n, i) => (
                      <React.Fragment key={i}>
                        <span style={{ background: '#e0e7ff', color: '#3730a3', borderRadius: '6px', padding: '3px 8px', fontSize: '12px', fontWeight: '500' }}>N{n}</span>
                        {i < currentTspPath.length - 1 && <span style={{ color: '#94a3b8', fontSize: '12px', lineHeight: '24px' }}>→</span>}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              </>
            )}

            {tspResult && (
              <div style={{ background: '#f0fdf4', border: '1px solid #86efac', borderRadius: '12px', padding: '12px 14px' }}>
                <div style={{ fontSize: '11px', color: '#15803d', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px' }}>✓ Solución óptima local</div>
                <div style={{ fontSize: '20px', fontWeight: '600', color: '#15803d', marginBottom: '6px' }}>{tspResult.cost}</div>
                <div style={{ fontSize: '12px', color: '#166534' }}>
                  Ruta: {tspResult.path.map(n => 'N' + n).join(' → ')}
                </div>
              </div>
            )}

            {/* Log */}
            <div style={{ ...card, flex: 1, overflow: 'hidden' }}>
              <div style={sectionLabel}>Log de iteraciones</div>
              <div style={{ overflowY: 'auto', maxHeight: '320px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {tspLog.length === 0 && (
                  <div style={{ fontSize: '12px', color: '#94a3b8', textAlign: 'center', padding: '20px 0' }}>
                    Ejecuta el algoritmo para ver el log
                  </div>
                )}
                {tspLog.map((entry, i) => (
                  <div key={i} style={{
                    background: entry.type === 'initial' ? '#f1f5f9' : '#f0fdf4',
                    border: `1px solid ${entry.type === 'initial' ? '#e2e8f0' : '#86efac'}`,
                    borderRadius: '8px', padding: '7px 10px',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '11px', fontWeight: '600', color: entry.type === 'initial' ? '#64748b' : '#15803d' }}>
                        {entry.type === 'initial' ? 'Inicial' : `Mejora #${i}`}
                      </span>
                      <span style={{ fontSize: '12px', fontWeight: '600', color: '#1e293b' }}>costo {entry.cost}</span>
                    </div>
                    <div style={{ fontSize: '11px', color: '#64748b', marginTop: '2px' }}>
                      {entry.path.map(n => 'N' + n).join(' → ')}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '12px', padding: '10px 12px', fontSize: '12px', color: '#1e40af', lineHeight: '1.6' }}>
              Genera vecinos intercambiando pares de nodos (swap). Se mueve al vecino de menor costo hasta no encontrar mejora.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}