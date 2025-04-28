// Import necessary libraries and hooks
import * as THREE from 'three'; // Three.js for 3D objects
import { useRef, useState, useEffect } from 'react'; // React hooks
import { useFrame, ThreeElements } from '@react-three/fiber'; // React Three Fiber utilities

// Import Recoil atoms for different shapes' parameters
import { cylinderLength, cylinderRadius } from '../atoms/cylinderTemplate';
import { sphereRadius } from '../atoms/sphereTemplate';
import { diskLength, diskRadius } from '../atoms/diskTemplate';
import { coreShellCylinderLength, coreShellCylinderRadius, coreShellCylinderThickness } from '../atoms/coreShellCylinderTemplate';
import { coreShellSphereRadius, coreShellSphereThickness } from '../atoms/coreShellSphereTemplate';
import { coreShellDiskLength, coreShellDiskRadius, coreShellDiskThickness } from '../atoms/coreShellDiskTemplate';
import { useRecoilValue } from 'recoil';

// Interface for props, extending basic mesh props and adding 'shapeType'
interface BoxProps extends Omit<ThreeElements['mesh'], 'children'> {
  shapeType: string; // The type of shape to render
}

// The main Box component
export function Box({ shapeType, ...props }: BoxProps) {
  const meshRef = useRef<THREE.Mesh>(null!); // Reference to the mesh for rotation
  const [sphradius, setSphRadius] = useState(1);
  const [cylradius, setCylRadius] = useState(1);
  const [diskradius, setDiskRadius] = useState(1);
  const [disklength, setDiskLength] = useState(1);
  const [length, setLength] = useState(1);
  const [coreshellsphradius, setCoreSphereRadius] = useState(1);
  const [coreshellsphthickness, setCoreSphereThickness] = useState(1);
  const [coreshellcylradius, setCoreCylRadius] = useState(1);
  const [coreshellcyllength, setCoreCylLength] = useState(1);
  const [coreshellcylthickness, setCoreCylThickness] = useState(1);
  const [coreshelldskradius, setCoreDiskRadius] = useState(1);
  const [coreshelldsklength, setCoreDiskLength] = useState(1);
  const [coreshelldskthickness, setCoreDiskThickness] = useState(1);

  // Get values from Recoil global state
  const sphRadius = useRecoilValue(sphereRadius);
  const cylRadius = useRecoilValue(cylinderRadius);
  const cylLength = useRecoilValue(cylinderLength);
  const dskLength = useRecoilValue(diskLength);
  const dskRadius = useRecoilValue(diskRadius);

  const coreShellSphRadius = useRecoilValue(coreShellSphereRadius);
  const coreShellSphThickness = useRecoilValue(coreShellSphereThickness);
  const coreShellCylRadius = useRecoilValue(coreShellCylinderRadius);
  const coreShellCylLength = useRecoilValue(coreShellCylinderLength);
  const coreShellCylThickness = useRecoilValue(coreShellCylinderThickness);
  const coreShellDskRadius = useRecoilValue(coreShellDiskRadius);
  const coreShellDskLength = useRecoilValue(coreShellDiskLength);
  const coreShellDskThickness = useRecoilValue(coreShellDiskThickness);

  // Whenever any shape parameter updates, rescale them (divided by 800 for scene fitting)
  useEffect(() => {
    setCylRadius(cylRadius / 800);
    setSphRadius(sphRadius / 800);
    setDiskRadius(dskRadius / 800);
    setDiskLength(dskLength / 800);
    setLength(cylLength / 800);
    setCoreCylRadius(coreShellCylRadius / 800);
    setCoreCylThickness(coreShellCylThickness / 800);
    setCoreCylLength(coreShellCylLength / 800);
    setCoreDiskThickness(coreShellDskThickness / 800);
    setCoreDiskRadius(coreShellDskRadius / 800);
    setCoreDiskLength(coreShellDskLength / 800);
    setCoreSphereThickness(coreShellSphThickness / 800);
    setCoreSphereRadius(coreShellSphRadius / 800);
  }, [
    cylRadius, cylLength, sphRadius, dskRadius, dskLength, 
    coreShellSphRadius, coreShellSphThickness,
    coreShellCylRadius, coreShellCylLength, coreShellCylThickness,
    coreShellDskRadius, coreShellDskLength, coreShellDskThickness
  ]);

  // Continuously rotate the mesh for better visualization
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });

  // Variable to hold the selected geometry
  let geometry;

  // Switch based on shapeType to choose which object to render
  //
  // add another shape to the function for example cone:
  // add the following to the switch statement:
  //case 'cone':
  //    geometry = (
  //      <mesh>
  //        <coneGeometry args={[coneradius, coneradius, length, 32]} />
  //        <meshStandardMaterial color={'blue'} />
  //      </mesh>
  //    );
  //    break;
  switch (shapeType) {
    case 'sphere':
      geometry = (
        <mesh>
          <sphereGeometry args={[sphradius, 32, 32]} />
          <meshStandardMaterial color={'red'} />
        </mesh>
      );
      break;
    case 'coreShellSphere':
      geometry = (
        <>
          {/* Core sphere */}
          <mesh position={[0, 0, 0]}>
            <sphereGeometry args={[coreshellsphradius, 32, 32]} />
            <meshStandardMaterial color="red" />
          </mesh>
          {/* Transparent shell */}
          <mesh position={[0, 0, 0]}>
            <sphereGeometry args={[coreshellsphradius + coreshellsphthickness, 32, 32]} />
            <meshStandardMaterial color="purple" transparent={true} opacity={0.3} />
          </mesh>
        </>
      );
      break;
    case 'cylinder':
      geometry = (
        <mesh>
          <cylinderGeometry args={[cylradius, cylradius, length, 32]} />
          <meshStandardMaterial color={'blue'} />
        </mesh>
      );
      break;
    case 'coreShellCylinder':
      geometry = (
        <>
          {/* Core cylinder */}
          <mesh position={[0, 0, 0]}>
            <cylinderGeometry args={[coreshellcylradius, coreshellcylradius, coreshellcyllength, 32]} />
            <meshStandardMaterial color="blue" />
          </mesh>
          {/* Transparent shell */}
          <mesh position={[0, 0, 0]} scale={[1, 1.01, 1]}>
            <cylinderGeometry args={[coreshellcylradius + coreshellcylthickness, coreshellcylradius + coreshellcylthickness, coreshellcyllength, 32]} />
            <meshStandardMaterial color="green" transparent={true} opacity={0.3} />
          </mesh>
        </>
      );
      break;
    case 'disk':
      geometry = (
        <mesh>
          <cylinderGeometry args={[diskradius, diskradius, disklength, 32]} />
          <meshStandardMaterial color={'green'} />
        </mesh>
      );
      break;
    case 'coreShellDisk':
      geometry = (
        <>
          {/* Core disk */}
          <mesh position={[0, 0, 0]}>
            <cylinderGeometry args={[coreshelldskradius, coreshelldskradius, coreshelldsklength, 32]} />
            <meshStandardMaterial color="green" />
          </mesh>
          {/* Transparent shell */}
          <mesh position={[0, 0, 0]} scale={[1, 1.01, 1]}>
            <cylinderGeometry args={[coreshelldskradius + coreshelldskthickness, coreshelldskradius + coreshelldskthickness, coreshelldsklength, 32]} />
            <meshStandardMaterial color="orange" transparent={true} opacity={0.3} />
          </mesh>
        </>
      );
      break;
    default:
      console.log("Unknown shape type", shapeType);
  }

  return (
    <mesh {...props} ref={meshRef} scale={1.5}>
      {geometry}
    </mesh> 
  );
}
