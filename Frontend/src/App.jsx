import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import RecentDownloads from "./pages/RecentDownloads";
import NavBar from "./components/NavBar";
import NewUser from "./pages/NewUser";
import { UserProvider } from "./context/UserContext";
import { NavBarProvider } from "./context/NavBarContext";
import CurrentDownloads from "./pages/CurrentDownloads";

function App() {
  return (
    <BrowserRouter>
      <UserProvider>
        <NavBarProvider>
          <NavBar></NavBar>
        </NavBarProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/recent" element={<RecentDownloads />} />
          <Route path="/current" element={<CurrentDownloads />} />
          <Route path="/newuser" element={<NewUser />} />
          <Route path="*" element={<h1>Not Found</h1>} />
        </Routes>
      </UserProvider>
    </BrowserRouter>
  );
}

export default App;
