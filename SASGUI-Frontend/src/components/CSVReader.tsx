import{ CSSProperties, useEffect, useState } from 'react';

import { useCSVReader } from 'react-papaparse';

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

export default function CSVReader() {
  const { CSVReader } = useCSVReader();
  const [curve, setCurve] = useState<String[][] | null>(null);
  const element = document.getElementById("remover");
  element?.addEventListener("click", clearCurve);
  function clearCurve(){
    setCurve(null);
  }
  useEffect(()=>{
    console.log(curve)
  },[curve])
  return (
    <CSVReader
      onUploadAccepted={(results: any) => {
        console.log(results);
        if(results?.data !== null) setCurve(results?.data);
      }}
      onUploadRejected={(results: any) => {
        console.log(results);
        if(results?.data !== null) setCurve(results?.data);
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