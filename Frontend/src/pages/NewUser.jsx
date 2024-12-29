import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/newuser.module.css";
import ClipLoader from "react-spinners/ClipLoader";
import bcrypt from "bcryptjs";

export default function NewUser() {
  const navigate = useNavigate();
  const URL = "/user/new_user/";
  const [inputNewUserName, setInputNewUsername] = useState(""); //input field updating methods
  const [inputNewPassword, setInputNewPassword] = useState(""); //input field updating methods
  const [inputDiscordId, setInputDiscordId] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context
  const [isLoadingVisible, setIsLoadingVisible] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setUser({ username: inputNewUserName });
  }

  function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
      const [name, value] = cookie.split("=");
      if (name === "csrftoken") return value;
    }
    return null;
  }

  useEffect(() => {
    async function createNewUser() {
      //make a post request
      //${user}

      const res = await fetch(`${URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
        body: JSON.stringify({
          username: inputNewUserName,
          password: inputNewPassword,
          discord_id: inputDiscordId,
        }),
      });

      setIsLoadingVisible(!isLoadingVisible);

      if (res.status === 200) {
        //check if discord id is valid???
        navigate("/recent");
      } else {
        //error creating user
        setUser({});
        setInputNewUsername("");
        setInputNewPassword("");
        setInputDiscordId("");
      }
    }

    if (inputNewUserName && inputNewPassword) {
      createNewUser();
    }
  }, [user?.username]);

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
        <div
          className={isLoadingVisible ? style.loadingDivShow : style.loadingDiv}
        >
          <ClipLoader
            size={45}
            color={"#ffffff"}
            loading={isLoadingVisible}
            speedMultiplier={1}
          />
        </div>
      </form>
    </div>
  );
}
