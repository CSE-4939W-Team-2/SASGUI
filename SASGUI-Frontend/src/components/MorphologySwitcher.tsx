export default function MorphologySwitcher() {
  
    return(
        <div style={{display:"flex", flexDirection:"row", marginBottom:"10px", alignItems:"center", marginRight:"100px"}}>
            <p>Select a Morphology: </p>
            <select name="morphologies" style={{height:"50px", backgroundColor:"#E1B6B0", borderRadius:"5px"}}>
                <option value="sphere" onClick={()=>{console.log("Sphere")}}>Sphere</option>
                <option value="coreShellSphere">Core-Shell-Sphere</option>
                <option value="coreShellCylinder">Core-Shell-Cylinder</option>
                <option value="coreShellDisk">Core-Shell-Disk</option>
                <option value="disk">Disk</option>
            </select>
        </div>
    )
}