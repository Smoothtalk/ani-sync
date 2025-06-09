import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/currentdownloads/currentdownloads.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";

export default function CurrentDownloadsComponent() {
  const TorrentDownloadsURL = "/transmission/get_current_downloads/?username=";
  const FileTransferURL = "/transmission/get_current_transfers/?username=";
  const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);

  useEffect(() => {
    async function fetchCurrentDownload() {
      // const res = await fetch(`${URL}${user.username}`);
      // if (res.status === 200) {
      //   const data = await res.json();
      //   setAnimeData(data);
      // } else {
      //   //handle errors here
      // }
    }
    fetchCurrentDownload();
  }, []);

  return (
    <div className={style.entries}>
      {/* {animeData.map((anime) => (
        <AnimeEntry key={anime.guid} anime={anime} />
      ))} */}
    </div>
  );
}
