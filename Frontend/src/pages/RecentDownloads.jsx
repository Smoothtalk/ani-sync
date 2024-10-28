import React, { useContext } from "react";
import RecentDownloadsTitleBar from "../components/RecentDownloads/RecentDownloadsTitleBar";
import RecentDownloadsComponent from "../components/RecentDownloads/RecentDownloadsComponent";
import { UserContext, UserProvider } from "../context/UserContext";

export default function RecentDownloads() {
  const { user } = useContext(UserContext);
  return (
    <div>
      <RecentDownloadsTitleBar />
      <RecentDownloadsComponent />
    </div>
  );
}
