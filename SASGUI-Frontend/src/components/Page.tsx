// Import components used in this page
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

// Import React and Recoil utilities
import { RecoilState, useRecoilValue } from "recoil";
import { useEffect } from "react";

// Import Canvas for 3D rendering
import { Canvas } from "@react-three/fiber";
import { Box } from "./cube.js"; // 3D box/cube component

// Import Recoil atom for morphology selection
import { currentMorphology } from "../atoms/morphologyTemplate.js";
// Import static image
import FinalRuler from "../assets/FinalRuler.png";

// Define the expected structure of a slider object
export interface sliderObj {
    label: string,
    minVal: number,
    maxVal: number,
    step: number,
    atomic: RecoilState<number>,
    predicted: boolean
}

// Define the props this Page component will receive
interface Props {
    sliderArray: sliderObj[],
    title: string
}

// Main Page component
export default function Page(props: Props) {
    // Get the current morphology state from Recoil
    const morphology = useRecoilValue(currentMorphology);

    // Update the document title whenever the prop `title` changes
    useEffect(() => {
        document.title = props.title;
    }, [props.title]);

    return (
        <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
            
            {/* Top bar: Morphology switcher, performance toggle, CSV upload, ML button */}
            <div style={{ display: "flex", justifyContent: "right" }}>
                <MorphologySwitcher />
                <div style={{ display: "flex", flexDirection: "column", marginRight: "20px" }}>
                    <PerformanceToggle />
                    <CSVFileReader />
                </div>
                <MLButton />
            </div>

            {/* Save/Load controls and Chart area */}
            <div style={{ display: "flex" }}>
                <div style={{ display: "flex", flexDirection: "column", marginRight: "5px" }}>
                    <SaveLocal />
                    <SaveRemote />
                    <LoadLocal />
                    <LoadRemote />
                </div>
                <Charter />
            </div>
            
            {/* Sliders, 3D visualization, and ruler image */}
            <div style={{ display: "flex", flexDirection: "row" }}>
                
                {/* Parameter sliders */}
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "50% 50%",
                    gap: "10px",
                    margin: "10px"
                }}>
                    {props.sliderArray.map((sliderFields: sliderObj, i) => {
                        return (
                            <ParameterSlider
                                key={i}
                                label={sliderFields.label}
                                minVal={sliderFields.minVal}
                                maxVal={sliderFields.maxVal}
                                step={sliderFields.step}
                                atomic={sliderFields.atomic}
                                predicted={sliderFields.predicted}
                            />
                        );
                    })}
                </div>

                {/* 3D Canvas for showing selected morphology shape */}
                <div style={{
                    minWidth: "0",
                    display: "flex",
                    width: "250px",
                    height: "250px",
                    marginRight: "0px",
                    alignSelf: "center"
                }}>
                    <Canvas>
                        {/* Lighting setup */}
                        <ambientLight intensity={Math.PI / 2} />
                        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
                        <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
                        
                        {/* Render Box (or other shape) based on current morphology */}
                        <Box shapeType={morphology.replace(/\//g, '')} position={[0, 0, 0]} />
                    </Canvas>
                </div>

                {/* Static ruler image */}
                <div style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    marginTop: "20px"
                }}>
                    <img
                        src={FinalRuler} // Imported image
                        alt="nanometer ruler"
                        style={{ width: "50px", height: "auto", objectFit: "contain" }}
                    />
                </div>
            </div>
            {/* Image Section */}
            <div style={{ display: morphology == "/"? "none" : "flex", justifyContent: "center", alignItems: "center", marginTop: "20px" }}>
                        <img
                            src={FinalRuler} // Using the imported path
                            alt="nanometer ruler"
                            style={{ width: "50px", height: "auto", objectFit: "contain" }}
                        />
                    </div>
        </div>
    );
}
