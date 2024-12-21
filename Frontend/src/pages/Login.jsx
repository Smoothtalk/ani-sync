import React, { useContext, useEffect, useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/login.module.css";

export default function Login() {
  const navigate = useNavigate();
  const [userValue, setUserValue] = useState(""); //input field updating methods
  const [passwordValue, setPasswordValue] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context
  const URL = "/user/login/";

  function handleSubmit(e) {
    e.preventDefault();
    const clickedButton = e.nativeEvent.submitter;
    const buttonName = clickedButton.name;

    if (buttonName === "login") {
      setUser({ username: userValue, password: passwordValue });
    } else {
      navigate("/newuser");
    }
  }

  useEffect(() => {
    //function to call api to see if valid user exists in db
    async function checkLogin() {
      const res = await fetch(
        `${URL}?username=${user.username}&password=${user.password}`
      );
      if (res.status === 200) {
        navigate("/recent");
      } else {
        setUser({});
        setUserValue("");
        setPasswordValue("");
      }
    }

    if (user?.username && user?.password) {
      checkLogin();
    }
  }, [user.username, user.password]);

  // function newUser() {
  //   return <Navigate to="/newuser" replace />;
  // }

  return (
    <div className={style.loginDiv}>
      <form className={style.loginForm} onSubmit={handleSubmit}>
        <input
          className={style.loginInputUsername}
          type="text"
          placeholder="Username"
          value={userValue}
          onChange={(e) => setUserValue(e.target.value)}
        ></input>
        <input
          className={style.loginInputUsername}
          type="text"
          placeholder="Password"
          value={passwordValue}
          onChange={(e) => setPasswordValue(e.target.value)}
        ></input>
        <button name="login" className={style.loginSubmitButton}>
          Login
        </button>
        <button name="newuser" className={style.newUserButton}>
          New User
        </button>
      </form>
    </div>
  );
}
