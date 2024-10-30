import React, { useContext } from "react";
import RecentDownloadsTitleBar from "../components/RecentDownloads/RecentDownloadsTitleBar";
import RecentDownloadsComponent from "../components/RecentDownloads/RecentDownloadsComponent";
import { UserContext } from "../context/UserContext";
import { Navigate } from "react-router-dom";

export default function RecentDownloads() {
  const { user } = useContext(UserContext);
  if (user != "") {
    return (
      <div>
        <RecentDownloadsTitleBar />
        <RecentDownloadsComponent />
      </div>
    );
  } else {
    return <Navigate to="/" replace />;
  }
}
