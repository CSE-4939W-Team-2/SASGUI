import { RecoilState, useRecoilState,  useSetRecoilState } from "recoil";
import { csvCurve, csvCurveData, csvFile, csvFileName} from "./CSVFileReader";
import { jsonToCSV } from "react-papaparse";
import { useRef, useState } from "react";
import { sliderObj } from "./Page";
import { sphereSliders } from "../atoms/sphereTemplate";
import { coreShellSphereSliders } from "../atoms/coreShellSphereTemplate";
import { cylinderSliders } from "../atoms/cylinderTemplate";
import { coreShellCylinderSliders } from "../atoms/coreShellCylinderTemplate";
import { diskSliders } from "../atoms/diskTemplate";
import { coreShellDiskSliders } from "../atoms/coreShellDiskTemplate";
import { currentMorphology, saveLoad } from "../atoms/morphologyTemplate";
import { useNavigate } from "react-router-dom";
import Modal from 'react-modal';
const customStyles = {
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
    },
  };
Modal.setAppElement("#root")
export default function LoadRemote() {
    const inputRef = useRef<HTMLInputElement>(null);//Used for file upload
    const [file, setFile] = useRecoilState(csvFile);//Setter for the csv file state
    const setCurve = useSetRecoilState(csvCurve);//Holds the csv curve data for the graph
    const setFileName = useSetRecoilState(csvFileName);//CSV file name
    const [morphology, setMorphology] = useRecoilState(currentMorphology)//Current morphology
    const navigate = useNavigate();
    const [modalIsOpen, setIsOpen] = useState(false);
    const [saveNames, setSaveNames] = useState<string[]>([]);
    const [selectedSave, setSelectedSave] = useState<string>("noSaves")
    //Below objects grab the setter functions for each morphology's data points
    const openModal = () =>{
        setIsOpen(true);
    }
    const afterOpenModal =()=> {
        
    }
    const closeModal = () => {
        setIsOpen(false);
    }
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
    const handleLoading = (parsedData:saveLoad) => {
        try {
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
        } catch (error) {
            console.error("Error parsing JSON:", error);
            alert("Error loading save")
        }
    };
    const handleLoad = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        fetch(`http://http://sasgui.cse.uconn.edu:5000/get_user_scans?userId=${1}`, {//Make the request
            method: 'GET',
            mode:'cors',//For CORSs
            headers: {
              "Access-Control-Allow-Origin":"*"//For CORS
            }
          }).then(response => response.json()).then(data=>{
            console.log("Success: ", data.message);
            setSaveNames(data.scans)
            openModal()
        }
          )
          .catch(error => {
            console.error('Error:', error);
            alert("Error getting file names")
          })
    }
    const handleSelectSave = (event: React.ChangeEvent<HTMLSelectElement>) => {
        console.log(event.target.value)
        setSelectedSave(event.target.value)
    }
    const handleLoadScanButton = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault()

        fetch(`http://http://sasgui.cse.uconn.edu:5000/get_scan_data?userId=${1}&name=${selectedSave}`, {//Make the request
            method: 'GET',
            mode:'cors',//For CORSs
            headers: {
              "Access-Control-Allow-Origin":"*"//For CORS
            }
          }).then(response => response.json()).then(data=>{
            console.log("Success: ", data.message);
            console.log(data.data.fileData);
            handleLoading(data.data.fileData);
            closeModal()
        }
          )
          .catch(error => {
            console.error('Error:', error);
            alert("Error getting file names")
          })
    }
    return(
        <div>
            <button style={{width:"150px", height:"80px"}} onClick={handleLoad}>Load Remote</button>
            <Modal
            isOpen={modalIsOpen}
            onAfterOpen={afterOpenModal}
            onRequestClose={closeModal}
            style={customStyles}
            contentLabel="Example Modal">
                <h2>Select a scan from the dropdown menu</h2>
                <button onClick={closeModal}>Cancel</button>
                <form>
                    <select name="saves" style={{height:"50px", backgroundColor:"#E1B6B0", borderRadius:"5px"}} onChange={handleSelectSave}
                                value={selectedSave}>
                                    <option value="noSaves" disabled hidden>Select a Save</option>
                                    {saveNames?.map((save:string, i)=>{
                                        //Maps the values in morphologyValues from morphologyTemplate
                                        return(
                                            <option key={i} value={save}>{save}</option>
                                        )
                                    })}
                                </select>
                    <button onClick={handleLoadScanButton}>Load Scan</button>
                    {/*<button>Delete Scan Scan</button>*/}
                </form>
            </Modal>
        </div>
    )
}