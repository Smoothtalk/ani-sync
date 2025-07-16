import AnimeEntry from "../Anime/AnimeEntry";
import style from "../css/currentdownloads/currentdownloads.module.css";
import { UserContext } from "../../context/UserContext";
import { useEffect } from "react";
import React, { useContext, useState } from "react";
import { Progress } from "flowbite-react"; 3

export default function CurrentDownloadsComponent() {
  const TorrentDownloadsURL = "/transmission/get_current_downloads/?username=";
  const FileTransferURL = "/transmission/get_current_transfers/?username=";
  const [animeData, setAnimeData] = useState([]);
  const { user, setUser } = useContext(UserContext);
  const [torrentProgressData, setTorrentProgressData] = useState({});

  useEffect(() => {
    const currentTorrentRes = new EventSource(`${TorrentDownloadsURL}${user.username}`);
    // const currentFileTransfersRes = await fetch(`${FileTransferURL}${user.username}`);

    currentTorrentRes.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setTorrentProgressData(data);
      // update your progress bar here with `data`
    };

    currentTorrentRes.onerror = (err) => {
      console.error("SSE error:", err);
      currentTorrentRes.close();  // Optional: Close connection on error
    };

    return () => {
      currentTorrentRes.close(); // Clean up on unmount
    };

    // if (currentTorrentRes.status === 200) {
    //   const data = await currentTorrentRes.json();
    //   // setAnimeData(data);
    //   console.log(data)
    // } else {
    //   //handle errors here
    // }

    // if (currentFileTransfersRes.status === 200) {
    //   const data = await currentFileTransfersRes.json();
    //   // setAnimeData(data);
    //   console.log(data)
    // } else {
    //   //handle errors here
    // }
  }, []);

  return (
    <div className={style.entries}>
      <div className="p-4 space-y-4 bg-white shadow-md rounded-lg">
        <h2 className="text-lg font-semibold text-gray-800">Download Progress</h2>
        {Object.entries(torrentProgressData).map(([title, progress]) => (
          <div key={title}>
            <div className="mb-1 text-sm text-gray-700">{title}</div>
            <Progress progress={progress} size="lg" labelText labelProgress color="blue" />
          </div>
        ))}
      </div>
    </div>
  );
}
