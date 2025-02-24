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
        atomic: coreShellSphereThickness
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: coreShellSphereRadius
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: coreShellSpherePolydispersity
    },
    {
        label: "Scattering Length Density Solvent (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthSolvent
    },
    {
        label: "Scattering Length Density Shell (Not Predicted)",
        minVal: -30,
        maxVal: 100,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthShell
    },
    {
        label: "Scattering Length Density Core (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellSphereScatteringLengthCore
    },
    {
        label: "Background (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellSphereBackground
    },
    {
        label: "Scale (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellSphereScale
    }
]