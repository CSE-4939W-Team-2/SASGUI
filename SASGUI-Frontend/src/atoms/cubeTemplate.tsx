import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const cubeLength = atom({
    key: 'cubeLength',
    default: 0
})
export const cubePolydispersity = atom({
    key: 'cubePolydispersity',
    default: 0
})
export const cubeScatteringLengthSolvent = atom({
    key: 'cubeScatteringLengthSolvent',
    default: 4
})
export const cubeScatteringLengthDensity = atom({
    key: 'cubeScatteringLengthDensity',
    default: 0
})
export const cubeBackground = atom({
    key: 'cubeBackground',
    default: 0.001
})
export const cubeScale = atom({
    key: 'cubeScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const cubeSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: cubeLength,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: cubePolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: cubeScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density",
        minVal: 0,
        maxVal: 30,
        step: 0.1,
        atomic: cubeScatteringLengthDensity,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: cubeBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: cubeScale,
        predicted: false
    }
]