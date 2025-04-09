import { LineChart, Line, XAxis, YAxis, Tooltip, TooltipProps, ReferenceArea, ResponsiveContainer, CartesianGrid, Label } from 'recharts';
import { NameType, ValueType } from 'recharts/types/component/DefaultTooltipContent';
import { useRecoilValue } from 'recoil';
import { csvCurve } from './CSVFileReader';
import {  useEffect, useState } from 'react';
import React from 'react';
import { curveWithCSVData } from './wrapper';
import { currentMorphology } from '../atoms/morphologyTemplate';

const SASTooltip = ({active, payload}:TooltipProps<ValueType, NameType>) => {//Function for the tooltip (popup view)
    if (active && payload && payload.length) {
        return (
            <div className="sas-tooltip" style={{backgroundColor:"#DDDDDD", textAlign:"left"}}>
              <p>{`Point Number: ${payload[0].payload[""]}`}</p>
              <>{isNaN(payload[0].payload.ICsv)? null : <p>{`Intensity (upload): ${payload[0].payload.ICsv}`}</p>}</>
              <>{isNaN(payload[0].payload.ISim)? null : <p>{`Intensity (sim): ${payload[0].payload.ISim}`}</p>}</>
              <p>{`Q: ${payload[0].payload.q}`}</p>
            </div>
          );
    }
}
//Custom tick marks trim X values down to avoid too many digit

class CustomizedAxisTick extends React.Component<{x?: number, y?:number, payload?:any}> {
  render() {
    const { x, y, payload } = this.props;
    console.log(payload);
    return (
      <g transform={`translate(${x},${y})`}>
        <text x={0} y={0} dy={12} textAnchor="middle" fill="#666">
          {payload.value.toFixed(4)}
        </text>
      </g>
    );
  }
}
export default function Charter(){
    const morphology = useRecoilValue(currentMorphology);
    const curveData = morphology==="/"? useRecoilValue(csvCurve):useRecoilValue(curveWithCSVData);
    const initialState = {
        data: curveData,
        left: "dataMin",
        right: "dataMax",
        refAreaLeft: "",
        refAreaRight: "",
        refHighlightAreaLeft: "",
        refHighlightAreaRight: "",
        top: "dataMax",
        bottom: "dataMin",
        // animation: true,
    };
    useEffect(() => {
        setState((prev) => ({
            ...prev,
            data:curveData,
          }));
          zoomOut();
    },[curveData])
    const getAxisYDomain = (
        from: number,
        to: number,
        ref1: string,
        ref2: string
      ) => {
        const refData: any[] = curveData.slice(from, to+1);
        console.log(refData)
        let initialValue = isNaN(refData[0][ref1])? refData[0][ref2] : refData[0][ref1]
        let [bottom, top] = [initialValue, initialValue];
        refData.forEach((d) => {
          if(!isNaN(d[ref1])){
            if (d[ref1] > top) top = d[ref1];
            if (d[ref1] < bottom) bottom = d[ref1];
          }
          if(!isNaN(d[ref2])){
            if (d[ref2] > top) top = d[ref2];
            if (d[ref2] < bottom) bottom = d[ref2];
          }
        });
        console.log(bottom, top)
        return [bottom,top];
    };
    const [state, setState] = useState<{
        data: any;
        left: string;
        right: string;
        refAreaLeft: string;
        refAreaRight: string;
        refHighlightAreaLeft: string;
        refHighlightAreaRight: string;
        top: string | number;
        bottom: string | number;
      }>(initialState);
    const {
        data,
        left,
        right,
        refAreaLeft,
        refAreaRight,
        refHighlightAreaLeft,
        refHighlightAreaRight,
        top,
        bottom
    } = state;
    const zoom = () => {
        if (refAreaLeft === refAreaRight || refAreaRight === "") {
          setState((prev) => ({
            ...prev,
            refAreaLeft: "",
            refAreaRight: "",
          }));
          return;
        }
            
        let [refAreaLeftTemp, refAreaRightTemp] = [refAreaLeft, refAreaRight];
    
        // xAxis domain
        if (refAreaLeft > refAreaRight)
          [refAreaLeftTemp, refAreaRightTemp] = [refAreaRight, refAreaLeft];
        // yAxis domain
        const [bottom, top] = getAxisYDomain(
          Number(refAreaLeftTemp),
          Number(refAreaRightTemp),
          "ICsv",
          "ISim"
        );
        if (refHighlightAreaLeft > refHighlightAreaRight){
            setState((prev) => ({
            refAreaLeft: "",
            refAreaRight: "",
            refHighlightAreaLeft: "",
            refHighlightAreaRight: "",
            data: prev.data.slice(),
            left: refHighlightAreaRight,
            right: refHighlightAreaLeft,
            bottom,
            top,
            }));
        }
        else{
            setState((prev) => ({
            refAreaLeft: "",
            refAreaRight: "",
            refHighlightAreaLeft: "",
            refHighlightAreaRight: "",
            data: prev.data.slice(),
            left: refHighlightAreaLeft,
            right: refHighlightAreaRight,
            bottom,
            top,
            }));
        }
      };
      const zoomOut = () => {
        setState((prev) => ({
          data: prev.data.slice(),
          refAreaLeft: "",
          refAreaRight: "",
          refHighlightAreaLeft: "",
          refHighlightAreaRight: "",
          left: "dataMin",
          right: "dataMax",
          top: "dataMax",
          bottom: "dataMin",
        }));
      };
      const component = (
        <div className="highlight-bar-charts" style={{ display:"flex", userSelect: "none", width:"70vw", 
        backgroundColor:"#EEEEEE", alignItems:"center", flexDirection:"column"}}>
            <button type="button" className="btn update" onClick={() => zoomOut()}>
            Zoom Out
            </button>
          <ResponsiveContainer height={305} width="95%">
            <LineChart
              data={data}
              onMouseDown={(e: any) =>
                setState((prev) => ({ ...prev, refHighlightAreaLeft: e.activeLabel, refAreaLeft: e.activeTooltipIndex}))
              }
              onMouseMove={(e: any) =>{
                state.refAreaLeft!== "" &&
                setState((prev) => ({ ...prev, refHighlightAreaRight: e.activeLabel, refAreaRight: e.activeTooltipIndex}))}
              }
              onMouseUp={() => zoom()}
              margin={{bottom:10, right: 5, top: 5, left: 5}}
            >
              <XAxis
                allowDataOverflow
                domain={[left, right]}
                type="number"
                dataKey={"q"} 
                tick={<CustomizedAxisTick/>} 
                scale="log"
              >
                <Label
                  value='q (Å)'
                  offset={0}
                  dx={0}
                  dy={15}
                  position="center"
                  fontSize={14}
                />
              </XAxis>
              <YAxis
                allowDataOverflow
                domain={[bottom, top]}
                type="number"
                yAxisId="1"
                label={{value: `Intensity (cm^-1)`,
                    style: { textAnchor: 'middle' },
                    angle: -90,
                    position: 'left',
                    offset: 0,}}
                tick={true}
                scale="log"
                padding={{bottom:0}}
              />
              <Tooltip content={<SASTooltip/>}/>
              <Line
                yAxisId="1"
                type="monotone"
                dataKey="ICsv"
                stroke="#8884d8"
                animationDuration={300}
                dot={false}
              />
              <Line
                yAxisId="1"
                type="monotone"
                dataKey="ISim"
                stroke="#950606"
                animationDuration={300}
                dot={false}
              />
              <CartesianGrid stroke="#ccc"/>
              {refHighlightAreaLeft && refHighlightAreaRight ? (
                <ReferenceArea
                  yAxisId="1"
                  x1={refHighlightAreaLeft}
                  x2={refHighlightAreaRight}
                  strokeOpacity={0.3}
                />
              ) : null}
            </LineChart>
          </ResponsiveContainer>
        </div>
      );
    return(
        <React.Fragment>
            {component}
        </React.Fragment>
    )
}