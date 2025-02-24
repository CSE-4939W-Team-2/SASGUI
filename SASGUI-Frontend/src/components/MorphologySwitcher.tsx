import { useLocation, useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import { currentMorphology, morphologyType, morphologyValues } from "../atoms/morphologyTemplate";
import { useEffect } from "react";
export default function MorphologySwitcher() {
    const navigate = useNavigate();
    const [morphology, setMorphology] = useRecoilState(currentMorphology); //Grab morphology state
    const handleSwitch = (event: React.ChangeEvent<HTMLSelectElement>) => { //Handle user selecting from the dropdown
        setMorphology(event.target.value);
        navigate(`${event.target.value}`); //Set browser route
    }
    const location = useLocation();
    const currentRoute = location.pathname;
    //If navigating directly to a morphology page, make sure morphology state gets set correctly
    useEffect(() => {
        const currentRoute = location.pathname; //Get current route
        if (currentRoute !== morphology){ //If current route is not the same as morphology, set the state
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
                    //Maps the values in morphologyValues from morphologyTemplate
                    return(
                        <option key={i} value={morph.value}>{morph.text}</option>
                    )
                })}
            </select>
        </div>
    )
}