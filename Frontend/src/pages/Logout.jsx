import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/logout.module.css";

export default function Logout(props) {
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext); //get user from context
  const { toggleNavBar } = props;

  function logout() {
    setUser("");
    navigate("/");
    {
      toggleNavBar();
    }
  }

  return (
    <div className={style.logoutDiv}>
      <button className={style.logoutSubmitButton} onClick={logout}>
        Logout
      </button>
    </div>
  );
}
