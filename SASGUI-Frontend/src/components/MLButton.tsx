import { useRecoilValue } from "recoil";
import { csvFile } from "./CSVFileReader";

export default function MLButton() {
    const csv = useRecoilValue(csvFile);
    const sendData = async () => {
        if(csv !== null){//If the csv data file is not null (if it exists)
            const formData = new FormData();//Add the CSV file to the request
            formData.append('file', csv);
            fetch('http://localhost:5000/upload', {//Make the request
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
                console.log(csv);
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