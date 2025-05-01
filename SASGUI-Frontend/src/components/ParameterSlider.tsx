import { useEffect, useState } from "react";
import { RecoilState, useRecoilState, useRecoilValue } from "recoil";
import { performanceMode } from "./PerformanceToggle";

interface Props {
    label: string,
    minVal: number,
    maxVal: number,
    step: number,
    atomic: RecoilState<number>,
    predicted: boolean
}
export default function ParameterSlider(props:Props){
    const [recValue, setRecValue] = useRecoilState(props.atomic);//Get the atom of state for the slider
    const [value, setValue] = useState(props.minVal)
    const perfMode = useRecoilValue(performanceMode)
    const [boxValue, setBoxValue] = useState(value.toString()); //Text box value (separate to allow correcting overflow without affecting state)
    useEffect(()=>{
        //Make sure value gets set correctly when changing pages and handle box changes
        setBoxValue(recValue.toString());
        setValue(recValue)
    },[props, recValue])
    //Handles sliders changing. Only sets the global recoil state if performance mode is off to allow constant updates to be disabled
    const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = parseFloat(event.target.value);
        setValue(newValue);
        setBoxValue(newValue.toString());
        if(!perfMode){
            setRecValue(newValue)
        }
    }
    //If in performance mode, only sets the global state when the mouse button is released. Makes performance much better in this mode
    const handlePerfModeSlider = () => {
        if(perfMode){
            setRecValue(value)
        }
    }
    //Handles and validates text entries. If they are out of bounds, sets them to the maximum bound
    const handleTextEnter = () => {
            const newValue = parseFloat(boxValue);
            if (newValue >= props.minVal){//Check if in range
                setRecValue(newValue);
            }
            else if (newValue <= props.minVal){//Value too low, set to min
                setRecValue(props.minVal);
            }
            else {//Value too high, set to max
                setRecValue(props.maxVal);
            }
    }
    //Handles text entry into the text box. Entries are validated when the user presses enter, or leaves the text box by the function above
    const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBoxValue(event.target.value)
    }
    return(
        <div style={{display:"flex", flexDirection:"column", justifyContent:"center", textAlign:"left"}}>
            <div style={{display:"flex", flexDirection:"column", height:"50px", justifyContent:"center", fontWeight:props.predicted? "bold" : "normal"}}>
                <label>{props.label}</label>
            </div>            
            <div style={{display:"flex", flexDirection:"row"}}>
                <input 
                    type="range" 
                    min={props.minVal} 
                    max={props.maxVal} value={value} 
                    id={props.label} step={props.step} 
                    onChange={handleSliderChange}
                    onMouseUp={handlePerfModeSlider}
                    onTouchEnd={handlePerfModeSlider}
                    style={{width:"80%"}}/>
                <input 
                    type="text" 
                    min={props.minVal} 
                    max={props.maxVal} 
                    value={boxValue} 
                    id={props.label} 
                    onChange={handleTextChange}
                    onBlur={handleTextEnter}
                    onKeyUp={(event) => {if(event.key === "Enter") handleTextEnter()}}
                    style={{width:"20%"}}/>
            </div>
        </div>
    )
}