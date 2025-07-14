import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import { NavBarContext } from "../context/NavBarContext";
import style from "../components/css/navbarbutton.module.css";

export default function navBarButton({ buttonText, path }) {
  const navigate = useNavigate();
  const { user, setUser } = useContext(UserContext); //get user from context
  const { setNavBarOpen } = useContext(NavBarContext);
  const URL = "/user/logout/";

  async function handleLogout() {
    setNavBarOpen(false);

    if (buttonText === "Logout") {
      try {
        const res = await fetch(URL);
        if (res.status === 200) {
          document.cookie =
            "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/"; // Clear CSRF token
          localStorage.removeItem("user"); // Clear localStorage
          setUser({}); // Update user context
        }
      } catch (error) {
        console.error("Error during logout:", error);
      }
    } else {
      navigate("/");
    }
  }

  if (user?.username) {
    return (
        <div className={style.buttonDiv}>
        <button className={style.button} onClick={() => navigate(path)}>
            {buttonText}
        </button>
        </div>
  );
  } else {
    return (null);
  }


}
