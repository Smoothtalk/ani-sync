import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/recentdownloads/recentdownloads.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";

export default function RecentDownloadsComponent() {
  const URL = "/transmission/get_recent_downloads/?username=";
  const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);

  useEffect(() => {
    async function fetchDownloads() {
      const res = await fetch(`${URL}${user}`);
      if (res.status === 200) {
        const data = await res.json();
        setAnimeData(data);
      } else {
        //handle errors here
      }
    }
    fetchDownloads();
  }, []);

  return (
    <div className={style.entries}>
      {animeData.map((anime) => (
        <AnimeEntry key={anime.guid} anime={anime} />
      ))}
    </div>
  );
}
