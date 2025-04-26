import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const coreShellCylinderLength = atom({
    key: 'coreShellCylinderLength',
    default: 0
})
export const coreShellCylinderThickness = atom({
    key: 'coreShellCylinderThickness',
    default: 0
})
export const coreShellCylinderRadius = atom({
    key: 'coreShellCylinderRadius',
    default: 0
})
export const coreShellCylinderPolydispersity = atom({
    key: 'coreShellCylinderPolydispersity',
    default: 0
})
export const coreShellCylinderScatteringLengthSolvent = atom({
    key: 'coreShellCylinderScatteringLengthSolvent',
    default: 4
})
export const coreShellCylinderScatteringLengthShell = atom({
    key: 'coreShellCylinderScatteringLengthShell',
    default: 2
})
export const coreShellCylinderScatteringLengthCore = atom({
    key: 'coreShellCylinderScatteringLengthCore',
    default: 1
})
export const coreShellCylinderBackground = atom({
    key: 'coreShellCylinderBackground',
    default: 0.001
})
export const coreShellCylinderScale = atom({
    key: 'coreShellCylinderScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const coreShellCylinderSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 1600,
        step: 0.1,
        atomic: coreShellCylinderLength,
        predicted: true
    },
    {
        label: "Thickness",
        minVal: 0,
        maxVal: 500,
        step: 0.1,
        atomic: coreShellCylinderThickness,
        predicted: true
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: coreShellCylinderRadius,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: coreShellCylinderPolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellCylinderScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density Shell",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellCylinderScatteringLengthShell,
        predicted: false
    },
    {
        label: "Scattering Length Density Core",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellCylinderScatteringLengthCore,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellCylinderBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellCylinderScale,
        predicted: false
    }
]