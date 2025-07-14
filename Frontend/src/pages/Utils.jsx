import React, { useContext } from "react";
import { UserContext } from "../context/UserContext";
import { Navigate } from "react-router-dom";
import UtilsComponent from "../components/Utils/UtilsComponent"
import UtilsTitleBar from "../components/Utils/UtilsTitleBar";

// This will have a manual pull user anime button
// also redownload last x (have a field here) anime, show the last x anime

export default function Utils() {
  const { user } = useContext(UserContext);
  if (user?.username) {
    return (
      <div>
        <UtilsTitleBar></UtilsTitleBar>
        <UtilsComponent></UtilsComponent>
      </div>
    );
  } else {
    return <Navigate to="/" replace />;
  }
}
