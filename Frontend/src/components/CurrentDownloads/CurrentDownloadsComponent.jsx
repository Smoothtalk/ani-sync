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
      const currentTorrentRes = await fetch(`${TorrentDownloadsURL}${user.username}`);
      const currentFileTransfersRes = await fetch(`${FileTransferURL}${user.username}`);

      if (currentTorrentRes.status === 200) {
        const data = await currentTorrentRes.json();
        // setAnimeData(data);
        console.log(data)
      } else {
        //handle errors here
      }

      if (currentFileTransfersRes.status === 200) {
        const data = await currentFileTransfersRes.json();
        // setAnimeData(data);
        console.log(data)
      } else {
        //handle errors here
      }
    }
    fetchCurrentDownload();
  }, []);

  return (
    <div className={style.entries}>
      {
      /* {animeData.map((anime) => (
        <AnimeEntry key={anime.guid} anime={anime} />
      ))} */
      }
    </div>
  );
}
