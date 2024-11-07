import React, { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/login.module.css";

export default function Login() {
  const navigate = useNavigate();
  const [value, setValue] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser(value);
    navigate("/recent");
  }

  if (user != "") {
    return <Navigate to="/recent" replace />;
  }

  return (
    <div className={style.loginDiv}>
      <form className={style.loginForm} onSubmit={handleSubmit}>
        <input
          className={style.loginInputUsername}
          type="text"
          placeholder="Username"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        ></input>
        <button className={style.loginSubmitButton} type="submit">
          Login
        </button>
      </form>
    </div>
  );
}
