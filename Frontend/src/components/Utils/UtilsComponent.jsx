import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/utils/utils.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";

export default function UtilsComponent() {
  const URL = "/transmission/get_recent_downloads/?username=";
  // const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);

  useEffect(() => {
    async function aFunction() {
      // const res = await fetch(`${URL}${user.username}`);
      // if (res.status === 200) {
      //   const data = await res.json();
      //   setAnimeData(data);
      // } else {
      //   //handle errors here
      // }
    }
    aFunction();
  }, []);

  return (
    <div className={style.entries}>
      
      {/* {animeData.map((anime) => (
        <AnimeEntry key={anime.guid} anime={anime} />
      ))} */}

    </div>
  );
}
