import { useEffect, useState } from "react";
import { RecoilState, useRecoilState } from "recoil";

interface Props {
    label: string,
    minVal: number,
    maxVal: number,
    step: number,
    atomic: RecoilState<number>
}
export default function ParameterSlider(props:Props){
    const [value, setValue] = useRecoilState(props.atomic);//Get the atom of state for the slider
    const [boxValue, setBoxValue] = useState(value.toString()); //Text box value (separate to allow correcting overflow without affecting state)
    const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = parseFloat(event.target.value);
        setValue(newValue);
        setBoxValue(newValue.toString());
    }
    useEffect(()=>{
        setBoxValue(value.toString());//Make sure value gets set correctly when changing pages
    },[props])
    const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if(event.target.value !== ""){//Check if box is empty
            const newValue = parseFloat(event.target.value);
            if (newValue >= props.minVal && newValue<= props.maxVal){//Check if in range
                setValue(newValue);
                setBoxValue(newValue.toString());
            }
            else if (newValue < props.minVal){//Value too low, set to min
                setValue(props.minVal);
                setBoxValue(props.minVal.toString());
            }
            else {//Value too high, set to max
                setValue(props.maxVal);
                setBoxValue(props.maxVal.toString());
            }
        }
        else{
            setBoxValue(event.target.value)//To allow box to be empty
        }
    }
    return(
        <div style={{display:"flex", flexDirection:"column", justifyContent:"center", textAlign:"left"}}>
            <div style={{display:"flex", flexDirection:"column", height:"50px", justifyContent:"center"}}>
                <label>{props.label}</label>
            </div>            
            <div style={{display:"flex", flexDirection:"row"}}>
                <input 
                    type="range" 
                    min={props.minVal} 
                    max={props.maxVal} value={value} 
                    id={props.label} step={props.step} 
                    onChange={handleSliderChange} 
                    style={{width:"80%"}}/>
                <input 
                    type="text" 
                    min={props.minVal} 
                    max={props.maxVal} 
                    value={boxValue} 
                    id={props.label} 
                    onChange={handleTextChange} 
                    style={{width:"20%"}}/>
            </div>
        </div>
    )
}