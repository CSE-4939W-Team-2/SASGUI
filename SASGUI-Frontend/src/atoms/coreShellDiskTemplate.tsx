import { atom } from "recoil";
import { sliderObj } from "../components/Page";

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

export const coreShellDiskSliders:sliderObj[] = [
    {
        label: "Length",
        minVal: 0,
        maxVal: 1600,
        step: 0.1,
        atomic: coreShellDiskLength
    },
    {
        label: "Thickness",
        minVal: 0,
        maxVal: 500,
        step: 0.1,
        atomic: coreShellDiskThickness
    },
    {
        label: "Radius",
        minVal: 0,
        maxVal: 800,
        step: 0.1,
        atomic: coreShellDiskRadius
    },
    {
        label: "Polydispersity",
        minVal: 0,
        maxVal: 1,
        step: 0.01,
        atomic: coreShellDiskPolydispersity
    },
    {
        label: "Scattering Length Density Solvent (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthSolvent
    },
    {
        label: "Scattering Length Density Shell (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthShell
    },
    {
        label: "Scattering Length Density Core (Not Predicted)",
        minVal: -30,
        maxVal: 30,
        step: 0.1,
        atomic: coreShellDiskScatteringLengthCore
    },
    {
        label: "Background (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellDiskBackground
    },
    {
        label: "Scale (Not Predicted)",
        minVal: 0.001,
        maxVal: 100,
        step: 0.001,
        atomic: coreShellDiskScale
    }
]