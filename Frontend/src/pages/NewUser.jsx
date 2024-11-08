import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import style from "../components/css/newuser.module.css";
import Cookies from "js-cookie";

export default function NewUser() {
  const navigate = useNavigate();
  const URL = "/anilist/create_user/";
  const [inputNewUserName, setInputNewUsername] = useState(""); //input field updating methods
  const [inputDiscordId, setInputDiscordId] = useState(""); //input field updating methods
  const { user, setUser } = useContext(UserContext); //get user from context

  function handleSubmit(e) {
    e.preventDefault();
    setUser(inputNewUserName);
  }

  useEffect(() => {
    async function createNewUser() {
      //make a post request
      //${user}

      const csrfToken = Cookies.get("csrftoken");

      if (!csrfToken) {
        //gen csrftoken
      }

      console.log(csrfToken);

      const res = await fetch(`${URL}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify({ firstParam: "asss", secondParam: "b" }),
      });
      if (res.status === 200) {
        //check if discord id is valid???
        //call backend to create new user in db

        // const data = await res.json();
        // navigate("/recent");
        console.log("url 200");

        //testing lines below
        setUser("");
        navigate("/");
      } else if (res.status === 404) {
        //error creating user
        setUser("");
        setInputNewUsername("");
        setInputDiscordId("");
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
