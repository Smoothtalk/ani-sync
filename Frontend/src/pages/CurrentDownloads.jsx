import React, { useContext } from "react";
import CurrentDownloadsTitleBar from "../components/CurrentDownloads/CurrentDownloadsTitleBar";
import CurrentDownloadsComponent from "../components/CurrentDownloads/CurrentDownloadsComponent";
import { UserContext } from "../context/UserContext";
import { Navigate } from "react-router-dom";


export default function CurrentDownloads() {
    const { user } = useContext(UserContext);
    if (user?.username) {
        return (
        <div>
            <CurrentDownloadsTitleBar />
            <CurrentDownloadsComponent />
        </div>
        );
    } else {
        return <Navigate to="/" replace />;
    }
}
