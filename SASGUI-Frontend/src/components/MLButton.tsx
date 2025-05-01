import { useRecoilValue, useSetRecoilState } from "recoil";
import { csvCurve } from "./CSVFileReader";
import { jsonToCSV } from "react-papaparse";
import { sliderObj } from "./Page";
import { sphereSliders } from "../atoms/sphereTemplate";
import { coreShellSphereSliders } from "../atoms/coreShellSphereTemplate";
import { cylinderSliders } from "../atoms/cylinderTemplate";
import { coreShellCylinderSliders } from "../atoms/coreShellCylinderTemplate";
import { diskSliders } from "../atoms/diskTemplate";
import { coreShellDiskSliders } from "../atoms/coreShellDiskTemplate";
import { useNavigate } from "react-router-dom";
import { currentMorphology } from "../atoms/morphologyTemplate";
import { backend_link } from "../App";
export default function MLButton() {
    const navigate = useNavigate();
    const setMorphology = useSetRecoilState(currentMorphology);
    const csv = useRecoilValue(csvCurve);
    const sphereSetters = sphereSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
                return(
                {
                    atom: slider.atomic,
                    key: slider.atomic.key,
                    setter: useSetRecoilState(slider.atomic),
                })
    });
    console.log(sphereSetters)
    const coreShellSphereSetters = coreShellSphereSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                key: slider.atomic.key,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const cylinderSetters = cylinderSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                key: slider.atomic.key,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const coreShellCylinderSetters = coreShellCylinderSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                key: slider.atomic.key,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const diskSetters = diskSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                key: slider.atomic.key,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const coreShellDiskSetters = coreShellDiskSliders.filter((slider:sliderObj)=> slider.predicted === true).map((slider:sliderObj)=>{
            return(
            {
                atom: slider.atomic,
                key: slider.atomic.key,
                setter: useSetRecoilState(slider.atomic)
            })
    });
    const sendData = async () => {
        if(csv.length !== 0){//If the csv data file is not null (if it exists)
            const formData = new FormData();//Add the CSV file to the request
            const timeStamp = Date.now().toString()
            const csvData = csv.map(point => {
              return {"": point.ICsv}
            })
            var newFile = new File([jsonToCSV(csvData)], timeStamp + ".csv", {type:'application/vnd.ms-excel'})
            const renamed = new File([newFile], Date.now().toString() + ".csv", {type: "application/vnd.ms-excel"});
            formData.append('file', renamed);
            fetch(`${backend_link}/upload`, {//Make the request
                method: 'POST',
                mode:'cors',//For CORSs
                body: formData,
                headers: {
                  "Access-Control-Allow-Origin":"*"//For CORS
                }
              })
              .then(response => response.json())
              .then(data => {
                console.log('Success:', data);
                setMorphology(data.morph);
                navigate(data.morph)
                switch(data.morph){
                  case '/sphere':
                    
                    sphereSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  case '/cylinder':
                    cylinderSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  case '/disk':
                    diskSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  case '/coreShellSphere':
                    coreShellSphereSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  case '/coreShellCylinder':
                    coreShellCylinderSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  case 'coreShellDisk':
                    coreShellDiskSetters.map(setter => {
                      setter.setter(parseFloat(data[setter.key]));
                    })
                    break;
                  default:
                    console.error("Received invalid morphology from ML model")
                }
              })
              .catch(error => {
                console.error('Error:', error);
                alert("File is not of a valid format. Please see documentation for correct format")
              });
        }
        else{
            alert("Please upload a valid file")
        }
    }
    return(
            <button style={{width:"150px", height:"150px"}} onClick={() => sendData()}>Predict Morphology and Parameters</button>
    )
}