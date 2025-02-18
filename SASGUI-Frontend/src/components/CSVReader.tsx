/*import{ CSSProperties} from 'react';

import { useCSVReader } from 'react-papaparse';
import { atom, useRecoilState } from 'recoil';


const styles = {
  csvReader: {
    display: 'flex',
    flexDirection: 'row',
    marginBottom: 10,
  } as CSSProperties,
  browseFile: {
    width: '100%',
    marginRight:'5px',
    height:"70px"
  } as CSSProperties,
  remove: {
    padding: '0 20px',
    width: "100%"
  } as CSSProperties,
};

export interface csvCurveData {name:String, I:number, q:number};

export const csvCurve = atom({
  key: 'csvCurveData',
  default: [] as csvCurveData[]
});

export default function CSVReader() {
  const [curve, setCurve] = useRecoilState(csvCurve);
  const { CSVReader } = useCSVReader();
  const element = document.getElementById("remover");
  if(element?.getAttribute("clearListener")!=="true"){
    element?.addEventListener("click", clearCurve);
    element?.setAttribute("clearListener", "true");
  }
  function clearCurve(){
    console.log(curve);
    setCurve([]);
  }
  return (
    <CSVReader
      onUploadAccepted={(results: any) => {
        console.log(results);
        if(results?.data !== null) {
          let resCurve = results?.data.map((x: string[]) => {return {
          name: x[0],
          I: parseFloat(x[1]),
          q: parseFloat(x[2])
          }})
          resCurve = resCurve.filter((x:{name:String, I:number, q:number}) => (!Number.isNaN(x.I) && typeof x.I !== 'string') || (!Number.isNaN(x.q) && typeof x.q !== 'string'))
          setCurve(resCurve)
          console.log(resCurve)
        }
        }
      }
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
}*/