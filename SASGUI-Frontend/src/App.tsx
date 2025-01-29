import { useState } from 'react'
import './App.css'
import CSVReader from './components/CSVReader'
import Charter from './components/Charter'

function App() {
  const [curve, setCurve] = useState<{name:String, I:number, q:number}[]>([])
  return (
    <>
      <CSVReader curve={curve} setCurve={setCurve}/>
      <Charter curve={curve}></Charter>
    </>
  )
}

export default App
