import Charter from "./Charter";
import CSVReader from "./CSVFileReader";
import mockSlider from '../assets/mockSlider.png';
import mock3d from '../assets/mock3d.png';
import PerformanceToggle from "./PerformanceToggle";
import MLButton from "./MLButton";
import SaveLocal from "./SaveLocal";
import SaveRemote from "./SaveRemote";
import LoadLocal from "./LoadLocal";
import LoadRemote from "./LoadRemote";
import MorphologySwitcher from "./MorphologySwitcher";
import CSVFileReader from "./CSVFileReader";
export default function Page(){
    return(
    <div style={{display:"flex", flexDirection:"column"}}>
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
            <div style={{display:"flex", flexDirection: "column", marginRight:"100px"}}>
                <img src={mockSlider}/>
                <img src={mockSlider}/>
                <img src={mockSlider}/>
            </div>
            <div style={{display:"flex", flexDirection: "column", marginRight:"100px"}}>
                <img src={mockSlider}/>
                <img src={mockSlider}/>
                <img src={mockSlider}/>
            </div>
            <img src={mock3d} style={{height:"250px"}}/>
        </div>
    </div>)
}