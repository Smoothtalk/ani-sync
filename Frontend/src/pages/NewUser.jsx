import React, { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/newuser.module.css";

export default function NewUser() {
  const navigate = useNavigate();
  const [inputNewUserName, setInputNewUsername] = useState(""); //input field updating methods
  const [inputDiscordId, setInputDiscordId] = useState(""); //input field updating methods
  const { setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser(inputNewUserName);
    navigate("/recent");
  }

  return (
    <div className={style.newUserDiv}>
      <form className={style.newUserForm} onSubmit={handleSubmit}>
        <input
          className={style.inputNewUsername}
          type="text"
          placeholder="Username"
          value={inputNewUserName}
          onChange={(e) => setInputNewUsername(e.target.value)}
        ></input>
        <input
          className={style.loginDiscordId}
          type="text"
          placeholder="DiscordId (Optional)"
          value={inputDiscordId}
          onChange={(e) => setInputDiscordId(e.target.value)}
        ></input>
        <button className={style.newUserSubmitButton} type="submit">
          Create New User
        </button>
      </form>
    </div>
  );
}
