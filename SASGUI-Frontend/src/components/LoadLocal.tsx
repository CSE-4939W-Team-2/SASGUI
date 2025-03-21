import { RecoilState, useRecoilState,  useSetRecoilState } from "recoil";
import { csvCurve, csvCurveData, csvFile, csvFileName} from "./CSVFileReader";
import { jsonToCSV } from "react-papaparse";
import { useRef } from "react";
import { sliderObj } from "./Page";
import { sphereSliders } from "../atoms/sphereTemplate";
import { coreShellSphereSliders } from "../atoms/coreShellSphereTemplate";
import { cylinderSliders } from "../atoms/cylinderTemplate";
import { coreShellCylinderSliders } from "../atoms/coreShellCylinderTemplate";
import { diskSliders } from "../atoms/diskTemplate";
import { coreShellDiskSliders } from "../atoms/coreShellDiskTemplate";
import { currentMorphology, saveLoad } from "../atoms/morphologyTemplate";
import { useNavigate } from "react-router-dom";
export default function LoadLocal() {
    const inputRef = useRef<HTMLInputElement>(null);//Used for file upload
    const [file, setFile] = useRecoilState(csvFile);//Setter for the csv file state
    const setCurve = useSetRecoilState(csvCurve);//Holds the csv curve data for the graph
    const setFileName = useSetRecoilState(csvFileName);//CSV file name
    const [morphology, setMorphology] = useRecoilState(currentMorphology)//Current morphology
    const navigate = useNavigate();
    //Below objects grab the setter functions for each morphology's data points
    const sphereSetters = sphereSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const coreShellSphereSetters = coreShellSphereSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const cylinderSetters = cylinderSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const coreShellCylinderSetters = coreShellCylinderSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const diskSetters = diskSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const coreShellDiskSetters = coreShellDiskSliders.map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const handleSave = (curveData:csvCurveData[]) => {
        const timeStamp = Date.now().toString()
        var newFile = new File([jsonToCSV(curveData)], timeStamp + ".csv", {type:'application/vnd.ms-excel'})
        setFile(newFile);
        setCurve(curveData);
        console.log(newFile);
    }
    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const loadedFile = e.target.files[0]
            const fr = new FileReader();
            fr.onload = (event) => {
                try {
                    if(event.target && typeof(event.target.result) === "string"){
                        const parsedData:saveLoad = JSON.parse(event.target.result);
                        handleSave(parsedData.curveData);
                        setFileName(parsedData.fileName);
                        setMorphology(parsedData.morphology);
                        //Grab all the data for all the sliders in all morphologies
                        parsedData.sphereData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === sphereSetters[i].atom.key){
                                sphereSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        parsedData.coreShellSphereData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === coreShellSphereSetters[i].atom.key){
                                coreShellSphereSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        parsedData.cylinderData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === cylinderSetters[i].atom.key){
                                cylinderSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        parsedData.coreShellCylinderData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === coreShellCylinderSetters[i].atom.key){
                                coreShellCylinderSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        parsedData.diskData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === diskSetters[i].atom.key){
                                diskSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        parsedData.coreShellDiskData.map((slider:{atom: RecoilState<number>, value: number}, i:number) => {
                            if(slider.atom.key === coreShellDiskSetters[i].atom.key){
                                coreShellDiskSetters[i].setter(slider.value)
                            }
                            else{
                                throw new Error("Ran into template mismatch, uploaded file does not match template")
                            }
                        })
                        navigate(parsedData.morphology);
                    }
                    else{
                        alert("Please upload a valid file")
                    }                  
                } catch (error) {
                  console.error("Error parsing JSON:", error);
                  alert("Please upload a valid file")
                }
              };
            fr.readAsText(loadedFile)
        }
    }
    function handleButtonClick(e: React.MouseEvent<HTMLButtonElement>) {
        e.preventDefault();
        if (!inputRef || !inputRef.current) return;
        inputRef.current.click();
    };
    return(
        <>
            <button style={{width:"150px", height:"80px", marginBottom:"7.4px"}} onClick={handleButtonClick}>Load Local</button>
            <input type="file" ref={inputRef} hidden onChange={handleFileChange} />
        </>
    )
}