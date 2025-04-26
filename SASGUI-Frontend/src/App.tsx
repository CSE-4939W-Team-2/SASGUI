import './App.css'
import { RecoilRoot } from 'recoil'
import Wrapper from './components/wrapper';


export const backend_link = import.meta.env.MODE === "production" ? import.meta.env.VITE_VM_URL : import.meta.env.VITE_LOCAL_URL
function App() {
  return (
    <RecoilRoot>
      <Wrapper/>
    </RecoilRoot>
  )
}

export default App
