import { atom } from "recoil";

export const currentMorphology = atom({
    key: 'currentMorphology',
    default: "/"//Default is base link
})

export interface morphologyType {
    value: string,
    text: string
}
export const morphologyValues:morphologyType[] = [
    //NOTE: the value must be the same as the react router path, with a "/" in front.
    //If react router path for morphology page is "sphere" then value must be "/sphere"
    //Each of these morphology values should have their own template file
    {
        value: "/sphere",
        text: "Sphere"
    },
    {
        value: "/coreShellSphere",
        text: "Core-Shell-Sphere"
    },
    {
        value: "/cylinder",
        text: "Cylinder"
    },
    {
        value: "/coreShellCylinder",
        text: "Core-Shell-Cylinder"
    },
    {
        value: "/disk",
        text: "Disk"
    },
    {
        value: "/coreShellDisk",
        text: "Core-Shell-Disk"
    }
]