import { useLocation, useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import { currentMorphology, morphologyType, morphologyValues } from "../atoms/morphologyTemplate";
import { useEffect } from "react";
export default function MorphologySwitcher() {
    const navigate = useNavigate();
    const [morphology, setMorphology] = useRecoilState(currentMorphology);
    const handleSwitch = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setMorphology(event.target.value);
        navigate(`${event.target.value}`);
    }
    const location = useLocation();
    const currentRoute = location.pathname;
    //If navigating directly to a morphology page, make sure morphology state gets set
    useEffect(() => {
        const currentRoute = location.pathname;
        if (currentRoute !== morphology){
            setMorphology(currentRoute);
        }
    },[])
    return(
        <div style={{display:"flex", flexDirection:"row", marginBottom:"10px", alignItems:"center", marginRight:"100px"}}>
            <p>Select a Morphology: </p>
            <select name="morphologies" style={{height:"50px", backgroundColor:"#E1B6B0", borderRadius:"5px"}} onChange={handleSwitch}
            defaultValue={currentRoute}>
                <option value="/" disabled hidden>Choose here</option>
                {morphologyValues.map((morph:morphologyType, i)=>{
                    return(
                        <option key={i} value={morph.value}>{morph.text}</option>
                    )
                })}
            </select>
        </div>
    )
}