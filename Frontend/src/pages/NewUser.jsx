import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/newuser.module.css";

export default function NewUser() {
  const navigate = useNavigate();
  const URL = "/anilist/";
  const [inputNewUserName, setInputNewUsername] = useState(""); //input field updating methods
  const [inputDiscordId, setInputDiscordId] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser(inputNewUserName);
  }

  useEffect(() => {
    async function createNewUser() {
      const res = await fetch(`${URL}${user}`);
      if (res.status === 200) {
        //check if discord id is valid???
        //call backend to create new user in db
        const data = await res.json();
        navigate("/recent");
      } else {
        setUser("");
        navigate("/");
      }
    }

    if (user) {
      createNewUser();
    }
  }, [user]);

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
