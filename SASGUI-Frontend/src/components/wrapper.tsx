import { atom, useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil'
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
import { csvCurve } from './CSVFileReader';
export const curveWithCSVData = atom({
    key: 'curveWithCSVData',
    default: [] as curveWithCSVData[]
  });
export interface curveWithCSVData {"":String, ICsv:number, ISim:number, q:number};
export default function Wrapper() {
    const upCurve = useRecoilValue(csvCurve);
    const setCurveData = useSetRecoilState(curveWithCSVData)
    const morphology = useRecoilValue(currentMorphology);
    /*The objects and map functions below take the templates in the atoms folder and put the data contained
    by all the atoms into an object for each morphology.*/
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
        //Using a switch case, the object containing the data for the current morphology is selected
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
            case "/":
                console.log("Default page");
                break;
            default:
                console.error("Not a valid morphology")
        }
        //Send off the data
        if(data!==null){
            fetch('http://http://sasgui.cse.uconn.edu:5000/simulate_graph',{
                method: 'POST',
                mode:'cors',//For CORSs
                body: JSON.stringify(data),
                headers: {
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin":"*"//For CORS
                }
            }).then(response => response.json())
            .then(data => {
            //Validate the data, process it into the curve object, and send it off to the chart via recoil
              if(data.xval !== null && data.yval !== null){
                let resCurve = data.xval.map((x:number, i:number) => {
                    return {
                        "": i.toString(),
                        ICsv: upCurve.length===200? upCurve[i].ICsv : NaN, 
                        ISim:data.yval[i], 
                        q:data.xval[i]
                    }
                })
                if(upCurve.length!==200 && upCurve.length!==0) alert("Uploaded spectra is hidden because it is not in a valid format")
                console.log(resCurve)
                setCurveData(resCurve)
              }
            })
            .catch(error => {
              console.error('Error:', error);
            });
        }
    //dependency list contains morphology and all of the data objects. This way, whenever a data point in any morphology or the current morphology changes, the above logic runs
    },[morphology, sphereData, coreShellSphereData, coreShellCylinderData, cylinderData, coreShellDiskData, diskData, upCurve])
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