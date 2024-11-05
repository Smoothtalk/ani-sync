import style from "./css/navbar.module.css";
import { UserContext } from "../context/UserContext";
import React, { useContext, useState } from "react";
import Logout from "../pages/Logout";

export default function NavBar() {
  const { user } = useContext(UserContext); //get user from context
  const [navBarOpen, setNavBarOpen] = useState(false);

  function toggleNavBar() {
    setNavBarOpen((prevState) => !prevState);
  }

  if (user === "") {
    return null;
  } else {
    return (
      <div className={style.navBarDiv}>
        <button className={style.navBarButton} onClick={toggleNavBar}>
          <img
            src="../static/icons/menu_icon.png"
            alt="Icon"
            className={style.navBarImg}
          ></img>
        </button>
        {navBarOpen && (
          <div className={style.navBarDiv}>
            <Logout toggleNavBar={toggleNavBar} />
          </div>
        )}
      </div>
    );
  }
}
