import './App.css'
import CSVReader from './components/CSVReader'
import Charter from './components/Charter'
import { RecoilRoot } from 'recoil'

function App() {
  return (
    <RecoilRoot>
      <CSVReader/>
      <Charter></Charter>
    </RecoilRoot>
  )
}

export default App
