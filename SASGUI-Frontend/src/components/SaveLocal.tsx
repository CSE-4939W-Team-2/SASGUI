import { useRecoilValue } from "recoil";
import { csvCurve, csvFileName } from "./CSVFileReader";
import { currentMorphology, saveLoad } from "../atoms/morphologyTemplate";
import { saveAs } from 'file-saver';
import { sphereSliders } from "../atoms/sphereTemplate";
import { sliderObj } from "./Page";
import { coreShellSphereSliders } from "../atoms/coreShellSphereTemplate";
import { coreShellCylinderSliders } from "../atoms/coreShellCylinderTemplate";
import { diskSliders } from "../atoms/diskTemplate";
import { coreShellDiskSliders } from "../atoms/coreShellDiskTemplate";
import { cylinderSliders } from "../atoms/cylinderTemplate";
export default function SaveLocal() {
    const fileName = useRecoilValue(csvFileName);
    const curveData = useRecoilValue(csvCurve);
    const morphology = useRecoilValue(currentMorphology);
    const sphereData = sphereSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const coreShellSphereData = coreShellSphereSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const cylinderData = cylinderSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const coreShellCylinderData = coreShellCylinderSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const diskData = diskSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const coreShellDiskData = coreShellDiskSliders.map((slider:sliderObj)=>{
        return(
        {
            atom: slider.atomic,
            value: useRecoilValue(slider.atomic)
        })
    })
    const handleSave = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        const name = prompt("Please enter a file name");
        if(name!== null){
            const jsonState:saveLoad = {
                fileName: fileName,
                curveData: curveData,
                morphology: morphology,
                sphereData: sphereData,
                coreShellSphereData: coreShellSphereData,
                cylinderData: cylinderData,
                coreShellCylinderData: coreShellCylinderData,
                diskData: diskData,
                coreShellDiskData: coreShellDiskData            
            }
            const blob = new Blob([JSON.stringify(jsonState)], {type: "text/json"})
            saveAs(blob, name + ".json");
        }
    }
    return(
            <button style={{width:"150px", height:"80px", marginBottom:"7.4px"}} onClick={handleSave}>Save Local</button>
    )
}