import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/newuser.module.css";

export default function NewUser() {
  const navigate = useNavigate();
  const URL = "/user/new_user/";
  const [inputNewUserName, setInputNewUsername] = useState(""); //input field updating methods
  const [inputNewPassword, setInputNewPassword] = useState(""); //input field updating methods
  const [inputDiscordId, setInputDiscordId] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser({ username: inputNewUserName, password: inputNewPassword });
  }

  useEffect(() => {
    async function createNewUser() {
      //make a post request
      //${user}

      const res = await fetch(`${URL}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: user.username,
          password: user.password,
          discord_id: inputDiscordId,
        }),
      });

      if (res.status === 200) {
        //check if discord id is valid???
        navigate("/recent");
      } else {
        //error creating user
        setUser({});
        setInputNewUsername("");
        setInputDiscordId("");
      }
    }

    if (user?.username && user?.password) {
      createNewUser();
    }
  }, [user.username, user.password]);

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
          className={style.inputNewUsername}
          type="text"
          placeholder="Password"
          value={inputNewPassword}
          onChange={(e) => setInputNewPassword(e.target.value)}
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
