import React, { useEffect, useState } from "react";
import styles from "../css/anime/animeicon.module.css";

export default function AnimeIcon({ anime_id }) {
  const URL = "/anilist/get_anime_icon/";
  const [image_url, setImageURL] = useState("");

  useEffect(() => {
    async function getIcon(anime_id) {
      const res = await fetch(`${URL}?anime_id=${anime_id}`);
      const imageTag = await res.text();
      setImageURL(imageTag);
    }
    getIcon(anime_id);
  }, []);
  return (
    <div className={styles.animeIconDiv}>
      <img className={styles.animeIcon} src={image_url} />
    </div>
  );
}
