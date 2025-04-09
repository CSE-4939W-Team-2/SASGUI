import { useRecoilValue } from "recoil";
import { csvCurve, csvFileName } from "./CSVFileReader";
import { currentMorphology, saveLoad } from "../atoms/morphologyTemplate";
import { sphereSliders } from "../atoms/sphereTemplate";
import { sliderObj } from "./Page";
import { coreShellSphereSliders } from "../atoms/coreShellSphereTemplate";
import { coreShellCylinderSliders } from "../atoms/coreShellCylinderTemplate";
import { diskSliders } from "../atoms/diskTemplate";
import { coreShellDiskSliders } from "../atoms/coreShellDiskTemplate";
import { cylinderSliders } from "../atoms/cylinderTemplate";
import Modal from 'react-modal';
import { useState } from "react";
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
export default function SaveRemote() {
    const fileName = useRecoilValue(csvFileName);
    const curveData = useRecoilValue(csvCurve);
    const morphology = useRecoilValue(currentMorphology);
    const [modalIsOpen, setIsOpen] = useState(false);
    const [saveNames, setSaveNames] = useState<string[]>([]);
    const [selectedSave, setSelectedSave] = useState<string>("noSaves")
    const [modalInputText, setModalInputText] = useState<string>("")
    const openModal = () =>{
        setIsOpen(true);
    }
    const afterOpenModal =()=> {
        
    }
    const closeModal = () => {
        setIsOpen(false);
    }
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
        fetch(`http://localhost:5000/get_user_scans?userId=${1}`, {//Make the request
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
        setModalInputText(event.target.value)
    }
    const handleSaveScanButton = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if(modalInputText!== ""){
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
            fetch('http://localhost:5000/save_to_database', {//Make the request
                method: 'POST',
                mode:'cors',//For CORSs
                body: JSON.stringify({
                    data:JSON.stringify(jsonState),
                    userId: 1,
                    name: modalInputText
                }),
                headers: {
                  "Content-Type":"application/json",
                  "Access-Control-Allow-Origin":"*"//For CORS
                }
              })
              .then(response => response.json())
              .then(data => {
                console.log('Success:', data);
                if(data.error){
                    alert(`Error: ${data.error}`)
                }
                else alert("File Saved Successfully")
                closeModal()
              })
              .catch(error => {
                console.error('Error:', error);
              });
        }
    }
    return(
        <div>
            <Modal
            isOpen={modalIsOpen}
            onAfterOpen={afterOpenModal}
            onRequestClose={closeModal}
            style={customStyles}
            contentLabel="Example Modal">
                <h2>Select a scan to overwrite from the dropdown, or enter a new name</h2>
                <button onClick={closeModal}>Cancel</button>
                <form>
                    <input value={modalInputText} onChange={(event) => {
                        setModalInputText(event.target.value);
                        setSelectedSave("noSaves")
                        }}/>
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
                    <button onClick={handleSaveScanButton}>Save Scan</button>
                    {/*<button>Delete Scan Scan</button>*/}
                </form>
            </Modal>
            <button style={{width:"150px", height:"80px", marginBottom:"7.4px"}} onClick={handleSave}>Save Remote</button>
        </div>
    )
}