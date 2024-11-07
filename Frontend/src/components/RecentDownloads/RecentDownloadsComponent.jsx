import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/recentdownloads/recentdownloads.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";
import { Navigate } from "react-router-dom";

export default function RecentDownloadsComponent() {
  const URL = "/transmission/get_recent_downloads/?username=";
  const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);
  const [redirectToHome, setRedirectToHome] = useState(false);

  useEffect(() => {
    async function fetchDownloads() {
      const res = await fetch(`${URL}${user}`);
      if (res.status === 200) {
        const data = await res.json();
        setAnimeData(data);
      } else {
        setRedirectToHome(true);
      }
    }
    fetchDownloads();
  }, []);

  if (redirectToHome) {
    setUser("");
    return <Navigate to="/" replace />;
  }

  return (
    <div className={style.entries}>
      {animeData.map((anime) => (
        <AnimeEntry key={anime.guid} anime={anime} />
      ))}
    </div>
  );
}
