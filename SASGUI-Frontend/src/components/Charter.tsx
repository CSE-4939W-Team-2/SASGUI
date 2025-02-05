import { LineChart, Line, XAxis, YAxis, Tooltip, TooltipProps } from 'recharts';
import { NameType, ValueType } from 'recharts/types/component/DefaultTooltipContent';
import { useRecoilValue } from 'recoil';
import { csvCurve } from './CSVReader';

const SASTooltip = ({active, payload}:TooltipProps<ValueType, NameType>) => {
    if (active && payload && payload.length) {
        return (
            <div className="sas-tooltip" style={{backgroundColor:"black", textAlign:"left"}}>
              <p>{`Point Number: ${payload[0].payload.name}`}</p>
              <p>{`Intensity: ${payload[0].payload.I}`}</p>
              <p>{`Q: ${payload[0].payload.q}`}</p>
            </div>
          );
    }
}
export default function Charter(){
    const data = useRecoilValue(csvCurve);
    return(
    <LineChart width={1200} height={600} data={data}>
        <Line type="monotone" dataKey="I" stroke="#8884d8" />
        <YAxis label={{value: `Intensity (cm^-1)`,
            style: { textAnchor: 'middle' },
            angle: -90,
            position: 'left',
            offset: 0,}}
            tick={false}
            type="number"
            domain={['dataMin','dataMax']}
            scale="log"
        />
        <XAxis label={"q"} dataKey={"q"} tick={false} type="number" 
        domain={['dataMin','dataMax']} scale="log"/>
        <Tooltip content={<SASTooltip/>}/>
    </LineChart>
    )
}