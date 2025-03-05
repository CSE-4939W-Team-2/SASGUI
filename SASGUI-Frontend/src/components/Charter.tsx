import { LineChart, Line, XAxis, YAxis, Tooltip, TooltipProps, ReferenceArea, ResponsiveContainer } from 'recharts';
import { NameType, ValueType } from 'recharts/types/component/DefaultTooltipContent';
import { useRecoilValue } from 'recoil';
import { csvCurve } from './CSVFileReader';
import { useEffect, useState } from 'react';
import React from 'react';

const SASTooltip = ({active, payload}:TooltipProps<ValueType, NameType>) => {//Function for the tooltip
    if (active && payload && payload.length) {
        return (
            <div className="sas-tooltip" style={{backgroundColor:"#DDDDDD", textAlign:"left"}}>
              <p>{`Point Number: ${payload[0].payload[""]}`}</p>
              <p>{`Intensity (upload): ${payload[0].payload.ICsv}`}</p>
              <p>{`Intensity (sim): ${payload[0].payload.ISim}`}</p>
              <p>{`Q: ${payload[0].payload.q}`}</p>
            </div>
          );
    }
}
export default function Charter(){
    const csvData = useRecoilValue(csvCurve);
    const initialState = {
        data: csvData,
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
            data:csvData,
          }));
          zoomOut();
    },[csvData])
    const getAxisYDomain = (
        from: number,
        to: number,
        ref: string,
      ) => {
        const refData: any[] = csvData.slice(from, to+1);
        let [bottom, top] = [refData[0][ref], refData[0][ref]];
        refData.forEach((d) => {
          if (d[ref] > top) top = d[ref];
          if (d[ref] < bottom) bottom = d[ref];
        });
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
          "I",
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
          <ResponsiveContainer height={300} width="95%">
            <LineChart
              // width={800}
              // height={400}
              data={data}
              onMouseDown={(e: any) =>
                setState((prev) => ({ ...prev, refHighlightAreaLeft: e.activeLabel, refAreaLeft: e.activeTooltipIndex}))
              }
              onMouseMove={(e: any) =>{
                state.refAreaLeft!== "" &&
                setState((prev) => ({ ...prev, refHighlightAreaRight: e.activeLabel, refAreaRight: e.activeTooltipIndex}))}
              }
              onMouseUp={() => zoom()}
            >
              <XAxis
                allowDataOverflow
                domain={[left, right]}
                type="number"
                label={"q"} 
                dataKey={"q"} 
                tick={false} 
                scale="log"
              />
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
                tick={false}
                scale="log"
              />
              <Tooltip content={<SASTooltip/>}/>
              <Line
                yAxisId="1"
                type="monotone"
                dataKey="ICsv"
                stroke="#8884d8"
                animationDuration={300}
              />
              <Line
                yAxisId="1"
                type="monotone"
                dataKey="ISim"
                stroke="#950606"
                animationDuration={300}
              />
    
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