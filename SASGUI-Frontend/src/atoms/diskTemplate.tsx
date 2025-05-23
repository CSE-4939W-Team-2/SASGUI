import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const diskLength = atom({
    key: 'diskLength',
    default: 0
})
export const diskRadius = atom({
    key: 'diskRadius',
    default: 0
})
export const diskPolydispersity = atom({
    key: 'diskPolydispersity',
    default: 0
})
export const diskScatteringLengthSolvent = atom({
    key: 'diskScatteringLengthSolvent',
    default: 4
})
export const diskScatteringLengthDensity = atom({
    key: 'diskScatteringLengthDensity',
    default: 0
})
export const diskBackground = atom({
    key: 'diskBackground',
    default: 0.001
})
export const diskScale = atom({
    key: 'diskScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const diskSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 1600,
        step: 0.1,
        atomic: diskLength,
        predicted: true
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: diskRadius,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: diskPolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: diskScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density",
        minVal: 0,
        maxVal: 30,
        step: 0.1,
        atomic: diskScatteringLengthDensity,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: diskBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: diskScale,
        predicted: false
    }
]