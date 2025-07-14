import style from "./css/navbar.module.css";
import { UserContext } from "../context/UserContext";
import { NavBarContext } from "../context/NavBarContext";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import React, { useContext, useState } from "react";
import Logout from "./Logout";

export default function NavBar() {
  const navigate = useNavigate();
  const { user } = useContext(UserContext); //get user from context
  const { navBarOpen, setNavBarOpen } = useContext(NavBarContext);
  const location = useLocation();

  function toggleNavBar() {
    setNavBarOpen((prevState) => !prevState);
  }

  switch (location.pathname) {
    case "/":
      return null;
    default:
      return (
        <div className={style.navBarDiv}>
          <button className={style.navBarButton} onClick={toggleNavBar}>
            <img
              src="../static/icons/menu_icon.png"
              alt="Icon"
              className={style.navBarImg}
            ></img>
          </button>
          {(navBarOpen && user?.username) && <button onClick={() => navigate("/recent")}>Recent</button>}
          {(navBarOpen && user?.username) && <button onClick={() => navigate("/current")}>Current</button>} 
          {(navBarOpen && user?.username) && <button onClick={() => navigate("/utils")}>Utils</button>}
          {navBarOpen && <Logout location={location.pathname} />}
        </div>
      );
  }
}
