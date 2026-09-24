import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import { RegisterUser } from './pages/RegisterUser/RegisterUser'
import { LoginPage } from './pages/LoginUser'
import { HomePage } from './pages/MealTracking'
import { AppLayout } from './components/AppLayout'
import { WeeklyMenu } from './pages/WeeklyMenu'
import { ClassroomsPage } from './pages/ClassroomsPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/register' element={<RegisterUser/>}/>
        <Route path='/' element={<LoginPage/>}/>

        <Route element={<AppLayout/>}>
          <Route path='/home' element={<HomePage/>}/>
          <Route path='/weeklyMenu' element={<WeeklyMenu/>}/>
          <Route path='/classrooms' element={<ClassroomsPage/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
