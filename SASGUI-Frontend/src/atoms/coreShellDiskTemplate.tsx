import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const coreShellDiskLength = atom({
    key: 'coreShellDiskLength',
    default: 0
})
export const coreShellDiskThickness = atom({
    key: 'coreShellDiskThickness',
    default: 0
})
export const coreShellDiskRadius = atom({
    key: 'coreShellDiskRadius',
    default: 0
})
export const coreShellDiskPolydispersity = atom({
    key: 'coreShellDiskPolydispersity',
    default: 0
})
export const coreShellDiskScatteringLengthSolvent = atom({
    key: 'coreShellDiskScatteringLengthSolvent',
    default: 4
})
export const coreShellDiskScatteringLengthShell = atom({
    key: 'coreShellDiskScatteringLengthShell',
    default: 2
})
export const coreShellDiskScatteringLengthCore = atom({
    key: 'coreShellDiskScatteringLengthCore',
    default: 1
})
export const coreShellDiskBackground = atom({
    key: 'coreShellDiskBackground',
    default: 0.001
})
export const coreShellDiskScale = atom({
    key: 'coreShellDiskScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const coreShellDiskSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 1600,
        step: 0.1,
        atomic: coreShellDiskLength,
        predicted: true
    },
    {
        label: "Thickness",
        minVal: 0,
        maxVal: 500,
        step: 0.1,
        atomic: coreShellDiskThickness,
        predicted: true
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: coreShellDiskRadius,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: coreShellDiskPolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density Shell",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthShell,
        predicted: false
    },
    {
        label: "Scattering Length Density Core",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthCore,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellDiskBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellDiskScale,
        predicted: false
    }
]