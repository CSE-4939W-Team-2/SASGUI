import { useState } from "react";
import { RecoilState, useRecoilState } from "recoil";

interface Props {
    label: string,
    minVal: number,
    maxVal: number,
    step: number,
    atomic: RecoilState<number>
}

export default function ParameterSlider(props:Props){
    const [value, setValue] = useRecoilState(props.atomic);
    const [boxValue, setBoxValue] = useState(value.toString());
    const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = parseFloat(event.target.value);
        setValue(newValue);
        setBoxValue(newValue.toString());
    }
    const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if(event.target.value !== ""){
            const newValue = parseFloat(event.target.value);
            if (newValue >= props.minVal && newValue<= props.maxVal){
                setValue(newValue);
                setBoxValue(newValue.toString());
            }
            else if (newValue < props.minVal){
                setValue(props.minVal);
                setBoxValue(props.minVal.toString());
            }
            else {
                setValue(props.maxVal);
                setBoxValue(props.maxVal.toString());
            }
        }
        else{
            setBoxValue(event.target.value)
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