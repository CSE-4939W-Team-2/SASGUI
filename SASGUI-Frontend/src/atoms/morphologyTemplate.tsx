import { atom, RecoilState } from "recoil";
import { csvCurveData } from "../components/CSVFileReader";

export const currentMorphology = atom({
    key: 'currentMorphology',
    default: "/"//Default is base link
})

export interface morphologyType {
    value: string,
    text: string,
}
export const morphologyValues:morphologyType[] = [
    //NOTE: the value must be the same as the react router path, with a "/" in front.
    //If react router path for morphology page is "sphere" then value must be "/sphere"
    //Each of these morphology values should have their own template file
    {
        value: "/sphere",
        text: "Sphere"
    },
    {
        value: "/coreShellSphere",
        text: "Core-Shell-Sphere"
    },
    {
        value: "/cylinder",
        text: "Cylinder"
    },
    {
        value: "/coreShellCylinder",
        text: "Core-Shell-Cylinder"
    },
    {
        value: "/disk",
        text: "Disk"
    },
    {
        value: "/coreShellDisk",
        text: "Core-Shell-Disk"
    }
]
//This is the type that defines the object used to save/load locally and remotely. Each page gets a field to store its sliders.
//When adding a new page, make sure to add logic for saving/loading to SaveLocal/LoadLocal.tsx and SaveRemote/LoadRemote.tsx
export interface saveLoad { 
    fileName: string;
    curveData: csvCurveData[];
    morphology: string;
    sphereData: {
        atom: RecoilState<number>;
        value: number;
    }[];
    coreShellSphereData: {
        atom: RecoilState<number>;
        value: number;
    }[];
    cylinderData: {
        atom: RecoilState<number>;
        value: number;
    }[];
    coreShellCylinderData: {
        atom: RecoilState<number>;
        value: number;
    }[];
    diskData: {
        atom: RecoilState<number>;
        value: number;
    }[];
    coreShellDiskData: {
        atom: RecoilState<number>;
        value: number;
    }[];
}

