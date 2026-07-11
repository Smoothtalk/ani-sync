import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import NewUser from "./pages/NewUser";
import UserAnime from "./pages/UserAnime";
import Utils from "./pages/Utils";
import RecentDownloads from "./pages/RecentDownloads";
import CurrentDownloads from "./pages/CurrentDownloads";

import NavBar from "./components/NavBar";
import { UserProvider } from "./context/UserContext";
import { NavBarProvider } from "./context/NavBarContext";



function App() {
  return (
    <BrowserRouter>
      <UserProvider>
        <NavBarProvider>
          <NavBar></NavBar>
        </NavBarProvider>
        <Routes>
          <Route path="/"            element={<Login />} />
          <Route path="/recent"      element={<RecentDownloads />} />
          <Route path="/current"     element={<CurrentDownloads />} />
          <Route path="/useranime"   element={<UserAnime />} />
          <Route path="/utils"       element={<Utils />} />
          <Route path="/newuser"     element={<NewUser />} />
          <Route path="*"            element={<h1>Not Found</h1>} />
        </Routes>
      </UserProvider>
    </BrowserRouter>
  );
}

export default App;
