import React from "react";
import styles from "../css/anime/animereleasedate.module.css";

export default function AnimeReleaseDate({ release_date }) {
  return (
    <div className={styles.releasedateDiv}>
      <p className={styles.releasedate}>{release_date}</p>
    </div>
  );
}
