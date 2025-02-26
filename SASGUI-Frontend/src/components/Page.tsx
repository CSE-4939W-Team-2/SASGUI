import Charter from "./Charter";
import PerformanceToggle from "./PerformanceToggle";
import MLButton from "./MLButton";
import SaveLocal from "./SaveLocal";
import SaveRemote from "./SaveRemote";
import LoadLocal from "./LoadLocal";
import LoadRemote from "./LoadRemote";
import MorphologySwitcher from "./MorphologySwitcher";
import CSVFileReader from "./CSVFileReader";
import ParameterSlider from "./ParameterSlider.js";
import { RecoilState } from "recoil";
import { useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { Box } from "./cube.js";
export interface sliderObj {
    label: string,
    minVal: number,
    maxVal: number,
    step: number,
    atomic: RecoilState<number>
}
interface Props {
    sliderArray:sliderObj[],
    title: string
}
export default function Page(props:Props){
    useEffect(() => {
        document.title=props.title//Set the webpage title when it changes
    },[props.title])
    return(
    <div style={{display:"flex", flexDirection:"column", width:"100%"}}>
        <div style={{display:"flex", justifyContent:"right"}}>
            <MorphologySwitcher/>
            <div style={{display:"flex", flexDirection:"column", marginRight:"20px"}}>
                <PerformanceToggle/>
                <CSVFileReader></CSVFileReader>
            </div>
            <MLButton/>
        </div>
        <div style={{display:"flex"}}>
            <div style={{display:"flex", flexDirection:"column", marginRight:"5px"}}>
                <SaveLocal/>
                <SaveRemote/>
                <LoadLocal/>
                <LoadRemote/>
            </div>
            <Charter/>
        </div>
        
        <div style={{display:"flex", flexDirection:"row"}}>
            <div style={{
                    display:"grid",
                    gridTemplateColumns: "50% 50%",
                    gap: "10px",
                    margin: "10px"
                }}>
                {props.sliderArray.map((sliderFields:sliderObj, i)=> {
                    return(
                        <ParameterSlider key={i} label={sliderFields.label} minVal={sliderFields.minVal} maxVal={sliderFields.maxVal}
                        step={sliderFields.step} atomic={sliderFields.atomic}/>
                    )
                })}
            </div>
            <div style={{minWidth:"0", display:"flex", width:"250px", height:"250px", marginRight:"0px", alignSelf:"center"}}>
                <Canvas style={{}}>
                    <ambientLight intensity={Math.PI / 2} />
                    <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
                    <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
                    <Box position={[0, 0, 0]} />
                </Canvas>
            </div>
        </div>
    </div>)
}