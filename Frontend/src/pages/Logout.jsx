import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/logout.module.css";

export default function Logout(props) {
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext); //get user from context
  const { toggleNavBar, location } = props;

  function logout() {
    document.cookie =
      "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    setUser("");
    navigate("/");
    {
      toggleNavBar();
    }
  }

  const buttonText = location === "/recent" ? "Logout" : "Return";

  return (
    <div className={style.logoutDiv}>
      <button className={style.logoutSubmitButton} onClick={logout}>
        {buttonText}
      </button>
    </div>
  );
}
