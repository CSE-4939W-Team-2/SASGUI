import { atom } from "recoil";
import { sliderObj } from "../components/Page";
//For each slider, define an "atom" with a unique name and key, with a default value
export const coreShellSphereThickness = atom({
    key: 'coreShellSphereThickness',
    default: 0
})
export const coreShellSphereRadius = atom({
    key: 'coreShellSphereRadius',
    default: 0
})
export const coreShellSpherePolydispersity = atom({
    key: 'coreShellSpherePolydispersity',
    default: 0
})
export const coreShellSphereScatteringLengthSolvent = atom({
    key: 'coreShellSphereScatteringLengthSolvent',
    default: 4
})
export const coreShellSphereScatteringLengthShell = atom({
    key: 'coreShellSphereScatteringLengthShell',
    default: 2
})
export const coreShellSphereScatteringLengthCore = atom({
    key: 'coreShellSphereScatteringLengthCore',
    default: 1
})
export const coreShellSphereBackground = atom({
    key: 'coreShellSphereBackground',
    default: 0.001
})
export const coreShellSphereScale = atom({
    key: 'coreShellSphereScale',
    default: 0.001
})
//For each slider, create an object in this array that has a label, min and max value, step (increment), and the atom for the slider
export const coreShellSphereSliders:sliderObj[] = [
    {
        label: "Thickness",
        minVal: 0,
        maxVal: 500,
        step: 0.1,
        atomic: coreShellSphereThickness,
        predicted: true
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: coreShellSphereRadius,
        predicted: true
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: coreShellSpherePolydispersity,
        predicted: true
    },
    {
        label: "Scattering Length Density Solvent",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthSolvent,
        predicted: false
    },
    {
        label: "Scattering Length Density Shell",
        minVal: -30,
        maxVal: 100,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthShell,
        predicted: false
    },
    {
        label: "Scattering Length Density Core",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthCore,
        predicted: false
    },
    {
        label: "Background",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellSphereBackground,
        predicted: false
    },
    {
        label: "Scale",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellSphereScale,
        predicted: false
    }
]