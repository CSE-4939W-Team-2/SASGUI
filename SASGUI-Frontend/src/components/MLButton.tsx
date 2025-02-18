import { useRecoilValue } from "recoil";
import { csvFile } from "./CSVFileReader";

export default function MLButton() {
    const csv = useRecoilValue(csvFile);
    const sendData = async () => {
        if(csv !== null){
            const formData = new FormData();
            formData.append('file', csv);
            fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
              })
              .then(response => response.json())
              .then(data => {
                console.log('Success:', data);
              })
              .catch(error => {
                console.error('Error:', error);
              });
        }
        else{
            console.log("Need a file")
        }
    }
    return(
            <button style={{width:"150px", height:"150px"}} onClick={() => sendData()}>Predict Morphology and Parameters</button>
    )
}