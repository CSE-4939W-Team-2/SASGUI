import { useRecoilValue } from 'recoil'
import Page, { sliderObj } from '../components/Page'
import { sphereSliders } from '../atoms/sphereTemplate'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { coreShellSphereSliders } from '../atoms/coreShellSphereTemplate';
import { cylinderSliders } from '../atoms/cylinderTemplate';
import { coreShellCylinderSliders } from '../atoms/coreShellCylinderTemplate';
import { diskSliders } from '../atoms/diskTemplate';
import { coreShellDiskSliders } from '../atoms/coreShellDiskTemplate';
import { currentMorphology } from '../atoms/morphologyTemplate';
import { useEffect } from 'react';
export default function Wrapper() {
    const morphology = useRecoilValue(currentMorphology);
    const sphereData:any = {morphology:"Sphere"}
    sphereSliders.map((slider:sliderObj)=>{
        sphereData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    const coreShellSphereData:any = {morphology:"CoreShellSphere"}
    coreShellSphereSliders.map((slider:sliderObj)=>{
        coreShellSphereData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    const cylinderData:any = {morphology:"Cylinder"}
    cylinderSliders.map((slider:sliderObj)=>{
        cylinderData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    const coreShellCylinderData:any = {morphology:"CoreShellCylinder"}
    coreShellCylinderSliders.map((slider:sliderObj)=>{
        coreShellCylinderData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    const diskData:any = {morphology:"Disk"}
    diskSliders.map((slider:sliderObj)=>{
        diskData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    const coreShellDiskData:any = {morphology:"CoreShellDisk"}
    coreShellDiskSliders.map((slider:sliderObj)=>{
        coreShellDiskData[slider.atomic.key] = useRecoilValue(slider.atomic)
    })
    useEffect(()=>{
        let data = null
        switch (morphology){
            case "/sphere":
                data = sphereData
                break;
            case "/coreShellSphere":
                data = coreShellSphereData
                break;
            case "/cylinder":
                data = cylinderData
                break;
            case "/coreShellCylinder":
                data = coreShellCylinderData
                break;
            case "/disk":
                data = diskData
                break;
            case "/coreShellDisk":
                data = coreShellDiskData
                break;
            default:
                console.error("Not a valid morphology")
        }
        if(data!==null){
            fetch('http://localhost:5000/simulate_graph',{
                method: 'POST',
                mode:'cors',//For CORSs
                body: JSON.stringify(data),
                headers: {
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin":"*"//For CORS
                }
            }).then(response => response.json())
            .then(data => {
              console.log('Success:', data);
            })
            .catch(error => {
              console.error('Error:', error);
            });
        }
        
    },[morphology, sphereData, coreShellSphereData, coreShellCylinderData, cylinderData, coreShellDiskData, diskData])
    return(
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
    )
}