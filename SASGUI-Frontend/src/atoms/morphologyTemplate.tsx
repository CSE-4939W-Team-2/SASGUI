import { atom } from "recoil";

export const currentMorphology = atom({
    key: 'currentMorphology',
    default: "/"
})

export interface morphologyType {
    value: string,
    text: string
}
export const morphologyValues:morphologyType[] = [
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