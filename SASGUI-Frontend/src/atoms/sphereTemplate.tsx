import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const sphereRadius = atom({
    key: 'sphereRadius',
    default: 0
})
export const spherePolydispersity = atom({
    key: 'spherePolydispersity',
    default: 0
})
export const sphereScatteringLengthSolvent = atom({
    key: 'sphereScatteringLengthSolvent',
    default: 4
})
export const sphereScatteringLengthDensity = atom({
    key: 'sphereScatteringLengthDensity',
    default: 0
})
export const sphereBackground = atom({
    key: 'sphereBackground',
    default: 0.001
})
export const sphereScale = atom({
    key: 'sphereScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const sphereSliders:sliderObj[] = [
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: sphereRadius
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: spherePolydispersity
    },
    {
        label: "Scattering Length Density Solvent (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: sphereScatteringLengthSolvent
    },
    {
        label: "Scattering Length Density (Not Predicted)",
        minVal: 0,
        maxVal: 30,
        step: 0.1,
        atomic: sphereScatteringLengthDensity
    },
    {
        label: "Background (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: sphereBackground
    },
    {
        label: "Scale (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: sphereScale
    }
]