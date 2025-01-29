import React from 'react';
import{ CSSProperties} from 'react';

import { useCSVReader } from 'react-papaparse';

export interface Props{
  curve: {name:String, I:number, q:number}[],
  setCurve: React.Dispatch<React.SetStateAction<{name:String, I:number, q:number}[]>>
}

const styles = {
  csvReader: {
    display: 'flex',
    flexDirection: 'row',
    marginBottom: 10,
  } as CSSProperties,
  browseFile: {
    width: '100%',
  } as CSSProperties,
  remove: {
    padding: '0 20px',
    width: "100%"
  } as CSSProperties,
};

export default function CSVReader(props:Props) {
  const { CSVReader } = useCSVReader();
  const element = document.getElementById("remover");
  if(element?.getAttribute("clearListener")!=="true"){
    element?.addEventListener("click", clearCurve);
    element?.setAttribute("clearListener", "true");
  }
  
  function clearCurve(){
    props.setCurve([]);
  }
  return (
    <CSVReader
      onUploadAccepted={(results: any) => {
        console.log(results);
        if(results?.data !== null) props.setCurve(results?.data.slice(1).map((x: string[]) => {return {
          name: x[0],
          I: parseFloat(x[1]),
          q: parseFloat(x[2])
        }}));
      }}
    >
      {({
        getRootProps,
        getRemoveFileProps,
        acceptedFile
      }: any) => (
        <>
          <div style={styles.csvReader}>
            <button type='button' {...getRootProps()} style={styles.browseFile}>
              {acceptedFile&&acceptedFile.name? acceptedFile.name : "Upload Curve"}
            </button>
            <button {...getRemoveFileProps()} style={styles.remove} id="remover">
              Clear Input Curve
            </button>
          </div>
        </>
      )}
    </CSVReader>
  );
}