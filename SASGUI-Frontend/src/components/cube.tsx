import * as THREE from 'three'
import { useEffect, useRef, useState } from 'react'
import { useFrame, ThreeElements } from '@react-three/fiber'
import './styles.css'
import { cylinderLength, cylinderRadius } from '../atoms/cylinderTemplate'
import { useRecoilValue } from 'recoil'

export function Box(props: ThreeElements['mesh']) {
const meshRef = useRef<THREE.Mesh>(null!)
const [radius, setRadius] = useState(0);
const [length, setLength] = useState(0);
const cylRadius = useRecoilValue(cylinderRadius)
const cylLength = useRecoilValue(cylinderLength)
useFrame(() => (meshRef.current.rotation.x = 0.7))
console.log(cylRadius)
useEffect(() => {
  setRadius(cylRadius/800);
  setLength(cylLength/800)
},[cylRadius, cylLength])
return (
  <mesh
    {...props}
    ref={meshRef}
    scale={1.5}>
    <cylinderGeometry args={[radius, radius, length, 32]} />
    <meshStandardMaterial color={'#2f74c0'} />
  </mesh>
)
}


