import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function OptimizationSurface() {
  const meshRef = useRef();

  // Subtle rotational animation for visualization
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005;
    }
  });

  return (
    <mesh ref={meshRef} position={[0, 0, 0]}>
      <planeGeometry args={[10, 10, 32, 32]} />
      <meshStandardMaterial color="#00ffcc" wireframe />
    </mesh>
  );
}

export default function Backtester3D() {
  return (
    <div style={{ width: '100%', height: '400px', background: '#0d1117' }}>
      <Canvas camera={{ position: [0, 5, 10], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <OptimizationSurface />
        <OrbitControls />
      </Canvas>
    </div>
  );
}
