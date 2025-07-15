import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/utils/utils.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";

export default function UtilsComponent() {
  const URL = "/sync/";
  // const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);

  function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
      const [name, value] = cookie.split("=");
      if (name === "csrftoken") return value;
    }
    return null;
  }

  async function syncAnime() {
    const res = await fetch(`${URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      credentials: "include",
      body: JSON.stringify({
        username: user.username,
      }),
    });
    if (res.status === 200) {
      const data = await res.json();
      console.log(data)
    } else {
      //handle errors here
    }
  }

  useEffect(() => {

  }, []);

  return (
    <div className={style.utilDiv}>
      <button className={style.syncButton} onClick={syncAnime}>Sync</button>
    </div>
  );
}
