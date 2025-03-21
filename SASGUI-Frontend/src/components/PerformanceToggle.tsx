import { atom, useRecoilState } from "recoil"
//The global state atom for performance control
export const performanceMode = atom({
    key: 'performanceMode',
    default: false
})
export default function PerformanceToggle() {
    const [mode, setMode] = useRecoilState(performanceMode)
    return(
        <div style={{display:"flex", flexDirection:"row", marginBottom:"10px"}}>
            <button style={{width:"200px", height: "70px", marginRight:"5px", fontWeight: mode? "normal" : "bold"}}
            onClick={() => setMode(false)}>Quality Mode</button>
            <button style={{width:"200px", height: "70px", fontWeight: mode? "bold" : "normal"}}
            onClick={() => setMode(true)}>Performance Mode</button>
        </div>
    )
}