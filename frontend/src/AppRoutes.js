import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./login";
import App from "./App"; // Your User Table page

function AppRoutes() {
  return (

    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/Inventory" element={<App />} />
    </Routes>

  );
}

export default AppRoutes;