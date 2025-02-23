import './App.css'
import { RecoilRoot } from 'recoil'
import Page from './components/Page'
import { sphereSliders } from './atoms/sphereTemplate'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { coreShellSphereSliders } from './atoms/coreShellSphereTemplate';
import { cylinderSliders } from './atoms/cylinderTemplate';
import { coreShellCylinderSliders } from './atoms/coreShellCylinderTemplate';
import { diskSliders } from './atoms/diskTemplate';
import { coreShellDiskSliders } from './atoms/coreShellDiskTemplate';

function App() {
  return (
    <RecoilRoot>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Page title="SASGUI" sliderArray={[]}/>}/>
          <Route path="sphere" element={<Page title="Sphere Morphology" sliderArray={sphereSliders}/>}/>
          <Route path="coreShellSphere" element={<Page title= "Core-Shell-Sphere Morphology" sliderArray={coreShellSphereSliders}/>}/>
          <Route path="Cylinder" element={<Page title= "Cylinder Morphology" sliderArray={cylinderSliders}/>}/>
          <Route path="coreShellCylinder" element={<Page title= "Core-Shell-Cylinder Morphology" sliderArray={coreShellCylinderSliders}/>}/>
          <Route path="disk" element={<Page title= "Disk Morphology" sliderArray={diskSliders}/>}/>
          <Route path="coreShellDisk" element={<Page title= "Core-Shell-Disk Morphology" sliderArray={coreShellDiskSliders}/>}/>
        </Routes>
      </BrowserRouter>
    </RecoilRoot>
  )
}

export default App
