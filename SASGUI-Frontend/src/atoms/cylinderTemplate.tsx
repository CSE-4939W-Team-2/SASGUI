import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const cylinderLength = atom({
    key: 'cylinderLength',
    default: 0
})
export const cylinderRadius = atom({
    key: 'cylinderRadius',
    default: 0
})
export const cylinderPolydispersity = atom({
    key: 'cylinderPolydispersity',
    default: 0
})
export const cylinderScatteringLengthSolvent = atom({
    key: 'cylinderScatteringLengthSolvent',
    default: 4
})
export const cylinderScatteringLengthDensity = atom({
    key: 'cylinderScatteringLengthDensity',
    default: 0
})
export const cylinderBackground = atom({
    key: 'cylinderBackground',
    default: 0.001
})
export const cylinderScale = atom({
    key: 'cylinderScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const cylinderSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 1600,
        step: 0.1,
        atomic: cylinderLength
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: cylinderRadius
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: cylinderPolydispersity
    },
    {
        label: "Scattering Length Density Solvent (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: cylinderScatteringLengthSolvent
    },
    {
        label: "Scattering Length Density (Not Predicted)",
        minVal: 0,
        maxVal: 30,
        step: 0.1,
        atomic: cylinderScatteringLengthDensity
    },
    {
        label: "Background (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: cylinderBackground
    },
    {
        label: "Scale (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: cylinderScale
    }
]