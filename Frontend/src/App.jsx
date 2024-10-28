import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import RecentDownloads from "./pages/RecentDownloads";
import { UserProvider } from "./context/UserContext";

function App() {
  return (
    <BrowserRouter>
      {/* <RecentDownloadsTitleBar></RecentDownloadsTitleBar> */}
      <UserProvider>
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
