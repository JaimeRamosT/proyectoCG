import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Tryitout from './components/Tryitout'
import Navbar from './components/Navbar'
import Readme from './components/Readme'

function App() {
  return (
    <BrowserRouter>
      <>
        <div className='min-h-screen w-full flex flex-col justify-center items-center bg-[#0d1116]'>
          <Navbar />
          <Routes>
            <Route path="/tryit" element={<Tryitout />} />
            <Route path="/" element={<Readme />} />
          </Routes>
        </div>
      </>
    </BrowserRouter>
  )
}

export default App
