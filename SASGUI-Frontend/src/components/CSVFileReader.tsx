import Papa from 'papaparse';
import{useRef, useState} from 'react';

import { atom, useRecoilState } from 'recoil';
//Atom that stores the csv curve data as used by the graph
export const csvCurve = atom({
  key: 'csvCurveData',
  default: [] as csvCurveData[]
});
//Atom that stores the CSV file itselt
export const csvFile = atom({
    key: 'csvFileData',
    default: null as File | null
})
export interface csvCurveData {name:String, I:number, q:number};
export default function CSVFileReader() {
    const inputRef = useRef<HTMLInputElement>(null);//Used for file upload
    const [fileName, setFileName] = useState('Upload File');//Tracks file name and puts it in the upload button
    const [file,setFile] = useRecoilState(csvFile); //State for the file
    const [curve, setCurve] = useRecoilState(csvCurve); //State for the processed csv data
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {//If file is uploaded
            setFile(e.target.files[0]);//Set file and file name
            setFileName(e.target.files[0].name);
            Papa.parse(e.target.files[0], {//Parse the files
                complete: function(results) {
                    if(results?.data !== null){
                        let resCurve = results?.data.map((x: any) => {return {//Maps the curve from string to numbers
                        name: x[0],
                        I: parseFloat(x[1]),
                        q: parseFloat(x[2])
                        }})
                        //Filter out any values that are null or invalid
                        resCurve = resCurve.filter((x:{name:String, I:number, q:number}) => (!Number.isNaN(x.I) && typeof x.I !== 'string') || (!Number.isNaN(x.q) && typeof x.q !== 'string'))
                        setCurve(resCurve)//Set the curve
                        console.log(resCurve)
                    }
        }})
    };
    }
    function handleButtonClick(e: React.MouseEvent<HTMLButtonElement>) {
        e.preventDefault();
        if (!inputRef || !inputRef.current) return;
        inputRef.current.click();
    };
    function handleClear(e: React.MouseEvent<HTMLButtonElement>){//Clear out the file
        e.preventDefault();
        setFile(null);
        setCurve([]);
        setFileName("Upload File");
    }
    return (
        <>
          <div style={{display: 'flex', flexDirection: 'row', marginBottom: "10px",}}>
            <button onClick={handleButtonClick} style={{width: '100%', marginRight:'5px', height:"70px"}}>{fileName}</button>
            <button onClick={handleClear} style={{padding: '0 20px', width: "100%"}}>Clear File</button>
            <input type="file" ref={inputRef} hidden onChange={handleFileChange} />
          </div>
        </>
    );
}