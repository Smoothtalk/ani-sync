import React, { useContext, useState } from "react";
import { useEffect } from "react";
import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/recentdownloads/recentdownloads.module.css";
import { UserContext } from "../../context/UserContext";

export default function RecentDownloadsComponent() {
  const URL = "/transmission/get_recent_downloads/?username=";
  const [animeData, setAnimeData] = useState([]);
  const { user } = useContext(UserContext);

  useEffect(() => {
    async function fetchDownloads() {
      const res = await fetch(`${URL}${user}`);
      const data = await res.json();
      setAnimeData(data);
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
