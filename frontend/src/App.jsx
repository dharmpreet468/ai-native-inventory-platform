import {
  BrowserRouter,
  Route,
  Routes
} from 'react-router-dom'

import AppLayout from './layouts/AppLayout'

import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Warehouses from './pages/Warehouses'
import Inventory from './pages/Inventory'
import Orders from './pages/Orders'
import Analytics from './pages/Analytics'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />}/>

          <Route 
            path="/products"
            element={<Products />}/>

          <Route 
            path="/warehouses"
            element={<Warehouses />}/>

          <Route 
            path="/inventory"
            element={<Inventory />}/>

          <Route 
            path="/orders"
            element={<Orders />}/>

          <Route
            path="/analytics"
            element={<Analytics/>}/>
         
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App