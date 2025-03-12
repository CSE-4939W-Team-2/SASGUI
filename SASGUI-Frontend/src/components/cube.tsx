import * as THREE from 'three';
import { useRef, useState, useEffect } from 'react';
import { useFrame, ThreeElements } from '@react-three/fiber';
import { cylinderLength, cylinderRadius } from '../atoms/cylinderTemplate';
import { sphereRadius } from '../atoms/sphereTemplate';
import { useRecoilValue } from 'recoil';

interface BoxProps extends Omit<ThreeElements['mesh'], 'children'> {
  shapeType: string;  // Ensuring it's a plain string
}

export function Box({ shapeType, ...props }: BoxProps) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const [sphradius, setSphRadius] = useState(1);
  const [cylradius, setCylRadius] = useState(1);
  const [length, setLength] = useState(1);
  const sphRadius = useRecoilValue(sphereRadius);
  const cylRadius = useRecoilValue(cylinderRadius);
  const cylLength = useRecoilValue(cylinderLength);

  useEffect(() => {
    setCylRadius(cylRadius / 800);
    setSphRadius(sphRadius / 800);
    setLength(cylLength / 800);
  }, [cylRadius, cylLength, sphRadius]);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });

  let geometry;
  switch (shapeType) {
    case 'sphere':
      geometry = (
        <mesh>
          <sphereGeometry args={[sphradius, 32, 32]} />
          <meshStandardMaterial color={'#ff5733'} />
        </mesh>
      );
      break;
    case 'core-shell-sphere':
      geometry = (
        <>
          <mesh>
            <sphereGeometry args={[sphradius * 0.8, 32, 32]} />
            <meshStandardMaterial color={'#ffcc00'} />
          </mesh>
          <mesh>
            <sphereGeometry args={[sphradius, 32, 32]} />
            <meshStandardMaterial color={'#ff5733'} wireframe />
          </mesh>
        </>
      );
      break;
    case 'cylinder':
      geometry = (
        <mesh>
          <cylinderGeometry args={[cylradius, cylradius, length, 32]} />
          <meshStandardMaterial color={'#33ff57'} />
        </mesh>
      );
      break;
    case 'core-shell-cylinder':
      geometry = (
        <>
          <mesh>
            <cylinderGeometry args={[cylradius * 0.8, cylradius * 0.8, length, 32]} />
            <meshStandardMaterial color={'#ffcc00'} />
          </mesh>
          <mesh>
            <cylinderGeometry args={[cylradius, cylradius, length, 32]} />
            <meshStandardMaterial color={'#33ff57'} wireframe />
          </mesh>
        </>
      );
      break;
    case 'disk':
      geometry = (
        <mesh>
          <cylinderGeometry args={[cylradius, cylradius, 0.1, 32]} />
          <meshStandardMaterial color={'#3380ff'} />
        </mesh>
      );
      break;
    case 'core-shell-disk':
      geometry = (
        <>
          <mesh>
            <cylinderGeometry args={[cylradius * 0.8, cylradius * 0.8, 0.1, 32]} />
            <meshStandardMaterial color={'#ffcc00'} />
          </mesh>
          <mesh>
            <cylinderGeometry args={[cylradius, cylradius, 0.1, 32]} />
            <meshStandardMaterial color={'#3380ff'} wireframe />
          </mesh>
        </>
      );
      break;
    default:
      console.warn(`Invalid shapeType received: ${shapeType}`);
      return null;
  }

  return (
    <mesh {...props} ref={meshRef} scale={1.5}>
      {geometry}
    </mesh>
  );
}