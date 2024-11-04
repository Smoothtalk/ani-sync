import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import RecentDownloads from "./pages/RecentDownloads";
import { UserProvider } from "./context/UserContext";
import NavBar from "./components/NavBar";

function App() {
  return (
    <BrowserRouter>
      <UserProvider>
        <NavBar></NavBar>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/recent" element={<RecentDownloads />} />
          <Route path="*" element={<h1>Not Found</h1>} />
        </Routes>
      </UserProvider>
    </BrowserRouter>
  );
}

export default App;
