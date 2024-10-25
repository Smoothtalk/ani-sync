import React, { useState } from "react";
import { useEffect } from "react";
import AnimeEntry from "./Anime/AnimeEntry";
import style from "./css/recentdownloads.module.css";

export default function RecentDownloads() {
  const URL = "/transmission/get_recent_downloads/";
  const [animeData, setAnimeData] = useState([]);

  useEffect(() => {
    async function fetchDownloads() {
      const res = await fetch(`${URL}`);
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
