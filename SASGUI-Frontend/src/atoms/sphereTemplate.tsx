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
        atomic: sphereRadius,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: spherePolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: sphereScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density",
        minVal: 0,
        maxVal: 30,
        step: 0.1,
        atomic: sphereScatteringLengthDensity,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: sphereBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: sphereScale,
        predicted: false
    }
]